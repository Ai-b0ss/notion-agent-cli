# GitHub Account Atlas — private canonical map

> Read this before concluding that prior work does not exist.
>
> This GitHub account is a network of product lineages, proof branches, PR dossiers, issue-based transport logs, CI/evidence surfaces and deployment mirrors. A repository-local Git search is not an account-wide search.

Snapshot: 2026-10-06. Resolve live state before freshness-sensitive decisions.

## Account surfaces

### Owned working repositories

| Repository | Main role | Branches | Pull requests | Issues |
|---|---|---:|---|---|
| `human-1.5` | Human legacy MVP + Human 2.0 restart | 2 | 1 open | 0 |
| `qwen-workspace` | Qwen/Pixel/Free Fabric umbrella workspace | 120 | 33 open / 39 merged / 56 closed-unmerged | 2 open |
| `qwen-free-api` | Qwen proxy/runtime + proof/CI carrier | 275 | 90 open / 19 merged / 25 closed-unmerged | 2 closed |
| `notion-agent-bridge` | Notion/NCM lineage → Windows Agent Bridge / FFBridge | 230 | 78 open / 32 merged / 30 closed-unmerged | 39 open / 3659 closed |
| `kontur` | Kontur product + deployment + AUTOPILOT lines | 103 | 20 open / 3 merged / 4 closed-unmerged | 5 open |
| `ai-mirrors` | private evolved/decomposed AI MIRRORS | 5 | 2 open / 1 merged / 1 closed-unmerged | 0 |
| `free-fabric-ci` | public reusable Free Fabric substrate | 11 | 2 open / 2 merged / 1 closed-unmerged | 3 closed |
| `notion-agent-cli` | Notion agent/session/protocol CLI | 2 | 1 merged | 0 |
| `chatgpt-429-conversation-recovery` | ChatGPT availability/429/stream recovery | 8 | 1 merged | 1 closed |

### Other account-visible repositories

- `Japan-Live/ai_mirrors` — older public monolithic GPT/AI MIRRORS line. The account has admin access. It was created in June 2026 and currently contains a large monolithic `app.py` plus a detailed product README.
- `ostrovok-hackathon-2026/if` — private organization repo for the Ostrovok Hackathon team; currently essentially the base project template.
- `ostrovok-hackathon-2026/project-template` — public base template.

Do not confuse the organizational hackathon `if` with the old short `Ai-b0ss/if` identity seen in earlier account snapshots; that owned path is not currently resolvable.

## Project topology

```text
Japan-Live/ai_mirrors (June public monolith)
           │ same product lineage; current heads do not share visible Git ancestry
           ▼
   Ai-b0ss/ai-mirrors ───────► Hugging Face runtime/source state
           │                    PR #3 is the reconciliation dossier
           └─ decomposed app_engine_v2 / provider_pool / tool_lab line

qwen-free-api  ◄──────────────► qwen-workspace
 proxy/runtime                  orchestration / Pixel / Free Fabric
      │                             │
      │ Kontur QA / Notion carriers │ Free Fabric / GPT-web / Notion work
      ▼                             ▼
   kontur ◄──── AUTOPILOT ─── free-fabric-ci
                                    │
                                    ▼
                         notion-agent-bridge
                         Notion/NCM → Windows/FFBridge/CUA
                                    │
                                    ▼
                           notion-agent-cli

human-1.5 ──► human-2.0-foundation

chatgpt-429-conversation-recovery is mostly standalone. Similar ChatGPT/browser
research elsewhere is not proof of code lineage.
```

## Why Git-only archaeology still misses major work

1. **Open PRs are project dossiers.** The four heaviest repositories currently contain 221 open PRs. Many are frozen proofs, but several preserve substantial unintegrated implementations.
2. **Issue streams can be runtime logs.** `notion-agent-bridge` has 3698 issues; most are transport, benchmark, evidence or recovery records rather than backlog tickets.
3. **PR bodies preserve intent and proof boundaries.** They frequently explain why something was not merged and what remains unproven.
4. **Workflow files encode historical acceptance contracts.** NCM28, FF-WIN/v3, RFGI and CUA epochs are visible in workflows even when code moved.
5. **Tags/releases are stronger historical anchors than branch names.**
6. **External source/deployment stores exist.** AI MIRRORS has had an older public GitHub line, the private GitHub line, and Hugging Face runtime/source state.

Therefore `not in main`, `not at a branch head`, and even `not in this repo's reachable Git history` are insufficient absence tests.

## High-value hidden / unintegrated clusters

### Human

PR #1 (`human-2.0-foundation`) is the benchmark-first Human 2.0 foundation: HumanBench, controller/data contracts, baseline runner, adversarial memory cases, architecture decisions and tests. It is intentionally unmerged pending real free/local-model measurement.

### qwen-workspace

- PR #130 `feat/qwen-standalone-closure-proof`: +10/-35 versus current main. Adds Qwen auth/runtime audits, OpenCode continuation, proxy lifecycle and substantial tests/evidence. Its body explicitly says OPEN / UNMERGED / DO NOT MERGE pending curator evaluation.
- PR #99 `feat/fabric-github-selfhosted-windows-20260829`: historical authenticated Windows transport line.
- PR #86 `fabric/gpt-agent-executor-v1`: full GPT web bridge/probe/patch line.
- The GPT `ci/g*-*` PR sequence is a staged diagnostic lineage, not random branch noise.

