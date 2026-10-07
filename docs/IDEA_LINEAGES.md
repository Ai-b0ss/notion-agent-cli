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

Legacy product/runtime remains on `Ai-b0ss/human/main`. PR #1 / branch `human-2.0-foundation` is an intentional restart and remains **open / draft / unmerged**, but it has advanced far beyond its original foundation PR body.

### Epoch A — benchmark-first foundation
- HumanBench v0, policy/data contracts, strict controller, adversarial memory cases and benchmark tooling.
- Early PR-body proof recorded 25/25 local tests and deliberately postponed real free/local-model measurement.

### Epoch B — measured memory architecture
Current branch evidence now includes:
- real GLM-5.3 HumanBench decisions rescored **30/30** on frozen v0;
- RetrievalBench controls: lexical **25/30**, SQLite + multilingual-E5 **29/30**, Mem0 OSS **29/30**, Graphiti flat retrieval **28/30**;
- selected MVP backend: Human SQLite + local multilingual-E5, with zero forbidden-memory leakage on the selected benchmark;
- frozen MemoryExtractBench v1, AnswerBench v0, MemoryLifecycleBench v1 (**17/17 deterministic**), held-out AnswerBench and blind PairwiseEval methodology;
- end-to-end extract -> guarded write -> semantic retrieve -> controller -> final-answer path plus privacy, tracing, storage-recovery and bounded-context contracts.

### Epoch C — durable personal continuity and provider routing
The latest 12 commits after historical head `f0191c7…` add provider quota awareness/doctor/pool behavior and regressions for:
- cross-conversation durable recall;
- cross-session correction/supersession;
- project-scope and cross-user isolation;
- memory-grounded recall fidelity;
- one-turn preference override;
- conflicting durable preferences.

Current live head at the 2026-10-07 refresh is `31d9408a6d8552401e93e0bedb2cd274909c489d`:
- PR #1: 111 commits, 185 changed files;
- GitHub Actions `Human 2.0 CI` run `37555589776`: **success**.
- Current branch docs report a 387/387 local suite on Python 3.12 and 3.13; README also mentions a later 424-test local branch suite before matrix verification. Treat those as separate recorded claims until tied to one exact run rather than adding them together.

Remaining measured-product boundary: live MemoryExtractBench v1, AnswerBench v0, held-out AnswerBench and PairwiseEval are still incomplete. No UI rewrite should be inferred complete.

Guard: PR-body prose is stale relative to the branch. Do not claim Human 2.0 is still waiting for its first real free/local model probe. Equally, do not treat benchmark and local-runtime progress as a merged/released Human 2.0 product.

Primary entry points: `human#1`, `human2/STATUS.md`, `human2/README.md`, `human2/EVALUATION.md`, `human2/FREE_INFERENCE_AUDIT.md`.

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
- Notion provider/worker proofs span `windows-agent-bridge` and later `qwen-workspace#116`.

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
- `qwen-free-api`: local proxy/runtime, session/account behavior, portable launch and the densest runtime proof ladder.
- `qwen-workspace`: system-level Qwen adapter/auth integration and the later standalone-closure dossier.

### Epoch A — encrypted runtime-state preflight
- `qwen-free-api#6`: verifies the existing encrypted runtime archive can be hydrated/decrypted on a runner without printing secrets and **without calling Qwen**.

### Epoch B — exact-head reliability convergence
The large `ci/*` family is a serial proof ladder rather than dozens of product features. Representative anchors:
- #51: exact `47d9` QWEN_CORE recovery proof.
- #60: exact `a658` Core + Reliability sync.
- #69: exact `f24` session/restart gate after CRLF portability repair.
- #78: exact `5ed` session durability on Linux and native Windows.
- #84: exact `ada1237` QWEN_RELIABILITY proof.

These PRs are mostly config/harness carriers restoring exact product bytes. **DO NOT MERGE** is often an evidence classification, not an abandoned feature label.

### Epoch C — bounded live acceptance
- #92: bounded live acceptance on exact `ada1237`: OpenCode tool-result continuation, same-session restart/state, controlled legitimate account failover and one sparse soak.
- #98: successor live acceptance on exact `c1` after clean install/server/full Linux/native-Windows gates.

