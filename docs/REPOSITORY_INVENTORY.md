# Repository inventory — notion-agent-cli

Python CLI/library for Notion account, agent, transcript, run and protocol workflows.

This is a structural snapshot for orientation, not a substitute for exact-ref inspection. For current truth resolve `main` at read time; for another ref use the tools below.

## Canonical navigation

1. `AGENTS.md`
2. `docs/AGENT_OPERATING_SYSTEM.md`
3. `docs/AGENT_NAVIGATION.md`
4. `.agent/branch-index.json`
5. `.agent/file-index.json`

## Current main snapshot

Tracked blob files currently visible on `main`: **37**.
Known named branches in the committed branch catalog: **2**.

### Top-level areas by stored bytes

| Area | Files | Bytes |
|---|---:|---:|
| `src` | 16 | 227,111 |
| `tests` | 5 | 23,345 |
| `tools` | 2 | 18,832 |
| `docs` | 2 | 11,884 |
| `README.md` | 1 | 11,497 |
| `.agent` | 3 | 8,223 |
| `AGENTS.md` | 1 | 1,871 |
| `LICENSE` | 1 | 1,066 |
| `pyproject.toml` | 1 | 752 |
| `CLAUDE.md` | 1 | 703 |
| `.cursor` | 1 | 658 |
| `GEMINI.md` | 1 | 588 |
| `.github` | 1 | 574 |
| `.gitignore` | 1 | 280 |

### File roles

| Role | Files |
|---|---:|
| `library_runtime` | 14 |
| `agent_tooling` | 12 |
| `test` | 5 |
| `documentation` | 2 |
| `cli_entry` | 2 |
| `project_file` | 1 |
| `packaging` | 1 |

### Largest tracked files

Large files are not automatically bad; this table tells an agent where blind full-file reading is likely wasteful.

| File | Bytes | Role |
|---|---:|---|
| `src/notion_agent_cli/cli/__main__.py` | 79,804 | `cli_entry` |
| `src/notion_agent_cli/provider.py` | 44,664 | `library_runtime` |
| `tools/agent_history.py` | 14,293 | `agent_tooling` |
| `src/notion_agent_cli/ndjson.py` | 14,230 | `library_runtime` |
| `src/notion_agent_cli/transcript.py` | 13,618 | `library_runtime` |
| `src/notion_agent_cli/bootstrap.py` | 12,809 | `library_runtime` |
| `src/notion_agent_cli/serve.py` | 12,226 | `library_runtime` |
| `src/notion_agent_cli/agents.py` | 11,562 | `library_runtime` |
| `README.md` | 11,497 | `documentation` |
| `docs/AGENT_OPERATING_SYSTEM.md` | 10,413 | `agent_tooling` |
| `tests/test_ndjson_patch_sync.py` | 9,206 | `test` |
| `src/notion_agent_cli/models.py` | 7,236 | `library_runtime` |
| `tests/test_workspace_binding.py` | 7,195 | `test` |
| `src/notion_agent_cli/account.py` | 6,909 | `library_runtime` |
| `src/notion_agent_cli/profile.py` | 6,581 | `library_runtime` |

## Branch families

Branch prefixes are navigational hints, not authority. Exact names and non-main head SHAs are in `.agent/branch-index.json`.

| Family | Branches |
|---|---:|
| `main` | 1 |
| `reconcile` | 1 |

## How to reach all work

Current branch tips:
```bash
python tools/agent_history.py branches
python tools/agent_history.py find-text "term"
python tools/agent_history.py find-path "**/name*"
```

Deleted/older committed work:
```bash
python tools/agent_history.py find-history-text "term"
python tools/agent_history.py find-history-path "**/name*"
```

Candidate branch context:
```bash
python tools/agent_history.py branch-info "<branch>"
```

Exact file/symbol/line index for any ref:
```bash
python tools/build_agent_index.py --ref "<branch-or-SHA>"
```

## Interpretation rule

Do not treat this inventory, a branch name, or a README statement as proof of runtime behavior. Trace the exact ref through code, tests, state/configuration and relevant evidence. When old work is found, determine why it diverged or disappeared before reusing it.
