# Account idea lineages — cross-repository archaeology

> This file is the idea/system layer above `docs/ACCOUNT_ATLAS.md`.
>
> A repository, branch, PR, workflow or issue stream is only a surface. The unit of historical navigation is the **lineage**: one idea/system across migrations, rewrites, transports, proof carriers and deployment stores.

Snapshot: 2026-10-06. Re-resolve live PR/branch/workflow state before freshness-sensitive decisions.

## Mandatory use

When a task names a system, feature family or historical idea:

1. Find its `lineage_id` in `.agent/idea-lineages.json`.
2. Read the lineage chronology before choosing a repository.
3. Inspect the listed key PRs/commits/workflows/issues using their **real base/head**, not head-vs-main alone.
4. Distinguish implementation state from proof state and deployment state.
5. Search aliases and predecessor names before concluding the idea is absent.
6. If two records disagree, prefer immutable exact-head evidence and current object state over stale PR-body prose.

A lineage can legitimately have several simultaneous truth surfaces. Do not collapse them into a single “latest repo”.

---

## L1 — Human 1.5 → Human 2.0

**Lineage ID:** `human-dialogue-platform`

- Legacy product/runtime remains on `Ai-b0ss/human-1.5/main`.
- PR #1 (`human-2.0-foundation`) is an intentional restart, not a small feature branch.
- It introduces HumanBench, policy/data contracts, a strict controller, adversarial memory cases and benchmark tooling.
- The branch is intentionally **open / draft / unmerged** pending real free/local-model baseline-vs-controller measurement.

Guard: do not infer that legacy FAI/IGS is the intended Human 2.0 architecture, and do not call PR #1 abandoned merely because it is unmerged.

Primary entry points: `human-1.5#1`, `human2/README.md`, `human2/STATUS.md`.

---

## L2 — AI MIRRORS public monolith → private decomposition → Hugging Face runtime

**Lineage ID:** `ai-mirrors-runtime`

Truth surfaces:

1. `Japan-Live/ai_mirrors` — June public monolith.
2. `Ai-b0ss/ai-mirrors` — later private decomposed line.
3. Hugging Face — deployment/runtime source surface.

Private PR #3 is the reconciliation dossier. It established that GitHub was a structural superset of the live HF tree at that point, but **not byte-identical**. 375/382 HF files matched; 7 shared paths differed and 8 service files existed only on GitHub.

Guard: never overwrite one surface with another just because one is “newer”. Reconcile exact files, runtime bundle metadata and deployment provenance first.

Primary entry point: `Ai-b0ss/ai-mirrors#3`.

---

## L3 — Free Fabric core and provider-independent execution

**Lineage ID:** `free-fabric-core`

This is the longest cross-repo systems lineage in the account.

### Epoch A — task/lease/fence kernel
- `qwen-workspace#36`: durable TaskSpec, generation/lease/fence, stale-result rejection, UNCERTAIN and resource registry.

### Epoch B — canonical v1
- `qwen-workspace#61`: canonical composition; Qwen live bounded path; independent verification and artifact contracts.
- `qwen-free-api#107`: scoped Qwen Agent Execution executor.

### Epoch C — provider-generic fabric
- `qwen-workspace#91`: provider-generic execution target registry and journal-bound result verification.
- Notion provider/worker proofs span `notion-agent-bridge` and later `qwen-workspace#116`.

### Epoch D — distributed/PC-independent substrate
- `qwen-workspace#121`: durable distributed control plane, tool broker and heterogeneous compute.
- `qwen-workspace#124`: full-system canon, PC-independent continuation and explicit separation of AI/model routing from compute/resource routing.

### Epoch E — exact-head external acceptance
- `qwen-workspace#129`: genuine two-worker migration, immutable evidence, stale-fence proof, verifier/worker/owner isolation.
- Public proof carrier: `free-fabric-ci`.

PR #129 explicitly says **the infrastructure proof phase is accepted while the whole product/system is not done**.

Guard: Free Fabric is not equivalent to Qwen, Notion, Kontur or the public CI repo. Those are providers, consumers, proof carriers or adjacent control planes.

---

## L4 — GPT web / ChatGPT Agent Execution branch of Free Fabric

**Lineage ID:** `gpt-web-agent-execution`

Chronology in `qwen-workspace`:
- PRs #6–#13: auth/bridge/browser/Circle diagnostic sequence.
- PR #86: bounded ChatGPT web Agent Execution adapter.
- PR #87: webhook entry.
- PR #88: provider-free live-canary harness.

PR #86 is **open / draft / unmerged** and deliberately limits claims to chat/text generation; it does not claim general tool calling or OpenAI-compatible API parity.

Guard: do not treat the diagnostic PR chain as random CI noise; equally, do not infer a production-ready GPT provider from its existence.

---

## L5 — Qwen standalone / OpenCode continuation

**Lineage ID:** `qwen-standalone`

Surfaces:
- `qwen-free-api`: local proxy/runtime and session/account behavior.
- `qwen-workspace`: system-level Qwen adapter, auth and Free Fabric integration.

Key object: `qwen-workspace#130` (`feat/qwen-standalone-closure-proof`).

