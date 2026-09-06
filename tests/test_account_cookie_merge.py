"""Regression tests for cookie parsing and session merging in NotionAccount."""
from __future__ import annotations

from notion_agent_cli.account import NotionAccount, build_cookie_header, parse_browser_cookie


def _synthetic_account(full_cookie: str | None = None) -> NotionAccount:
    return NotionAccount(
        token_v2="v03%3Asynthetic_test_token_12345",
        user_id="11111111-2222-3333-4444-555555555555",
        user_name="Synthetic Test User",
        user_email="testuser@example.com",
        space_id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        space_view_id="99999999-8888-7777-6666-555555555555",
        space_name="Synthetic Workspace",
        browser_id="bbbbbbbb-cccc-dddd-eeee-ffffffffffff",
        device_id="dddddddd-eeee-ffff-0000-111111111111",
        timezone="America/Los_Angeles",
        full_cookie=full_cookie,
    )


def test_parse_browser_cookie_basic() -> None:
    raw = "token_v2=v03%3Afoo; notion_user_id=123; device_id=456; invalid_part"
    parsed = parse_browser_cookie(raw)
    assert parsed["token_v2"] == "v03%3Afoo"
    assert parsed["notion_user_id"] == "123"
    assert parsed["device_id"] == "456"
    assert "invalid_part" not in parsed


def test_build_cookie_header_when_full_cookie_none() -> None:
    acc = _synthetic_account(full_cookie=None)
    hdr = build_cookie_header(acc)
    parsed = parse_browser_cookie(hdr)

    assert parsed["token_v2"] == acc.token_v2
    assert parsed["notion_user_id"] == acc.user_id
    assert parsed["notion_browser_id"] == acc.browser_id
    assert parsed["device_id"] == acc.device_id
    assert parsed["notion_users"] == f'[%22{acc.user_id}%22]'
    assert parsed["notion_check_cookie_consent"] == "false"
    assert parsed["notion_locale"] == "en-US/autodetect"


def test_build_cookie_header_merges_partial_full_cookie() -> None:
    # Operator provided only token_v2 and notion_user_id in full_cookie
    partial = f"token_v2={_synthetic_account().token_v2}; notion_user_id={_synthetic_account().user_id}"
    acc = _synthetic_account(full_cookie=partial)
    hdr = build_cookie_header(acc)
    parsed = parse_browser_cookie(hdr)

    # Required active identity/device cookies must be stitched in
    assert parsed["token_v2"] == acc.token_v2
    assert parsed["notion_user_id"] == acc.user_id
    assert parsed["notion_browser_id"] == acc.browser_id
    assert parsed["device_id"] == acc.device_id
    assert parsed["notion_users"] == f'[%22{acc.user_id}%22]'
    assert parsed["notion_check_cookie_consent"] == "false"
    assert parsed["notion_locale"] == "en-US/autodetect"


def test_build_cookie_header_preserves_custom_cookie_attributes() -> None:
    # Operator cookie already has custom notion_locale and browser_id
    custom = (
        f"token_v2={_synthetic_account().token_v2}; "
        f"notion_browser_id=custom-browser-id-999; "
        f"notion_locale=fr-FR; "
        f"custom_telemetry_id=telemetry-abc"
    )
    acc = _synthetic_account(full_cookie=custom)
    hdr = build_cookie_header(acc)
    parsed = parse_browser_cookie(hdr)

    assert parsed["notion_browser_id"] == "custom-browser-id-999"
    assert parsed["notion_locale"] == "fr-FR"
    assert parsed["custom_telemetry_id"] == "telemetry-abc"
    # Missing fields were ensured
    assert parsed["device_id"] == acc.device_id
    assert parsed["notion_user_id"] == acc.user_id
