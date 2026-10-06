# AGENTS.md — notion-agent-cli

## Mandatory orientation
1. Pin branch/head in `.agent/branch-index.json`.
2. Read `README.md` and `docs/AGENT_NAVIGATION.md`.
3. Use `.agent/file-index.json` for exact file/blobs on `main`.
4. On checkout run `python tools/build_agent_index.py --ref "<branch-or-SHA>"` for line counts and symbol start lines.
5. Read the closest test before changing protocol, cookie/account, transcript, workspace-binding or continuation behavior.

`main` is the integration source of truth. `reconcile/notion-agent-cli-0.1.13` is a reconciliation branch and must be compared explicitly, not assumed newer.

## Protocol caution
This project uses Notion internal web endpoints. Keep transport/protocol observations separate from assumptions. Never commit `token_v2`, cookies or account files. Do not claim a Custom Agent workflow was invoked when only the main AI runtime/persona overlay path was used.