Live acceptance is stronger than provider-free CI, but it remains scoped to the exact product revision and the calls authorized by that carrier.

### Epoch D — product safety correction
- #99 is **merged**: suppresses an immediate successful duplicate tool replay so a mutating tool is not blindly executed twice.
- Its own evidence explicitly says multi-round tools were still unstable afterward. This is a safety fix, not proof that the whole tool loop became healthy.

### Epoch E — OpenCode execution-witness / harness diagnosis
- #104–#105: source-verified OpenCode execution witness and session-identity repair.
- #110–#112: least-tool pin repair and continuation witnesses.
- #116, #119–#121: delivery/stage-localization/inner-HARNESS diagnostics.

Treat this as one evolving evidence apparatus. A failed harness stage is not automatically a Qwen-model failure, and a carrier repair is not automatically a product-code change.

### Epoch F — portable Windows standalone release
- #123 is **merged** and proves a provider-free Windows release path: `QWEN_START.cmd`, clean release-ZIP extraction, dependency bootstrap, real local `server.js` + `/healthz`, cleanup and exact-head Ubuntu/Windows CI.
- Exact recorded artifact: `qwen-free-api-windows-d363fa492589b09f5aaa81c454f0c463ee81bdc9`, artifact id `9798030182`, digest `sha256:1c191c08e799e3786e6dba68724236dfb3827f3aaaffd03ffcae8bc628cdafea`.

This proves packaging/launch/runtime health **without** proving an authenticated live Qwen inference.

### Epoch G — later standalone closure dossier
- `qwen-workspace#130` remains **OPEN / UNMERGED / DO NOT MERGE** pending curator evaluation.
- Its live audit reached upstream auth, but the stored Qwen pool was expired; direct and OpenCode live continuation therefore remain unproven on that head.

Guard: keep four states separate: provider-free runtime reliability, live-provider capability, merged product fixes, and carrier/harness evidence. Do not turn an auth-pool/environment blocker into either “system broken” or “feature proven”.

---

## L6 — Notion protocol / NCM lineage

**Lineage ID:** `notion-ncm-protocol`

- Early NCM28 exact-source/guarded-parent sequence: `windows-agent-bridge#1–#7`.
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

### 9. Seven Pillars / ordinary-user full-access direction — Oct 3 onward
- PR #3833: owner requirements and seven pillars; merged.
- PR #3834: large continuation candidate, still **open / draft / unmerged**.

Historical exact proof point:
- head `4444e96fb2ead032083f144de0aa7e93c21b5171`;
- run `37384262241`, artifact `ff-seven-pillars-contracts`: **501/501**, 0 failures/errors/skips, 41.284 s;
- two owner-desktop tests excluded;
- lossless archive: `.agent/evidence-index/archive/pr-3834-run-37384262241/`, ZIP SHA-256 `2d7cc981…132d`.

Continuation after that proof point adds real Cursor HTTP/durable-outcome work, native crash/process-tree recovery, cold/native Office workflows, portable ZIP/Drive/install evidence, UTF-8 installation-path repair and bounded local startup recovery. At the 2026-10-07 refresh:
- live head: `6d67d762bd976ab0118ea0e30a235f3789fdfa8e`;
- PR #3834: 30 commits, 164 changed files, +22,061 / -358;
- three exact-head workflows are green: Windows product gate, FF Transport Contract and guarded-parent exact-source gate;
- exact-head Seven Pillars isolated-Windows run `37554211082` is **red: 568 passed / 1 failed / 0 errors / 0 skipped**. The sole failure is `test_real_candidate_http_durable_outcome_and_process_tree_cleanup`.
- its artifact is losslessly archived under `.agent/evidence-index/archive/pr-3834-run-37554211082/`, ZIP SHA-256 `af77785…fcfb`.

Regression localization matters: immediately preceding head `7f12d118…` passed the same Seven Pillars workflow (run `37553895364`), while `6d67d76…` differs from it only by two report files under `docs/LOCAL_STARTUP_RECOVERY_20261007.*`. Therefore the red run is **not proof of a product-code regression**, but the live head is still not green and the root cause remains unresolved.

Guard: never transfer the 501/501 proof from `4444e96…` to later bytes, and never erase the current 568/569 red gate merely because the immediately previous code-identical head was green.

