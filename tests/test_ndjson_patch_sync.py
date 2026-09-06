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
