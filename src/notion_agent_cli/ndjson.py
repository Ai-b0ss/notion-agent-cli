"""Parse the NDJSON event stream from ``/api/v3/runInferenceTranscript``.

Supports both response encodings:

- ``asPatchResponse=true`` (default) — Notion emits ``patch-start`` +
  ``patch`` events with jsonpatch-style ops (``a`` add, ``x`` append,
  ``p`` replace) against paths like ``/s/N/value/M/content``. We track
  each value entry's declared type so we can route content patches to
  the right accumulator.
- ``asPatchResponse=false`` (notion_manager / legacy) — Notion emits
  ``agent-inference`` events whose ``value[]`` carries cumulative text.
  Supported for symmetry with notion_manager-style fixtures.

The parser is stateful: feed lines one at a time, then call
:meth:`NDJSONStreamParser.finalize`. ``feed_line`` raises
:class:`NotionAgentError` on terminal events (``error`` /
``premium-feature-unavailable``).

Real-world observation (live capture 2026-05-15): for short replies
Notion bundles the entire ``agent-inference`` section into the single
``/s/-`` append patch with the text inline, rather than streaming it
incrementally via ``/s/N/value/-``. The :meth:`_absorb_inline_section`
helper handles that path so we don't drop short answers.
"""
from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from notion_agent_cli.exceptions import ErrorCode, NotionAgentError

log = logging.getLogger(__name__)


@dataclass(slots=True)
class NDJSONParseResult:
    text: str = ""
    thinking: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0
    notion_model: str | None = None
    line_count: int = 0
    event_type_counts: dict[str, int] = field(default_factory=dict)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _raise_if_error_entry(entry: Any) -> None:
    """Raise if a section entry is an inline ``{"type":"error",...}``.

    Notion's runInferenceTranscript can return 200 yet carry the failure
    *inside* the first ``patch-start`` section (``data.s[0]``) instead of
    a top-level ``error`` event — e.g. when the server-side
    ``checkRunInferenceTranscriptRuleSet`` denies the call
    (``subType: "trust-rule-denied"``, ``isRetryable: false``), which is
    what a burst of automated calls trips. Surfacing the real ``subType``
    + ``message`` keeps the caller from misreading it as a generic empty
    reply (or, worse, retrying a non-retryable denial).
    """
    if not isinstance(entry, dict) or entry.get("type") != "error":
        return
    sub = entry.get("subType") or "error"
    msg = entry.get("message") or "AI inference error"
    retryable = entry.get("isRetryable")
    code = (
        ErrorCode.TRUST_RULE_DENIED
        if sub == "trust-rule-denied"
        else ErrorCode.NOTION_ERROR
    )
    detail = f"notion denied inference [{sub}]: {msg}"
    if retryable is False:
        detail += (
            " — not retryable; likely an anti-automation trust rule or usage "
            "cap triggered by too many requests. Back off and retry later "
            "rather than hammering the endpoint"
        )
    # Carry the raw subType / isRetryable through so a structured caller
    # (chat --json) can branch on them without scraping ``detail``.
    raise NotionAgentError(detail, code=code, subtype=sub, retryable=retryable)


def _handle_patch_replace(current: str, replacement: str) -> str:
    if not replacement:
        return current
    if replacement.startswith(current) or current.startswith(replacement):
        return replacement if len(replacement) > len(current) else current
    return replacement