### qwen-free-api

There are 90 open PRs; 81 are `ci/*`. This repository became a proof carrier for Qwen runtime behavior and also for Kontur/Notion work.

Do not interpret raw ahead/behind without the PR base. Example: PR #95 is a tiny one-file `express` dependency fix whose base is an old autopilot branch; comparing its inherited head directly against modern main makes it look like a 770-commit feature.

### notion-agent-bridge

This is the densest archaeology surface.

- PR #3834 `worker/seven-pillars-controller-20261004`: open/draft, +18/-31 versus current main. It preserves ordinary-user runtime, desktop/native input, WGC, Office Word/Excel/PowerPoint Copilot, panel controls, artifact verification and large proof sets. Its own body also lists remaining release gates; never flatten this line to simply DONE or ABANDONED.
- PR #3820: standalone technical-debt/bug audit.
- PR #3366: authenticated FlClash API candidate.
- PR #3298: Antigravity cold-start/CDP discovery line.
- Browser/UIA/WGC/Commander/RFGI worker lines are separate historical families.

### Kontur

Open PRs preserve a product evolution chain:
- #11 separates current product from legacy V1–V5.
- #20–27 track accepted visual candidate → state machine → flash continuity → master-frame → proof.
- #32 AUTOPILOT v4.1 state/CAS control plane is +40/-30 versus main and is closely related to public scheduler primitives in `free-fabric-ci`.

### AI MIRRORS

Treat these as distinct truth surfaces:
1. `Japan-Live/ai_mirrors` — older public monolith (June);
2. `Ai-b0ss/ai-mirrors` — private structural migration (August onward);
3. Hugging Face runtime/source state.

Private PR #3 explicitly established that private GitHub was a structural superset of HF at that point but **not a byte-identical mirror**. Reconcile; do not overwrite blindly.

### free-fabric-ci

- PR #1: reproducible cross-Windows/Linux release archive proof.
- PR #2: reusable public scheduler/control-plane contracts (state validation, sticky leases, dependency transitions, provider outcome classification). It aligns closely in timing and design with Kontur AUTOPILOT v4.1.

## notion-agent-bridge Issues = operational database

Snapshot prefix counts:
- FF-AUTO: 1892
- FF-WIN: 1341
- FF-FAST: 122
- FF-RUNNER: 67
- FF-GH: 23
- FF-GH-INBOX: 11
- ASTRA-EVIDENCE-EXPORT: 3

Thematic title hits include Commander 222, Antigravity 201, OmniRouter 95, browser 95, native 57, Astra 51, Excel 34, Notion 33, vision 24, UIA 18 and WGC 11.

These issues record diagnostics, retries, benchmark runs, idempotency, uncertain outcomes, evidence transport and recovery checkpoints. Search them before repeating an old experiment.

## Milestone anchors

- `qwen-free-api`: `v1.0.1`
- `notion-agent-cli`: `v0.1.12-baseline`, `v0.1.13`, proven-live/reconciled/release 0.1.13 tags
- `chatgpt-429-conversation-recovery`: v0.8.0 → v0.8.4 → v0.9.3
- `notion-agent-bridge`: proven 2026-09-07 tags plus GitHub Windows transport v5 RC1/RC2 prereleases

## Mandatory account-wide absence test

Before saying “never implemented”, “no solution exists”, “abandoned”, or designing a replacement:

1. search exact current repo/ref;
2. search all refs and full reachable Git history with `tools/agent_history.py`;
3. inspect the repo's `.agent/github-objects-index.json`;
4. search PR titles **and bodies**;
5. search Issues if that project used Issues as transport/evidence;
6. inspect tags/releases;
7. inspect related repositories from this atlas;
8. inspect deployment/external truth surfaces such as Hugging Face;
9. inspect workflow/evidence files and workflow runs when proof matters;
10. if still absent, inspect local machines, CI artifacts, external storage and handoffs.

Only after this can absence be a supported conclusion.

## Account-level source authority

There is no universal single source of truth.

- Runtime behavior: exact deployed/current source + tests > current docs > historical evidence.
- Product intent: explicit current owner requirements > authoritative product/state docs > implementation > old ideas.
- Historical proof: immutable commit/blob/tag/release/run evidence > contemporaneous PR/issue record > later summary.
- Cross-repo lineage: direct hashes/migration docs > explicit PR descriptions > matching implementation/architecture > naming similarity.

Always state which source class supports a conclusion.

## Limits

This atlas is an index, not a copy of every PR/issue body. Query GitHub when detail is needed.

GitHub Actions are only partially enumerable through the currently available connector. Workflow source files, commit workflow runs, PR references, saved evidence and artifacts remain valid routes.

Uncommitted local work and garbage-collected commits still require the machine/storage/backup where they existed.

## Rule for agents

A repository is a **view into the account**, not necessarily the boundary of the project.

Use a small mandatory bootstrap to find the correct layer, then expand into all available work only when the task requires it.