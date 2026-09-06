"""Regression tests for client-hint platform mapping across OS user-agents."""
from __future__ import annotations

from notion_agent_cli.account import NotionAccount
from notion_agent_cli.provider import _sec_ch_ua_platform, build_headers


def _synthetic_account_with_ua(ua: str) -> NotionAccount:
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
        user_agent=ua,
    )


def test_sec_ch_ua_platform_windows() -> None:
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    assert _sec_ch_ua_platform(ua) == '"Windows"'


def test_sec_ch_ua_platform_macos() -> None:
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
    assert _sec_ch_ua_platform(ua) == '"macOS"'


def test_sec_ch_ua_platform_linux() -> None:
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    assert _sec_ch_ua_platform(ua) == '"Linux"'


def test_sec_ch_ua_platform_fallback() -> None:
    assert _sec_ch_ua_platform("") == '"macOS"'
    assert _sec_ch_ua_platform("CustomBot/1.0") == '"macOS"'


def test_build_headers_reflects_platform_hint() -> None:
    win_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    acc = _synthetic_account_with_ua(win_ua)
    headers = build_headers(acc)
    assert headers["sec-ch-ua-platform"] == '"Windows"'

    mac_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    acc_mac = _synthetic_account_with_ua(mac_ua)
    headers_mac = build_headers(acc_mac)
    assert headers_mac["sec-ch-ua-platform"] == '"macOS"'
