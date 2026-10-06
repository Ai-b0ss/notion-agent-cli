# notion-agent-cli — agent navigation map

## Core flow
| Concern | Start here | Follow next |
|---|---|---|
| CLI dispatch | `src/notion_agent_cli/cli/__main__.py` | command handlers/imported modules |
| Account/bootstrap | `account.py`, `bootstrap.py` | profile/workspace binding tests |
| Notion inference transport | `provider.py` | `transcript.py`, NDJSON parsing, exceptions |
| Transcript streaming | `transcript.py`, `ndjson.py` | provider and patch-sync tests |
| Agents/persona binding | `agents.py` | account/bootstrap and workspace-binding tests |
| Thread continuation | `thread_state.py` | transcript/provider call sites |
| Profiles | `profile.py` | account paths and CLI commands |
| HTTP wrapper | `serve.py` | provider/client calls |
| Runs/workflows | `runs.py` | distinguish from normal chat/persona path |
| Public types/models | `types.py`, `models.py` | callers + tests |

## Trace rule
For any CLI command trace: argument parsing → selected module → HTTP/provider call → transcript decoding → persisted account/thread state → returned error code/output. For auth issues inspect both account bootstrap and cookie merge behavior.

## Branches and lines
Both branch heads are recorded in `.agent/branch-index.json`. Run `python tools/build_agent_index.py` after checkout and use symbol line numbers from `.agent/local-code-index.json`; never reuse line numbers from another branch.
