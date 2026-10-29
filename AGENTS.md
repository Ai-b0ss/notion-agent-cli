# notion-agent-cli

Python CLI and library for Notion's internal web endpoints, using the owner's authenticated browser session. It supports account/workspace setup, AI chat and transcript streaming, persona binding, thread continuation, profiles, and an optional HTTP server.

## Code map

- `src/notion_agent_cli/cli/__main__.py`: CLI dispatch and command handlers.
- `src/notion_agent_cli/account.py`, `src/notion_agent_cli/bootstrap.py`: credentials, cookie merging, workspace discovery and binding.
- `src/notion_agent_cli/provider.py`: inference transport and client calls.
- `src/notion_agent_cli/transcript.py`, `src/notion_agent_cli/ndjson.py`: request transcripts and streamed response parsing.
- `src/notion_agent_cli/agents.py`: agent discovery and persona binding.
- `src/notion_agent_cli/thread_state.py`, `src/notion_agent_cli/profile.py`: continuation state and account profiles.
- `src/notion_agent_cli/serve.py`, `src/notion_agent_cli/runs.py`: optional HTTP wrapper and separate workflow/run operations.
- `src/notion_agent_cli/types.py`, `src/notion_agent_cli/models.py`, `src/notion_agent_cli/exceptions.py`: public types, model aliases and errors.
- `tests/`: offline regression tests; `pyproject.toml`: dependencies and CLI entry point.

## Local checks

This checkout has no CI workflows or test/check commands in README. With the declared development dependencies already available, use PowerShell:

```powershell
$env:PYTHONPATH = 'src'
python -m pytest -q -p no:cacheprovider
python -m ruff check --no-cache src tests
```

## Rules

`main` is the integration branch.
- Inspect related tests before changing protocol, cookies/accounts, transcripts, workspace binding or continuation behavior.
- Keep observed transport/protocol behavior separate from assumptions.
- Never commit `token_v2`, cookies or account files.
- Claim a Custom Agent workflow invocation only when that workflow ran; the main AI runtime/persona overlay path does not establish this.
