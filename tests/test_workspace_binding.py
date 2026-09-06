"""Regression tests for workspace AI feature detection, safe binding, and guard enforcement."""
from __future__ import annotations

import argparse
import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from notion_agent_cli.account import NotionAccount
from notion_agent_cli.bootstrap import (
    _extract_workspaces,
    _is_space_ai_enabled,
    bootstrap_account,
)
from notion_agent_cli.cli.__main__ import _cmd_doctor
from notion_agent_cli.exceptions import ErrorCode, NotionAgentError


def _sample_load_user_content_payload() -> dict:
    return {
        "recordMap": {
            "notion_user": {
                "user-1": {
                    "value": {
                        "id": "user-1",
                        "given_name": "Test",
                        "family_name": "User",
                        "email": "user@example.com",
                    }
                }
            },
            "space": {
                "space-ai-disabled": {
                    "value": {
                        "id": "space-ai-disabled",
                        "name": "Team Space",
                        "domain": "team-disabled",
                        "settings": {
                            "enable_ai_feature": False,
                            "disable_ai_feature": True,
                            "notion_admin_disabled_ai_feature": True,
                        },
                    }
                },
                "space-ai-enabled": {
                    "value": {
                        "id": "space-ai-enabled",
                        "name": "Team Space",
                        "domain": "team-enabled",
                        "settings": {
                            "enable_ai_feature": True,
                            "disable_ai_feature": False,
                            "enable_ai_training": False,
                        },
                    }
                },
            },
            "space_view": {
                "sv-1": {"value": {"id": "sv-1", "space_id": "space-ai-disabled"}},
                "sv-2": {"value": {"id": "sv-2", "space_id": "space-ai-enabled"}},
            },
        }
    }


def test_is_space_ai_enabled_checks_settings() -> None:
    enabled_rec = {"settings": {"enable_ai_feature": True, "disable_ai_feature": False}}
    disabled_rec_1 = {"settings": {"enable_ai_feature": False, "disable_ai_feature": True}}
    disabled_rec_2 = {"settings": {"notion_admin_disabled_ai_feature": True}}

    assert _is_space_ai_enabled(enabled_rec) is True
    assert _is_space_ai_enabled(disabled_rec_1) is False
    assert _is_space_ai_enabled(disabled_rec_2) is False


def test_extract_workspaces_marks_ai_status() -> None:
    data = _sample_load_user_content_payload()
    workspaces = _extract_workspaces(data)

    assert len(workspaces) == 2
    ws_map = {w.space_id: w for w in workspaces}
    assert ws_map["space-ai-disabled"].ai_enabled is False
    assert ws_map["space-ai-enabled"].ai_enabled is True


def test_bootstrap_account_prefers_ai_enabled_workspace_on_name_collision() -> None:
    payload = _sample_load_user_content_payload()

    with patch("notion_agent_cli.bootstrap.fetch_user_content", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = payload

        # Both workspaces are named "Team Space"
        acc = asyncio.run(
            bootstrap_account(
                token_v2="v03%3Asynthetic_test_token",
                space_name="Team Space",
            )
        )

        # Must auto-select the AI-enabled space
        assert acc.space_id == "space-ai-enabled"
        assert acc.space_name == "Team Space"


def test_bootstrap_account_supports_exact_space_id() -> None:
    payload = _sample_load_user_content_payload()

    with patch("notion_agent_cli.bootstrap.fetch_user_content", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = payload

        acc = asyncio.run(
            bootstrap_account(
                token_v2="v03%3Asynthetic_test_token",
                space_id="space-ai-enabled",
            )
        )
        assert acc.space_id == "space-ai-enabled"


def test_bootstrap_account_refuses_ai_disabled_workspace() -> None:
    payload = _sample_load_user_content_payload()

    with patch("notion_agent_cli.bootstrap.fetch_user_content", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = payload

        # Explicitly targeting the disabled workspace must fail fast
        with pytest.raises(NotionAgentError) as exc_info:
            asyncio.run(
                bootstrap_account(
                    token_v2="v03%3Asynthetic_test_token",
                    space_id="space-ai-disabled",
                )
            )

        assert exc_info.value.code == ErrorCode.AI_FEATURE_DISABLED
        assert "has Notion AI features disabled" in str(exc_info.value)


def test_doctor_detects_ai_disabled_workspace() -> None:
    payload = _sample_load_user_content_payload()
    acc_disabled = NotionAccount(
        token_v2="v03%3Asynthetic_token",
        user_id="user-1",
        space_id="space-ai-disabled",
        space_name="Team Space",
        space_view_id="sv-1",
        browser_id="test-browser-id",
        device_id="test-device-id",
        timezone="America/Los_Angeles",
        client_version="23.13.20260906.1700",
    )

    args = argparse.Namespace(
        account="dummy_account.json",
        json_out=True,
        refresh_client_version=False,
    )

    with patch("notion_agent_cli.cli.__main__.load_notion_account", return_value=acc_disabled), \
         patch("notion_agent_cli.cli.__main__._ping_load_user_content", new_callable=AsyncMock) as mock_ping, \
         patch("notion_agent_cli.cli.__main__.fetch_live_client_version", new_callable=AsyncMock) as mock_cv:
        mock_ping.return_value = payload
        mock_cv.return_value = "23.13.20260906.1700"

        exit_code = _cmd_doctor(args)
        assert exit_code == 1, "Doctor must fail when space AI is disabled"


def test_doctor_passes_when_workspace_ai_is_enabled() -> None:
    payload = _sample_load_user_content_payload()
    acc_enabled = NotionAccount(
        token_v2="v03%3Asynthetic_token",
        user_id="user-1",
        space_id="space-ai-enabled",
        space_name="Team Space",
        space_view_id="sv-2",
        browser_id="test-browser-id",
        device_id="test-device-id",
        timezone="America/Los_Angeles",
        client_version="23.13.20260906.1700",
    )

    args = argparse.Namespace(
        account="dummy_account.json",
        json_out=True,
        refresh_client_version=False,
    )

    with patch("notion_agent_cli.cli.__main__.load_notion_account", return_value=acc_enabled), \
         patch("notion_agent_cli.cli.__main__._ping_load_user_content", new_callable=AsyncMock) as mock_ping, \
         patch("notion_agent_cli.cli.__main__.fetch_live_client_version", new_callable=AsyncMock) as mock_cv:
        mock_ping.return_value = payload
        mock_cv.return_value = "23.13.20260906.1700"

        exit_code = _cmd_doctor(args)
        assert exit_code == 0, "Doctor must pass when space AI is enabled"
