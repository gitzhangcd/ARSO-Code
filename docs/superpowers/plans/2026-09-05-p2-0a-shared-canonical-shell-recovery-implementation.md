# P2.0A Shared Canonical Shell Support Contract Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close P2.0-SC01–SC04 by freezing the shared canonical-shell support contracts required by full B01 canonical models, without copying candidate baseline structures or writing production Python code.

**Architecture:** Add one scoped shared-core Exact V1 companion contract under the global Exact Contract, backed by a source-recovery matrix and field-decision ledger. Keep support types owner-neutral and non-canonical; preserve P0/P1 semantics; update authority/checksum/CI governance; then independently re-review both P2.0A and the blocked P2.0 B01 contract.

**Tech Stack:** Markdown normative contracts, GitHub Actions, SHA-256 source manifest, existing Python/Pytest regression suites.

**Spec:** `docs/superpowers/specs/2026-09-05-p2-0a-shared-canonical-shell-recovery-design.md`

## Global Constraints

- No production Python implementation under `src/design_intelligence/contracts/core/` or `src/design_intelligence/contracts/b01/` in P2.0A.
- `di_contracts_v1/` remains read-only executable evidence, never normative authority.
- P0/P1 frozen types and semantics remain unchanged.
- `ActorType` is an open non-empty typed vocabulary; USER/SERVICE/AGENT/SYSTEM/EXTERNAL are standard recognized codes, not an exhaustive closed enum.
- `TenantScopeType` is exactly `GLOBAL | TENANT`; `GLOBAL` does not imply public access.
- `Provenance` contains canonical source references and opaque external-source references only; no candidate `command_ref:ObjectRef`; `run_ref` remains deferred.
- `ObjectRevision` is a JSON integer >= 1, server-assigned ordering metadata only; lineage remains `parent_refs`.
- Exact V1 remains `FREEZE CANDIDATE`; P2 remains `NOT AUTHORIZED` until P2.0 final Freeze.

---

### Task 1: Freeze the Shared-Core Field Decision Ledger

**Files:**
- Create: `SHARED_CORE_FIELD_DECISION_LEDGER.md`
- Read: `SHARED_CORE_SOURCE_RECOVERY_MATRIX.md`
- Read: `docs/superpowers/specs/2026-09-05-p2-0a-shared-canonical-shell-recovery-design.md`

**Interfaces:**
- Consumes: authoritative global field roles, P0/P1 frozen nominal/reference contracts, candidate structural evidence.
- Produces: one traceable decision table for ActorId, ActorType, ActorRef, TenantId, TenantScopeType, TenantScope, Provenance, ObjectRevision, CanonicalObject, CanonicalRevision, ImmutableFact, and UTC normalization.

- [ ] **Step 1:** Record every shared-core field/type as `DIRECT_FROZEN`, `NORMALIZED_RECOVERY`, `NEW_FREEZE_DECISION`, `DEFERRED`, or `REJECTED`.
- [ ] **Step 2:** State exact wire type, requiredness, cardinality, invariants, and authority rationale for each decision.
- [ ] **Step 3:** Explicitly reject closed candidate `ActorType` exhaustiveness, candidate opaque-ID regex promotion, `Provenance.command_ref:ObjectRef`, and candidate `run_ref:ObjectRef` promotion.
- [ ] **Step 4:** Verify the ledger contains no `TBD`, `TODO`, `FIXME`, no B01 owner fields, no Command/Event identity contract, and no ARSO `RunRecord` structure.
- [ ] **Step 5:** Commit with message `docs: freeze shared-core field decision ledger`.

Expected result:

```text
SC01 ActorRef decision surface      COMPLETE
SC02 TenantScope decision surface   COMPLETE
SC03 Provenance decision surface    COMPLETE
SC04 ObjectRevision decision surface COMPLETE
SPEC_CONFLICT discovered            0
```

---

### Task 2: Create the Scoped Shared Canonical Shell Exact Contract