class NDJSONStreamParser:
    """Stateful parser for runInferenceTranscript NDJSON streams."""

    def __init__(self) -> None:
        self.input_tokens: int = 0
        self.output_tokens: int = 0
        self.cache_read_tokens: int = 0
        self.cache_creation_tokens: int = 0
        self.notion_model: str | None = None
        self.line_count: int = 0
        self.event_type_counts: dict[str, int] = {}

        # Slot tracking for patch mode:
        # slot path (e.g. "/s/7/value/0") -> content string
        self._slot_contents: dict[str, str] = {}
        # slot path -> type ("text"|"thinking"|"tool_use")
        self._slot_types: dict[str, str] = {}
        # Ordered list of slot paths to maintain insertion order
        self._slot_order: list[str] = []

        # Number of value entries seen per section prefix ("/s/N")
        self._value_counts: dict[str, int] = {}
        # Number of top-level sections (/s) seen
        self._section_count: int = 0

        # Legacy (asPatchResponse=false) mode accumulators
        self._legacy_text: str = ""
        self._legacy_thinking: str = ""
        self._has_legacy: bool = False

    @property
    def text(self) -> str:
        if self._has_legacy:
            return self._legacy_text
        return "".join(
            self._slot_contents[s]
            for s in self._slot_order
            if self._slot_types.get(s) == "text"
        )

    @property
    def thinking(self) -> str:
        if self._has_legacy:
            return self._legacy_thinking
        return "".join(
            self._slot_contents[s]
            for s in self._slot_order
            if self._slot_types.get(s) == "thinking"
        )

    # ---------------------------- public API ---------------------------- #

    def feed_line(self, line: str) -> None:
        line = line.strip()
        if not line:
            return
        self.line_count += 1
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            log.debug("ndjson: skip non-json line: %s", line[:200])
            return

        event_type = event.get("type")
        if not isinstance(event_type, str):
            return
        self.event_type_counts[event_type] = self.event_type_counts.get(event_type, 0) + 1

        if event_type == "error":
            msg = event.get("message") or event.get("data") or "unknown notion error"
            raise NotionAgentError(
                f"notion error event: {msg}",
                code=ErrorCode.NOTION_ERROR,
            )
        if event_type == "premium-feature-unavailable":
            raise NotionAgentError(
                "notion premium feature unavailable — account/thread cannot use the "
                "requested model or capability",
                code=ErrorCode.PREMIUM_REQUIRED,
            )

        if event_type == "patch":
            self._handle_patch(event)
            return
        if event_type in ("patch-start", "patch-sync"):
            self._handle_patch_start(event)
            return
        if event_type == "agent-inference":
            self._handle_agent_inference(event)
            return
        # Other events (agent-tool-result, agent-search-extracted-results,
        # heartbeat, record-map, etc.) are not needed for text + usage.

    def feed(self, lines: Iterable[str]) -> None:
        for line in lines:
            self.feed_line(line)

    def finalize(self) -> NDJSONParseResult:
        return NDJSONParseResult(
            text=self.text,
            thinking=self.thinking,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
            cache_read_tokens=self.cache_read_tokens,
            cache_creation_tokens=self.cache_creation_tokens,
            notion_model=self.notion_model,
            line_count=self.line_count,
            event_type_counts=dict(self.event_type_counts),
        )

    # ---------------------------- patch mode ---------------------------- #

    def _register_slot(
        self,
        slot_path: str,
        entry_type: str | None,
        initial_content: str = "",
    ) -> None:
        if slot_path not in self._slot_order:
            self._slot_order.append(slot_path)
        if entry_type:
            self._slot_types[slot_path] = entry_type
        if slot_path not in self._slot_contents:
            self._slot_contents[slot_path] = initial_content
        elif initial_content:
            current = self._slot_contents[slot_path]
            self._slot_contents[slot_path] = _handle_patch_replace(current, initial_content)

    def _extract_slot_path(self, path: str) -> str:
        idx = path.rfind("/content")
        if idx >= 0:
            return path[:idx]
        return path

    def _handle_patch_start(self, event: dict[str, Any]) -> None:
        data = event.get("data") or {}
        s = data.get("s")
        if isinstance(s, list):
            self._section_count = max(self._section_count, len(s))
            for i, entry in enumerate(s):
                _raise_if_error_entry(entry)
                if isinstance(entry, dict):
                    self._absorb_inline_section(i, entry)

    def _handle_patch(self, event: dict[str, Any]) -> None:
        ops = event.get("v")
        if not isinstance(ops, list):
            return
        for op in ops:
            if isinstance(op, dict):
                self._handle_patch_op(op)

    def _handle_patch_op(self, op: dict[str, Any]) -> None:
        o = op.get("o")
        p = op.get("p")
        v = op.get("v")
        if not isinstance(o, str) or not isinstance(p, str):
            return

        # 0) New section appended at /s/- — may carry an inline ``value``
        # list with the entire turn's text (common for short replies).
        if o == "a" and p == "/s/-" and isinstance(v, dict):
            section_idx = self._section_count
            self._section_count += 1
            self._absorb_inline_section(section_idx, v)
            return

        # 1) New value entry added at /s/N/value/- → register its slot.
        if o == "a" and "/value/-" in p and isinstance(v, dict):
            state_prefix = p[: p.index("/value/")]
            idx = self._value_counts.get(state_prefix, 0)
            slot_path = f"{state_prefix}/value/{idx}"
            self._value_counts[state_prefix] = idx + 1

            entry_type = v.get("type") or "text"
            content = v.get("content") or ""
            self._register_slot(slot_path, entry_type, content)
            return

        # 2) Usage tokens (per-section).
        if o == "a" and p.endswith("/inputTokens") and _is_int(v):
            self.input_tokens += int(v)
            return
        if o == "a" and p.endswith("/outputTokens") and _is_int(v):
            self.output_tokens += int(v)
            return
        if o == "a" and p.endswith("/cachedTokensRead") and _is_int(v):
            self.cache_read_tokens += int(v)
            return
        if o == "a" and p.endswith("/cachedTokensCreated") and _is_int(v):
            self.cache_creation_tokens += int(v)
            return

        # 3) Model id surfacing.
        if o == "a" and p.endswith("/model") and isinstance(v, str):
            self.notion_model = v
            return

        # 4) Incremental content patches.
        if "content" not in p:
            return
        if not isinstance(v, str):
            return

        slot_path = self._extract_slot_path(p)
        entry_type = self._slot_types.get(slot_path, "text")
        if entry_type == "tool_use":
            return

        if slot_path not in self._slot_contents:
            self._register_slot(slot_path, entry_type, "")

        if o == "x":
            self._slot_contents[slot_path] = self._slot_contents[slot_path] + v
        elif o == "p":
            self._slot_contents[slot_path] = _handle_patch_replace(self._slot_contents[slot_path], v)

    def _absorb_inline_section(self, section_idx: int, section: dict[str, Any]) -> None:
        """Absorb a section (from patch-start, patch-sync, or /s/- op) into slot tracking.

        Registers each entry at ``/s/N/value/M`` slot and updates/reconciles content.
        """
        section_type = section.get("type")
        values = section.get("value")
        if not isinstance(values, list):
            return
        if section_type not in ("agent-inference", "agent-reply", "assistant-reply"):
            return
        section_prefix = f"/s/{section_idx}"
        for i, entry in enumerate(values):
            if not isinstance(entry, dict):
                continue
            etype = entry.get("type") or "text"
            content = entry.get("content") or ""
            slot_path = f"{section_prefix}/value/{i}"
            self._register_slot(slot_path, etype, content)
        self._value_counts[section_prefix] = max(self._value_counts.get(section_prefix, 0), len(values))

    # ----------------------- legacy / non-patch mode -------------------- #

    def _handle_agent_inference(self, event: dict[str, Any]) -> None:
        """Handle ``asPatchResponse=false`` mode (cumulative agent-inference)."""
        self._has_legacy = True
        values = event.get("value")
        if isinstance(values, list):
            text_parts: list[str] = []
            thinking_parts: list[str] = []
            for entry in values:
                if not isinstance(entry, dict):
                    continue
                etype = entry.get("type")
                content = entry.get("content")
                if etype == "text" and isinstance(content, str):
                    text_parts.append(content)
                elif etype == "thinking" and isinstance(content, str):
                    thinking_parts.append(content)
            if text_parts:
                self._legacy_text = "".join(text_parts)
            if thinking_parts:
                self._legacy_thinking = "".join(thinking_parts)

        if _is_int(event.get("inputTokens")):
            self.input_tokens += int(event["inputTokens"])
        if _is_int(event.get("outputTokens")):
            self.output_tokens += int(event["outputTokens"])

        model = event.get("model")
        if isinstance(model, str):
            self.notion_model = model


def parse_ndjson_stream(lines: Iterable[str]) -> NDJSONParseResult:
    """Convenience: parse a complete iterable of lines in one call."""
    parser = NDJSONStreamParser()
    parser.feed(lines)
    return parser.finalize()
