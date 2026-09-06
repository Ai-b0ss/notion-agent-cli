"""Regression tests for NDJSON stream parser handling patch-sync and patch-start."""
from __future__ import annotations

import json
import pytest

from notion_agent_cli.exceptions import ErrorCode, NotionAgentError
from notion_agent_cli.ndjson import NDJSONStreamParser


def test_ndjson_parser_handles_patch_sync_with_inline_sections() -> None:
    parser = NDJSONStreamParser()
    events = [
        {
            "type": "patch-sync",
            "data": {
                "s": [
                    {
                        "type": "agent-inference",
                        "value": [{"type": "text", "content": "SESSION_OK"}],
                    }
                ]
            },
        },
    ]
    lines = [json.dumps(ev) for ev in events]
    parser.feed(lines)
    result = parser.finalize()

    assert result.text == "SESSION_OK"
    assert result.event_type_counts["patch-sync"] == 1


def test_ndjson_parser_handles_patch_sync_followed_by_inline_patch() -> None:
    parser = NDJSONStreamParser()
    events = [
        {"type": "patch-sync", "data": {"s": []}},
        {
            "type": "patch",
            "v": [
                {
                    "o": "a",
                    "p": "/s/-",
                    "v": {
                        "type": "agent-inference",
                        "value": [{"type": "text", "content": "Hello from patched Notion session!"}],
                    },
                }
            ],
        },
    ]
    lines = [json.dumps(ev) for ev in events]
    parser.feed(lines)
    result = parser.finalize()

    assert result.text == "Hello from patched Notion session!"
    assert result.event_type_counts["patch-sync"] == 1
    assert result.event_type_counts["patch"] == 1


def test_ndjson_parser_handles_patch_sync_followed_by_incremental_stream() -> None:
    parser = NDJSONStreamParser()
    events = [
        {"type": "patch-sync", "data": {"s": []}},
        {
            "type": "patch",
            "v": [
                {
                    "o": "a",
                    "p": "/s/-",
                    "v": {
                        "type": "agent-inference",
                        "value": [],
                    },
                },
                {
                    "o": "a",
                    "p": "/s/0/value/-",
                    "v": {
                        "type": "text",
                        "content": "SES",
                    },
                },
                {
                    "o": "x",
                    "p": "/s/0/value/0/content",
                    "v": "SION_OK",
                },
            ],
        },
    ]
    lines = [json.dumps(ev) for ev in events]
    parser.feed(lines)
    result = parser.finalize()

    assert result.text == "SESSION_OK"


def test_ndjson_parser_raises_on_error_inside_patch_sync() -> None:
    parser = NDJSONStreamParser()
    events = [
        {
            "type": "patch-sync",
            "data": {
                "s": [
                    {
                        "type": "error",
                        "subType": "trust-rule-denied",
                        "isRetryable": False,
                    }
                ]
            },
        }
    ]
    lines = [json.dumps(ev) for ev in events]
    with pytest.raises(NotionAgentError) as exc_info:
        parser.feed(lines)

    assert exc_info.value.code == ErrorCode.TRUST_RULE_DENIED
    assert exc_info.value.subtype == "trust-rule-denied"
    assert exc_info.value.retryable is False