**Files:**
- Create: `specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md`
- Read: `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
- Read: `SHARED_CORE_FIELD_DECISION_LEDGER.md`

**Interfaces:**
- Consumes: global Exact Contract + P0/P1 frozen semantics + Task 1 decisions.
- Produces: scoped normative contract `DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT V1.0-FC1`.

- [ ] **Step 1:** Define authority scope: subordinate to global `DI-V5-EXACT-CONTRACT`, superior to owner-specific field contracts only for shared-shell support internals.
- [ ] **Step 2:** Freeze ActorId/ActorType/ActorRef exact wire semantics and standard-code meanings.
- [ ] **Step 3:** Freeze TenantId/TenantScopeType/TenantScope exact wire semantics and discriminator invariants.
- [ ] **Step 4:** Freeze Provenance exact wire as `source_refs: Tuple[CanonicalRef]` + `external_source_refs: Tuple[str]`, both required and possibly empty.
- [ ] **Step 5:** Freeze ObjectRevision as positive integer ordering metadata and explicitly forbid lineage/concurrency/identity semantics.
- [ ] **Step 6:** Freeze CanonicalObject, CanonicalRevision, ImmutableFact structural bases and UTC timestamp normalization.
- [ ] **Step 7:** State support/nested types are not Object Registry primitives and get no registry manifest entries.
- [ ] **Step 8:** State exact exclusions: no ObjectId/LogicalId lexical changes, no Command/Event full schema, no OperationalControlState expansion, no B01/B02 owner schemas.
- [ ] **Step 9:** Commit with message `spec: add shared canonical shell Exact V1 contract`.

Expected result:

```text
P2.0-SC01 ActorRef       CLOSED in scoped candidate
P2.0-SC02 TenantScope    CLOSED in scoped candidate
P2.0-SC03 Provenance     CLOSED in scoped candidate
P2.0-SC04 ObjectRevision CLOSED in scoped candidate
```

---

### Task 3: Cross-Spec Consistency Audit

**Files:**
- Create: `SHARED_CORE_CROSS_SPEC_FREEZE_AUDIT.md`
- Read: all eight currently registered normative sources plus the new shared-core candidate contract.

**Interfaces:**
- Consumes: Task 2 contract.
- Produces: criteria-based audit that distinguishes support-type closure from domain-owner semantics.

- [ ] **Step 1:** Audit `ActorRef` against `created_by` role and candidate-only evidence.
- [ ] **Step 2:** Audit `TenantScope` against tenant-isolation text and domain-scope separation.
- [ ] **Step 3:** Audit `Provenance` against Command/Event non-canonical-primitive rule and ARSO ownership.
- [ ] **Step 4:** Audit `ObjectRevision` against `ID != LogicalID != Revision != SchemaVersion` and `parentage = parent_refs`.
- [ ] **Step 5:** Audit CanonicalObject/CanonicalRevision structural fields against global Exact Contract §6.
- [ ] **Step 6:** Record `SPEC_CONFLICT`, remaining blocking shared-core `SPEC_GAP`, and deferred non-P2 requirements separately.
- [ ] **Step 7:** Commit with message `docs: audit shared canonical shell contract`.

Expected result before independent review:

```text
shared-core SPEC_CONFLICT = 0
blocking shared-core field SPEC_GAP = 0
P2.0A preliminary recommendation = READY FOR INDEPENDENT REVIEW
```

---

### Task 4: Register Scoped Authority and Checksum

**Files:**
- Modify: `specs/SPEC_SOURCE_CHECKSUMS.sha256`
- Modify: `SPEC_AUTHORITY.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: exact SHA-256 of Task 2 contract.
- Produces: nine-file normative manifest and explicit authority relation.

- [ ] **Step 1:** Obtain the actual GitHub/runner SHA-256 of `DI_Shared_Canonical_Shell_Exact_V1_Contract.md`; do not hand-invent the digest.
- [ ] **Step 2:** Append it as the ninth normative checksum while preserving the existing eight digests byte-for-byte.
- [ ] **Step 3:** Normalize authority order to:

```text
1A Global DI Exact Contract
1B Shared Canonical Shell Exact Contract
1C DI-B01 Exact Owner Contract
2+ Existing chain
```

- [ ] **Step 4:** Update governance state to `P2.0A RECOVERY COMPLETE / INDEPENDENT REVIEW PENDING`; keep P2 unauthorized.
- [ ] **Step 5:** Explicitly document that P2.0A does not reopen P0/P1 and does not authorize production core code.
- [ ] **Step 6:** Commit governance/checksum changes.

---