Current recorded state: **OPEN / UNMERGED / DO NOT MERGE** pending curator evaluation. Its live audit reached upstream auth but the stored Qwen pool was expired; direct and OpenCode live continuation therefore remain unproven on that head.

Guard: do not turn an auth-pool/environment blocker into either “system broken” or “feature proven”.

---

## L6 — Notion protocol / NCM lineage

**Lineage ID:** `notion-ncm-protocol`

- Early NCM28 exact-source/guarded-parent sequence: `notion-agent-bridge#1–#7`.
- Later bridge integration/consolidation includes PR #88 and PR #131.
- `notion-agent-cli#1` reconciles 0.1.13 protocol semantics, workspace binding, Windows UTF-8 and durable recovery; merged with 24/24 unit tests plus isolated package/live inference verification.

NCM28 is also the historical root of the Windows-control lineage below. This is intentional overlap: one lineage tracks Notion/protocol provenance, the other tracks desktop-control evolution.

Guard: frozen NCM28 exact-source gates are provenance evidence; passing them does not by itself prove a modern FFBridge/Seven-Pillars candidate.

---

## L7 — Windows control: NCM28 → FF-WIN → Bridge v3 → CUA → RFGI → GitHub v5 → FFBridge → Seven Pillars

**Lineage ID:** `windows-agent-control`

This is the densest lineage and must be navigated by epoch.

### 1. NCM28 / exact-source provenance — Aug 16–18
- PR #1 exact guarded-parent remote gate (merged).
- PR #7 native Windows candidate (open/draft) preserves the remaining native acceptance history.

### 2. FF Windows desktop product — Sep 1
- PR #86: supervised Windows launcher v1; one-command bootstrap/release/cleanup, local HTTP hardening and F51 acceptance work.

### 3. Bridge v3 — Sep 10
- PR #461: embedded-Python startup/import correction (merged).
- OmniRouter work remains a separate isolated branch, notably PR #395.

### 4. CUA semantic/safety kernel — Sep 13–18
- PR #737: browser semantic sidecar prototype.
- PRs #738–#755: native/UIA, human-input arbiter, capture, browser, WGC and related workers.
- PR #740: integration router/safety kernel. **GitHub metadata says merged**; its body still contains stale “OPEN / DRAFT / UNMERGED” prose. Current object state wins.

### 5. Canonical bridge RC — Sep 22
- PR #1909: safe autorecovery contract, passive defaults, stop tooling and 507-test suite; merged.

### 6. RFGI application discovery — Sep 27
- PR #3239: Electron CDP discovery from app-owned listeners (merged).
- PR #3298: Antigravity cold-start CDP (open/draft; exact guarded-parent remote gate did not execute).
- PR #3366: authenticated FlClash loopback API (open/draft; same infrastructure gate blocker).
- PRs #3393/#3395: Fast recovery line.

### 7. GitHub Windows transport v5 — Sep 30
- PR #3815: reproducible handoff, crash-safe inbox/outbox and live throughput/recovery proof; merged.

### 8. FFBridge verified execution stack — Oct 1–2
- PR #3823: durable outcomes and restricted/background execution proof on a stacked branch; closed unmerged.
- PR #3831: integrates #3821–#3830 into main; merged and bound to verified installed/cloud smoke evidence.

### 9. Seven Pillars / ordinary-user full-access direction — Oct 3–5
- PR #3833: owner requirements and seven pillars; merged.
- PR #3834: current large candidate, open/draft, exact head `4444e96f…` at the recorded proof point.
- Run `37384262241` artifact `ff-seven-pillars-contracts`: 501 tests, 0 failures/errors/skips, 41.284 s. It excludes two owner-desktop tests.
- The expiring Actions artifact has been losslessly archived under `.agent/evidence-index/archive/pr-3834-run-37384262241/` and bound to SHA-256 `2d7cc981…132d`.

Sublineages worth searching independently: `Commander`, `Antigravity`, `FlClash`, `OmniRouter`, `WGC`, `UIA`, `Office/Excel/Word/PowerPoint`, `hidden apps`, `physical input`.

Guard: never call the whole lineage “NCM28”, “Bridge v3”, “CUA” or “Seven Pillars” without identifying the epoch. Never add test counts from overlapping runs.

---

## L8 — AUTOPILOT scheduler/control plane

**Lineage ID:** `autopilot-control-plane`

Two coordinated but not identical surfaces:
- `kontur#32`: private AUTOPILOT v4.1 canonical scheduler state and CAS control plane.
- `free-fabric-ci#2`: public reusable scheduler/control-plane contracts.

Shared concepts include authoritative machine state, compare-and-swap updates, sticky leases, dependency-aware transitions and provider outcome classification.

`qwen-workspace#124` explicitly distinguishes the general Free Fabric architecture from the Kontur AUTOPILOT meta-runtime.

Guard: conceptual/architectural pairing is not proof that the two PRs are byte-identical or that one should be merged into the other.

---

## L9 — Kontur product evolution

**Lineage ID:** `kontur-product`