Sublineages worth searching independently: `Commander`, `Antigravity`, `FlClash`, `OmniRouter`, `WGC`, `UIA`, `Office/Excel/Word/PowerPoint`, `hidden apps`, `physical input`.

Machine-readable facets under `windows-agent-control` preserve the most easily lost subhistories:
- `commander-prelogin-rescue`: Commander cloud-health/direct-control work plus Prelogin/Session 0 rescue (#1607, #1640, #1642, #1660).
- `antigravity-cdp`: UIA/CDP evolution through #744, #3239 and open #3298.
- `flclash-control`: GUI/OCR/Guardian experiments in the issue ledger -> authenticated loopback controller in open #3366.
- `omnirouter-transfer`: isolated source/build/runtime/adoption history around #395 and #461.
- `office-structured-automation`: Excel COM/ROT and broader Office work (#966, #3220, #3834).
- `capture-vision-wgc`: capture/visual grounding/WGC integrity (#741, #749, #751 plus issue-ledger Gen36/RFGI evidence).
- `ffbridge-isolation-durable`: durable outcomes, tool recovery, isolated browser, AppContainer, hidden apps, trusted-shell boundary and browser-to-document recovery (#3823–#3832).
- `fast-network-rescue`: FF-FAST transport, network guardian/supervisor and later Fast recovery (#1984, #3393, #3395 plus the FF-FAST issue stream).

Issue-ledger companion for this lineage: `docs/ISSUE_ARCHAEOLOGY.md` and `.agent/issue-theme-epochs.json`. Use it because many executed experiments exist only or primarily as transport/task Issues.

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

The most misleading repository boundary is `qwen-free-api`: at the snapshot it has 90 open PRs, **81 under `ci/*`**. Its own object index classifies multiple carrier roles rather than 81 unfinished product features.

Qwen carrier subepochs:
- **#29–#94 — exact-head convergence/localization:** successive QWEN_CORE/QWEN_RELIABILITY, Linux/native-Windows and runner-localization proofs around frozen product SHAs.
- **#92/#98 — bounded live acceptance:** live-provider evidence on exact selected revisions, still carried by disposable CI branches.
- **#100–#112 — execution witness/continuation:** dynamic stage, OpenCode witness, least-tool and continuation diagnostics; distinguish harness failure from model/runtime failure.
- **#116/#119–#121 — delivery and inner-HARNESS localization:** evidence transport and wrapper-stage diagnosis, not product features.
- **#122 — Q15 one-live carrier:** belongs semantically to the Q15 execution-surface lineage even though it lives in `qwen-free-api`.
- **#134 — provider-session preflight carrier:** proof infrastructure, not a release.

Other cross-repo carrier roles:
- #13–#15 and #27 carried Kontur Chromium/cross-repo QA.
- #118 is explicitly a provider-free Notion Stage-B Windows carrier.
- #95 remains the canonical base-history warning: a tiny one-file `express` fix inherits an old autopilot base, so head-vs-modern-main wildly overstates its scope.

Guard: classify the **payload and target system**, not the repository that happened to execute CI. A carrier PR is not ownership transfer of the product. A red carrier can mean harness/runner/delivery failure; bind the failure to its exact stage before attributing it to product code.

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

This late-August execution-surface investigation spans both Qwen repositories:

In `qwen-workspace`:
- PR #92 — disposable Q15 provider-free execution-surface proof.
- #93 — secure SSH execution-surface verification.
- #98 — native Circle provider-free execution proof.
- Nearby #97 adds a Windows Circle read broker; #99 explores authenticated GitHub self-hosted transport in the broader Free Fabric line.

In `qwen-free-api`:
- PR #122 — one-live Q15 witness on exact `3b27` release, with the runtime key scoped only to the finite harness invocation and sanitized stage/first-fail evidence.

Guard: Q15 is an execution/proof sublineage, not equivalent to general Qwen model-runtime capability and not automatically the canonical Free Fabric transport. Provider-free Q15 proof and the one-live witness are different evidence classes.

---

## L15 — Astra audit/adjudication state and evidence transport

**Lineage ID:** `astra-audit-state-transport`

This lineage is largely invisible in PR-only archaeology and was recovered from the `windows-agent-bridge` issue ledger.

Observed sampled epoch: **7–8 September 2026**.

- Issues #132–#136: audit bridge health, checkpoints, evidence locators and R01/u51 source/context inspection.
- #210–#211: evidence export and shard transfer.
- #217: cleanup of public transport runner residue.
- #229–#230: durable state inventory and staged state-package transport.

Guard: do not infer that Astra belongs to the Windows Bridge product merely because its transport ran through that repository. The issue ledger is acting as an execution/evidence carrier.

Primary archaeology: `windows-agent-bridge/docs/ISSUE_ARCHAEOLOGY.md`.


---

## L16 — Shared remote-agent / phone-first PR loop foundation

**Lineage ID:** `remote-agent-foundation`

This predates the later Free Fabric architecture and is easy to miss because the same bootstrap was copied into several product repositories on **16–17 August 2026**.

### Epoch A — safe remote CI foundations
- `qwen-workspace#1`, `qwen-free-api#1`, `kontur#1`: repository-specific offline/safe GitHub Actions foundations. The Kontur body explicitly calls this the first base contour for phone-driven branch/PR work.

### Epoch B — common remote task/PR contract
- `qwen-workspace#2`, `qwen-free-api#2`, `kontur#2`, `windows-agent-bridge#5`: a shared remote-task entry and PR contract with live/production work disabled by default.

### Epoch C — autonomous repair-loop smoke
- `kontur#3`: intentionally starts RED, requires the remote agent to read the real Actions failure, repair the marker and wait for a green rerun.

Guard: this is **account-wide remote-development infrastructure**, not product ownership and not proof of later Free Fabric semantics. Do not erase it merely because Free Fabric later became the larger orchestration system.

---

## L17 — Free Fabric Provider Incubator / temporary-provider worker factory

**Lineage ID:** `free-fabric-provider-incubator`

This is a distinct sublineage inside Free Fabric. Its goal is to turn short-lived/free provider opportunities into bounded workers without confusing “API discovered” with “trusted executor”.

### Epoch A — provider lead -> verified candidate
- `qwen-workspace#100`: one-post Provider Incubator, normalized provider lead/manifest, integration-lane and promo-lifetime budgets, fail-closed live smoke.

### Epoch B — OpenCode and tool-capability gates
- #105: verified OpenAI-compatible providers can become isolated OpenCode repo-worker plans.
- #106: a real structured harmless tool-call smoke becomes mandatory before repo execution.

### Epoch C — CodeBuddy / Hy4 lane
- #107: loopback-only authenticated CodeBuddy job adapter.
- #108: one-post CodeBuddy/Hy4 activation with exact model/transcript marker proof.

### Epoch D — isolated worker factory and sealed task flow
- #109 explored the hardened OpenCode worktree/credential-proxy lane but stayed closed-unmerged.
- #111 merged the caller-facing bounded worker factory.
- #112 added exact-agent pull, scoped ticket, fresh worktree, Fabric-created sealed commit and independent-verifier handoff.

### Epoch E — compute substrate expansion
- #113–#115 add and harden the bounded Novita sandbox substrate, including teardown-liveness semantics.
- #118 then incorporates the incubator into the larger autonomous orchestrator/compute-atlas “system finish”.
- #124’s full-system canon explicitly names Provider Incubator as part of the reconstructed architecture.

Guard: provider-free tests, merged adapters or a promo post are **not live provider proof**. Credentialed text/tool smoke and the exact execution lane remain separate evidence gates.

## Cross-lineage rules

- **PR metadata beats stale prose.** A body can describe an earlier draft state; fetch live object state.
- **Base matters.** Never estimate PR size by comparing its head to modern `main` when the PR base is another historical branch.
- **Proof is scoped.** Record exact head, environment and exclusions. “501 green” is not “everything live-proven”.
- **Merged is not deployed.** Check installed/deployed/runtime evidence separately.
- **Closed-unmerged is not worthless.** It may be a stacked branch later integrated elsewhere.
- **Public proof carrier is not the private product.** Reusable public contracts can prove a boundary without containing private source.
- **Names drift.** Search predecessor and successor aliases before declaring absence.

For object-level detail, continue into each repository’s `.agent/github-objects-index.json` and exact PR/issue/workflow evidence.