### Task 5: Upgrade Verification Gates for P2.0A

**Files:**
- Modify: `.github/workflows/p2-0-b01-contract-freeze.yml`
- Modify if required: `.github/workflows/p1-contracts.yml`

**Interfaces:**
- Consumes: nine-source manifest and stacked PR topology.
- Produces: automated evidence that P2.0A preserves frozen sources and contains no production leakage.

- [ ] **Step 1:** Change normative checksum gate from exactly 8 to exactly 9 and run `sha256sum -c` on all nine entries.
- [ ] **Step 2:** Extend scoped authority allowlist to permit only the shared-core contract and checksum manifest in addition to the existing B01 contract.
- [ ] **Step 3:** Add support-surface coverage checks for ActorRef, TenantScope, Provenance, ObjectRevision and structural CanonicalObject/CanonicalRevision sections.
- [ ] **Step 4:** Add no-production-leakage checks for both:

```text
src/design_intelligence/contracts/core/*.py changes attributable to P2.0A
src/design_intelligence/contracts/b01/*.py
```

- [ ] **Step 5:** Preserve P0/P1 root tests, candidate baseline regression, compile, placeholder and whitespace gates.
- [ ] **Step 6:** Run workflows on the resulting head and require both P1 regression and P2.0/P2.0A scoped gate `completed/success`.
- [ ] **Step 7:** If a gate fails, diagnose the gate/contract boundary; do not weaken the gate merely to obtain green status.

---

### Task 6: Independent P2.0A Freeze Review

**Files:**
- Create: `P2_0A_FREEZE_REVIEW.md`

**Interfaces:**
- Consumes: final contract, ledger, audit, automated evidence, PR diff.
- Produces: independent blocker decision.

- [ ] **Step 1:** Re-read the global Exact Contract and frozen P0/P1 audit decisions independently of the recovery rationale.
- [ ] **Step 2:** Check for candidate silent promotion, closed-enum over-freeze, cross-owner coupling, Command/Event/Run reference pollution, ID-regex backdoor changes, and registry misclassification.
- [ ] **Step 3:** Verify final workflow runs correspond to the exact PR head.
- [ ] **Step 4:** Record findings as Critical / Important / Minor.
- [ ] **Step 5:** Only if Critical=0, Important=0, shared-core `SPEC_GAP=0`, and workflows pass, mark `P2.0A READY FOR P2.0 RE-REVIEW`.
- [ ] **Step 6:** Commit review record.

---

### Task 7: Re-review the Blocked P2.0 B01 Contract

**Files:**
- Modify: `B01_P2_0_FREEZE_REVIEW.md`
- Modify if necessary: `B01_CROSS_SPEC_FREEZE_AUDIT.md`
- Update PR #4 metadata/comment after stacked remediation is complete.

**Interfaces:**
- Consumes: P2.0A frozen-candidate shared shell.
- Produces: a new P2.0 decision on SC01–SC04 closure.

- [ ] **Step 1:** Map SC01–SC04 to the exact sections in the shared-core contract.
- [ ] **Step 2:** Verify B01 owner contract imports shared shell without redefining it.
- [ ] **Step 3:** Confirm all seven B01 canonical models are now implementable at contract level without copying candidate-only support structures.
- [ ] **Step 4:** Re-run final stacked CI on the exact P2.0A head.
- [ ] **Step 5:** If no blocker remains, update P2.0 review to:

```text
B01 owner-field recovery PASS
shared canonical shell closure PASS
P2.0 automated verification PASS
P2.0 independent Freeze Review PASS
P2.0 READY FOR USER FREEZE DECISION
P2 remains NOT AUTHORIZED until explicit user approval
```

- [ ] **Step 6:** Do not merge PR #4 or PR #5 and do not authorize P2 without explicit user Freeze approval.

---

## Completion Gate

P2.0A execution is complete only when:

```text
Shared-core field ledger complete
Scoped shared-core contract complete
9 / 9 normative checksums PASS
No original frozen-source drift
No candidate-baseline drift
No production core/B01 leakage
P0/P1 regression PASS
P2.0A independent review PASS
SC01-SC04 explicitly CLOSED
P2.0 re-review PASS
P2.0 READY FOR USER FREEZE DECISION
P2 still NOT AUTHORIZED
```
