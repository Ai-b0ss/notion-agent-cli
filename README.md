> **Проект заморожен 30 октября 2026 года.** Разработка остановлена, работа с
> Notion AI живьём не подтверждена. Описание ниже написано до заморозки и при
> заморозке не перепроверялось.
# notion-agent-cli

> 把你的 Notion ✦ AI / Custom Agent 变成一条 shell 命令。

A small Python CLI + library that talks **directly** to Notion's internal
`POST /api/v3/runInferenceTranscript` endpoint using a `token_v2` cookie
copied from a logged-in browser session. No `notion_manager` Go proxy, no
account pool — just your own session.

The conversations show up in Notion's ✦ AI chat panel under whichever
Custom Agent persona you bind (e.g. Jarvis), so you can switch between
talking to your agent from Notion's UI and from the shell.

## Status

**v0.1.0 — first tagged release.** The library is live-validated against
Notion's real endpoint and adopted by at least one downstream project
([NotionAgents](https://github.com/chenyqthu/NotionAgents) uses
`NotionAgentClient` as its inference backend). See
[`docs/STATUS.md`](docs/STATUS.md) for the full live-test ledger and
[`docs/ROADMAP.md`](docs/ROADMAP.md) for what's still planned.

## Install

```bash
pipx install notion-agent-cli      # recommended — isolated venv, one-line upgrade
# or
pip install notion-agent-cli       # if you don't use pipx
```

For the optional FastAPI HTTP wrapper (`notion-agent serve`):

```bash
pipx install 'notion-agent-cli[serve]'
```

For local development from a clone, `pip install -e ".[dev]"`. The
release flow is in [`docs/RELEASING.md`](docs/RELEASING.md).

## Quickstart

```bash
# One-shot setup: paste your `token_v2` cookie value from DevTools
# (Application → Cookies → notion.so → token_v2 row → "Value" column).
# The CLI hits /loadUserContent with the token alone, reads your
# user_id back from the response, and picks the (only) workspace.
notion-agent init --token-v2 "v03%3A..."

# Multiple workspaces? Disambiguate with --space-name "TP-Link"
# (case-insensitive) or --space-domain. The first `init` will exit
# with a list of choices and a ready-to-copy rerun line.

# Chat (returns the full reply after streaming completes).
notion-agent chat "用一句话确认你在线。"
```

Prefer keeping the token out of shell history? Either of these works:

```bash
# Token from stdin — never lands in argv / `ps` output:
pbpaste | notion-agent init --token-v2 -

# Or pipe a full document.cookie string (DevTools → Application →
# Cookies → notion.so → right-click → "Copy all as ...") so init
# also pre-fills notion_user_id / notion_browser_id:
pbpaste | notion-agent init --cookie -
```

For Jarvis-style custom agent binding (so threads surface in the ✦ AI
chat panel under your agent name), `agents list` now resolves the name,
icon, and the **`agent_page_id`** (the persistent_instructions_page
UUID) for every Custom Agent in the workspace — copy that value
straight into `--agent-page-id`:

```bash
# Find your agent — `name`, `icon`, `agent_page_id` all populated:
notion-agent agents list --json | jq '.[] | {name, icon, agent_page_id}'

# Bind it. `init` reverse-resolves --agent-page-id against the agents
# list; if it matches a registered Custom Agent, agent_name is
# auto-filled (so passing --agent-name is optional):
notion-agent init --token-v2 "v03%3A..." \
                  --agent-page-id 2e115375-830d-8184-bf4d-f427d847c6bc
```

> `--agent-name` alone is still **not enough** — `init` records the
> binding by `agent_page_id`. The warning fires if only the name is
> passed.

`--agent-page-id` accepts two semantically distinct kinds of UUID:

| Source | What it is | `chat --json` reports |
|---|---|---|
| `agents list[].agent_page_id` | A workflow-registered Custom Agent's `instructions.id` | `binding_mode: "persona_overlay"` — main ✦ AI runtime overlaid with the Custom Agent's persona. |
| Any other Notion page UUID | Free-form steering page (e.g. a notes index) | `binding_mode: "free_form_steering"` — main ✦ AI runtime steered by the page as system prompt. |

In both modes, `surface="custom_agent"` and the call still runs on
the main ✦ AI runtime — `--agent-page-id` only overlays the
identity (system prompt). It does **not** invoke the Custom
Agent's independent workflow / workers / credit; that requires a
separate `runs` API (planned). See [`docs/AGENTS.md`](docs/AGENTS.md)
for the full four-axis breakdown (surface / identity / runtime /
workflow record).

If you don't know which agent matches a task, `notion-agent agents
route "<task description>"` ranks agents by keyword overlap between
the query and each agent's `name + description`:

```bash
notion-agent agents route "处理邮件" --json
# {"best_match": {"name": "Email Agent", "agent_page_id": "...", "score": 1.2}, ...}
```

Debug: `notion-agent agents inspect <id> [--table workflow]` dumps the
raw `syncRecordValuesMain` response. Use it to investigate unfamiliar
Notion record types without dropping into Python. ACL-only responses
(`{"role":"editor"}`) signal an id-space mismatch — try `--table bot`
or `block` to locate the record's actual table.

## CLI surface

```text
notion-agent init     Bootstrap notion_account.json from a token_v2 cookie.
notion-agent chat     Send one prompt, print the reply (text / --json / --stream / --ndjson).
notion-agent doctor   Validate the account file and ping /loadUserContent.
notion-agent models   refresh — pull the current alias→Notion-id map.
notion-agent agents   list    — custom agents in the bound workspace.
notion-agent agents   route   — best-matching agent for a task description.
notion-agent agents   inspect — debug: raw syncRecordValuesMain dump.
notion-agent threads  list    — recent chat threads (filter by --agent).
notion-agent profile  list / current / use <name> / migrate <name>
notion-agent serve    Local FastAPI server (optional [serve] extra).
```

Run `notion-agent <sub> --help` for flag details. Every subcommand
accepts `--account PATH` to point at a non-default credential file.

## Continuation (multi-turn chats)

`chat` saves per-thread continuation state under
`~/.notionagents/threads/<thread-id>.json` after every successful turn,
so the next turn can be a follow-up in the same chat-panel thread:

```bash
# Turn 1 — capture the thread id.
THREAD=$(notion-agent chat --json "summarize my day so far" | jq -r .thread_id)

# Turn 2 — reuse it.
notion-agent chat --thread-id "$THREAD" "now translate it to chinese"
```

The thread's model is locked to whatever turn 1 chose — passing
`--model` on a `--thread-id` continuation is silently ignored, since
mid-thread model switches occasionally make Notion reject the partial
transcript.

## Multi-workspace profiles

Run `notion-agent init` once per workspace into a named profile file,
then swap between them with `profile use`:

```bash
notion-agent init --cookie "..." --account ~/.notionagents/tplink.json
notion-agent init --cookie "..." --account ~/.notionagents/personal.json
notion-agent profile use tplink   # symlinks notion_account.json → tplink.json
notion-agent profile current      # prints "tplink"
notion-agent profile list         # both, * marks active
```

If you started before profiles existed, `profile migrate <name>` renames
your existing `notion_account.json` into a named profile and replaces
the original with a symlink — non-destructive, no re-init required.

## Local HTTP server

`notion-agent serve` wraps the CLI in a small FastAPI app for
orchestrators (n8n, Make, internal Go services) that prefer HTTP over
shell-out. Install with the `[serve]` extra:

```bash
pip install -e ".[serve]"
notion-agent serve --host 127.0.0.1 --port 8000

# In another shell:
curl -sN -X POST localhost:8000/chat \
     -H 'content-type: application/json' \
     -d '{"prompt":"hi","stream":true}'   # SSE; data: {"text":"..."} per chunk
curl -s localhost:8000/healthz
curl -s localhost:8000/agents
```

Endpoints: `POST /chat` (blocking JSON or SSE), `GET /healthz` (doctor's
checks, 200 / 503), `GET /agents`, `GET /threads`. Error codes match
the library's [`ErrorCode`](src/notion_agent_cli/exceptions.py) taxonomy
so callers branch on `code` without parsing messages.

## Calling this from an AI agent

Two paths, pick the one that matches your runtime:

- **Claude Code** — the repo ships a skill at
  [`.claude/skills/notion-agent/`](.claude/skills/notion-agent/). Open
  this repo (or a downstream project that depends on the CLI) and the
  skill auto-loads via its frontmatter trigger phrases ("ask Jarvis",
  "Notion AI", "via the chat panel").
- **Anything else** (Codex, Gemini, openclaw, your own orchestrator) —
  read [`docs/AGENTS.md`](docs/AGENTS.md). It has a paste-ready
  system-prompt snippet at the bottom covering the CLI contract,
  preflight, error codes, and safety rules in ~40 lines.

Both paths shell out to the same `notion-agent` binary — make sure it
is on `$PATH` for whatever runtime you use.

Exit codes let a wrapper branch without scraping text: **75** = Notion's
anti-automation trust rule tripped (back off ~5 min and retry serially —
never hammer or parallelize), **77** = auth/credential failure (re-run
`init`), any other failure = `1`. With `--json`, a failed `chat` also
writes a `{"error": {code, subtype, retryable, retry_after_seconds, …}}`
object to stdout (no `"error"` key on success). Full table in
[`docs/AGENTS.md`](docs/AGENTS.md#error-handling).

## Why this exists

Notion's Custom Agents went paid in May 2026 ($10 / 1k credits,
30–60 credits per run, Business+ only). Their built-in ✦ AI chat is
free for any Plus seat but only addressable from the UI — not from a
cron job, a webhook, or a shell pipe. This CLI bridges that gap by
mirroring exactly what the SPA sends, so you get the same
free-quota model from `bash` / `python` / wherever.

Reverse-engineering notes + the captured chat-panel traffic that this
implementation is built against live in
[`docs/01-notion-chat-protocol.md`](docs/01-notion-chat-protocol.md).

## Library use

```python
import asyncio
from notion_agent_cli import NotionAgentClient

async def main():
    client = NotionAgentClient("~/.notionagents/notion_account.json")
    try:
        resp = await client.complete(prompt="今天周几？")
        print(resp.text)
        print(f"usage: in={resp.usage.input_tokens} out={resp.usage.output_tokens}")

        # Reuse the thread for a follow-up:
        followup = await client.complete(
            prompt="and yesterday?", thread_id=resp.thread_id,
        )
        print(followup.text)
    finally:
        await client.aclose()

asyncio.run(main())
```

Async streaming consumers can pass `on_text_delta=` (sync) or
`on_text_delta_async=` (coroutine, awaited per chunk — used by the
FastAPI SSE branch). For raw NDJSON passthrough use
`client.stream_lines(...)`.

The public surface kept stable across v0.1: `NotionAgentClient`,
`NotionAgentError`, `ChatResponse`, `TokenUsage`, `ErrorCode`. Sub-modules
(`transcript`, `ndjson`, `account`, `models`, `profile`, `serve`) are
importable but their internals can shift between minor releases.

## License

MIT. See [`LICENSE`](LICENSE).