def test_ndjson_parser_prevents_duplication_on_live_patch_sync_sequence() -> None:
    """Exact reproduction of live Notion stream where patch-start, inline patch section,
    incremental content append, and trailing patch-sync snapshot previously produced
    'SESSION_OKSESSION_OK'.
    """
    parser = NDJSONStreamParser()
    events = [
        # Line 0: patch-start
        {
            "type": "patch-start",
            "data": {
                "s": [
                    {"type": "agent-instruction-state", "value": [{"type": "text", "content": ""}]},
                ]
            },
        },
        # Line 1: dummy tool / state section appended
        {
            "type": "patch",
            "v": [{"o": "a", "p": "/s/-", "v": {"type": "agent-tool-use", "value": []}}],
        },
        # Line 7: inference section appended with inline "SESSION"
        {
            "type": "patch",
            "v": [
                {
                    "o": "a",
                    "p": "/s/-",
                    "v": {
                        "type": "agent-inference",
                        "value": [{"type": "text", "content": "SESSION"}],
                    },
                }
            ],
        },
        # Line 8: incremental patch appending "_OK"
        {
            "type": "patch",
            "v": [{"o": "x", "p": "/s/2/value/0/content", "v": "_OK"}],
        },
        # Line 9..11: tokens
        {
            "type": "patch",
            "v": [
                {"o": "a", "p": "/s/2/outputTokens", "v": 4},
                {"o": "a", "p": "/s/2/inputTokens", "v": 100},
            ],
        },
        # Line 12: patch-sync with full snapshot of s
        {
            "type": "patch-sync",
            "data": {
                "s": [
                    {"type": "agent-instruction-state", "value": [{"type": "text", "content": ""}]},
                    {"type": "agent-tool-use", "value": []},
                    {
                        "type": "agent-inference",
                        "value": [{"type": "text", "content": "SESSION_OK"}],
                        "outputTokens": 4,
                        "inputTokens": 100,
                    },
                ]
            },
        },
    ]
    lines = [json.dumps(ev) for ev in events]
    parser.feed(lines)
    result = parser.finalize()

    assert result.text == "SESSION_OK"
    assert result.output_tokens == 4
    assert result.input_tokens == 100


def test_ndjson_parser_preserves_legitimate_repeated_text() -> None:
    """Verifies that repetitive model output (e.g. 'hello hello') is preserved,
    both in incremental stream chunks and across multiple text slots.
    """
    # Case A: incremental chunks within a slot
    parser_a = NDJSONStreamParser()
    events_a = [
        {"type": "patch-start", "data": {"s": []}},
        {
            "type": "patch",
            "v": [
                {"o": "a", "p": "/s/-", "v": {"type": "agent-inference", "value": [{"type": "text", "content": "hello "}]}},
                {"o": "x", "p": "/s/0/value/0/content", "v": "hello"},
            ],
        },
        {
            "type": "patch-sync",
            "data": {
                "s": [
                    {"type": "agent-inference", "value": [{"type": "text", "content": "hello hello"}]},
                ]
            },
        },
    ]
    parser_a.feed([json.dumps(ev) for ev in events_a])
    assert parser_a.finalize().text == "hello hello"

    # Case B: repeated text across multiple text entries/slots
    parser_b = NDJSONStreamParser()
    events_b = [
        {"type": "patch-start", "data": {"s": []}},
        {
            "type": "patch",
            "v": [
                {
                    "o": "a",
                    "p": "/s/-",
                    "v": {
                        "type": "agent-inference",
                        "value": [
                            {"type": "text", "content": "hello "},
                            {"type": "text", "content": "hello"},
                        ],
                    },
                }
            ],
        },
    ]
    parser_b.feed([json.dumps(ev) for ev in events_b])
    assert parser_b.finalize().text == "hello hello"


def test_ndjson_parser_preserves_thinking_and_text_separation() -> None:
    parser = NDJSONStreamParser()
    events = [
        {"type": "patch-start", "data": {"s": []}},
        {
            "type": "patch",
            "v": [
                {
                    "o": "a",
                    "p": "/s/-",
                    "v": {
                        "type": "agent-inference",
                        "value": [
                            {"type": "thinking", "content": "Thinking about it... "},
                            {"type": "text", "content": "Here is the answer."},
                        ],
                    },
                },
                {"o": "x", "p": "/s/0/value/0/content", "v": "Done thinking."},
            ],
        },
        {
            "type": "patch-sync",
            "data": {
                "s": [
                    {
                        "type": "agent-inference",
                        "value": [
                            {"type": "thinking", "content": "Thinking about it... Done thinking."},
                            {"type": "text", "content": "Here is the answer."},
                        ],
                    }
                ]
            },
        },
    ]
    parser.feed([json.dumps(ev) for ev in events])
    res = parser.finalize()
    assert res.thinking == "Thinking about it... Done thinking."
    assert res.text == "Here is the answer."