- PR #11 separates the current product line from legacy V1–V5.
- PRs #20–#27 preserve the accepted visual candidate → state machine → flash continuity → master-frame → proof chain.
- PR #32 is AUTOPILOT control-plane work and should be read through the AUTOPILOT lineage, not mistaken for a UI/product feature.

Guard: product design lineage and autonomous scheduler lineage intersect operationally but have different source authority.

---

## L10 — ChatGPT conversation availability / 429 recovery

**Lineage ID:** `chatgpt-conversation-recovery`

Primary repo: `chatgpt-429-conversation-recovery`.

Milestones: tags `v0.8.0` → `v0.8.4` → `v0.9.3`.

This is mostly standalone. Similar ChatGPT/browser experiments in Free Fabric or Windows Bridge are **not evidence of code lineage** unless a direct commit/file migration is found.

Guard: preserve its explicit idempotency/privacy/rate-limit boundaries; do not reinterpret it as a generic rate-limit bypass.

---

---

## L11 — Cross-repository proof-carrier mesh

**Lineage ID:** `proof-carrier-mesh`

The most misleading repository boundary is `qwen-free-api`: at the snapshot it has 90 open PRs, **81 under `ci/*`**. Its own object index classifies three roles:

- Qwen live/offline exact-source and gating laboratory;
- Kontur Chromium/browser QA carrier;
- Notion Stage-B/provider proof carrier.

Examples:
- PRs #29–#85 contain successive Qwen exact-head Linux/Windows failure localization, reliability and gate work. They are largely a diagnostic/proof sequence, not dozens of product features.
- PRs #13–#15 and #27 carried Kontur Chromium/cross-repo QA.
- PR #118 is explicitly a provider-free Notion Stage-B Windows carrier.
- PR #134 is a provider-session preflight carrier.
- PR #95 is the known counterexample where a one-file `express` fix inherits a huge historical base.

Guard: classify the **payload and target system**, not the repository that happened to execute CI. A carrier PR is not ownership transfer of the product.

---

## L12 — Notion Agent matrix → promoted-v3 recovery → Stage-B delivery

**Lineage ID:** `notion-stage-b-delivery`

This is a diagnostic/proof lineage inside the broader Notion/NCM history.

### Epoch A — Agent prompt/matrix/materialization
- PR #8 establishes engineer/owner prompt-mode contract.
- PRs #9–#32 are successive exact Agent pair, materialization, cleanup, fixture and safety-matrix proofs.

### Epoch B — promoted-v3 crash/recovery
- PRs #35–#50 cover promoted installer identity, postwrite crash recovery, absent/staged payload handling and Agent+Core proof.

### Epoch C — Stage-B native Windows delivery
- PRs #51–#77 form a sequential delivery investigation: server integration, Circle routing, same-byte/native proof, CRLF recomposition, object-origin boundaries, preamble/transport diagnostics, prepare traces/classifiers, PYTHONPATH/EOL fixes and final sanitized delivery probes.
- `qwen-free-api#118` is a provider-free carrier for this Stage-B line rather than Qwen product work.

Guard: treat this as a **serial debugging lineage**. Do not count each diagnostic PR as an independent unfinished feature, and never discard later fixes merely because an earlier carrier PR failed.

---

## L13 — Kontur Cloudflare deployment/proof

**Lineage ID:** `kontur-cloudflare-deployment`

Separate deployment history from the visual/product and AUTOPILOT lineages:

- PR #6 — promote isolated Cloudflare staging path.
- PR #7 — prove real staging product API path.
- PR #8 — verify forbidden production targets remain unchanged.
- PR #10 — integrate staging product proof plus production post-check.
- PR #17 — canonical Linux build gate.
- PR #18 — production D1 read-only capability probe.

Guard: a staging/deployment proof is not a product-design authority, and a read-only production capability probe is not permission for production writes.

---

## L14 — Q15 provider-free execution surface

**Lineage ID:** `q15-provider-free-execution`

Open `qwen-workspace` evidence preserves a distinct late-August execution-surface investigation:

- PR #92 — disposable Q15 provider-free execution-surface proof.
- PR #93 — secure SSH execution-surface verification.
- PR #98 — native Circle provider-free execution proof.
- Nearby PR #97 adds a Windows Circle read broker; PR #99 then explores authenticated GitHub self-hosted transport in the broader Free Fabric line.

Guard: Q15 is an execution/proof sublineage, not equivalent to Qwen model-runtime capability and not automatically the canonical Free Fabric transport.


## Cross-lineage rules

- **PR metadata beats stale prose.** A body can describe an earlier draft state; fetch live object state.
- **Base matters.** Never estimate PR size by comparing its head to modern `main` when the PR base is another historical branch.
- **Proof is scoped.** Record exact head, environment and exclusions. “501 green” is not “everything live-proven”.
- **Merged is not deployed.** Check installed/deployed/runtime evidence separately.
- **Closed-unmerged is not worthless.** It may be a stacked branch later integrated elsewhere.
- **Public proof carrier is not the private product.** Reusable public contracts can prove a boundary without containing private source.
- **Names drift.** Search predecessor and successor aliases before declaring absence.

For object-level detail, continue into each repository’s `.agent/github-objects-index.json` and exact PR/issue/workflow evidence.
