"""Regression tests for inference request transcript builder protocol fields."""
from __future__ import annotations

from notion_agent_cli.account import NotionAccount
from notion_agent_cli.transcript import build_inference_request


def _synthetic_account() -> NotionAccount:
    return NotionAccount(
        token_v2="v03%3Asynthetic_test_token_12345",
        user_id="11111111-2222-3333-4444-555555555555",
        user_name="Synthetic User",
        user_email="testuser@example.com",
        space_id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        space_view_id="99999999-8888-7777-6666-555555555555",
        space_name="Synthetic Workspace",
        browser_id="bbbbbbbb-cccc-dddd-eeee-ffffffffffff",
        device_id="dddddddd-eeee-ffff-0000-111111111111",
        timezone="America/Los_Angeles",
    )


def test_build_inference_request_includes_patch_v2_and_nudge_support() -> None:
    acc = _synthetic_account()
    body = build_inference_request(
        acc=acc,
        transcript=[],
        thread_id="thread-test-123",
        create_thread=True,
        is_partial_transcript=False,
    )

    assert body["patchResponseVersion"] == 2
    assert body["supportsCustomAgentNudgeTranscriptStep"] is True
    assert body["asPatchResponse"] is True
    assert body["spaceId"] == acc.space_id
    assert body["threadType"] == "workflow"
