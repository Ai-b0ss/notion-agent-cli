<!-- ACCOUNT_WIDE_BOOTSTRAP_V1 -->
## Account-wide orientation — mandatory

Before every substantial repository task, also read:

1. `docs/ACCOUNT_ATLAS.md` — private cross-repository topology, hidden work clusters and absence-test protocol.
2. `docs/IDEA_LINEAGES.md` — cross-repository system/idea lifetimes and epoch transitions.
3. `.agent/account-index.json` — machine-readable account/repository graph snapshot.
4. `.agent/idea-lineages.json` — machine-readable lineage IDs, aliases, key objects and evidence boundaries.
5. `.agent/github-objects-index.json` — this repository's PR/issue/workflow/tag archaeology.
6. `.agent/pr-ledger.json` — complete all-state PR archaeology (open, merged, and closed-unmerged) with real base/head SHAs. Read it whenever prior, abandoned, superseded, migrated, or historical PR work could matter.
7. `.agent/tag-release-index.json` — exact tag/release archaeology, including terminal tag targets and release-asset digests. Read it when a version, release, accepted/proven baseline, handoff archive, or historical artifact may matter.

These are navigation snapshots, not live authority: re-resolve current GitHub state when freshness matters. Any SHA, branch head, PR state, counter, test total, or "current status" written in README/docs is evidence for its recorded snapshot only unless it matches the live object you just resolved.

Reading the atlas and lineage map is mandatory; exhaustively searching every other repository is not. When a task names a system/idea, resolve its lineage ID and epoch before assuming the current repository is the project boundary. Expand account-wide archaeology when the task may overlap prior, abandoned, migrated, cross-repo or externally deployed work.

---

<!-- AGENT_BOOTSTRAP_V2 -->
# READ THIS FIRST — mandatory repository bootstrap

For every substantial task in this repository, **before designing or editing**:

1. Read [docs/AGENT_OPERATING_SYSTEM.md](docs/AGENT_OPERATING_SYSTEM.md) — this is the all-work recovery and source-authority contract.
2. Read [docs/AGENT_NAVIGATION.md](docs/AGENT_NAVIGATION.md) — repository-specific architecture map.
3. Pin the exact branch and commit; do not reason from a branch name alone.
4. If prior/abandoned/forgotten work may exist, search branch tips **and full reachable Git history** with `tools/agent_history.py` before implementing a replacement.
5. For exact code locations on any ref, run `python tools/build_agent_index.py --ref "<branch-or-SHA>"`.
6. Never conclude "this was never implemented" from `main` alone.

The navigation files in `main` are deliberately external to old evidence branches so those historical heads remain immutable.

---

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