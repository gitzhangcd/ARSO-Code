# P2.0 B01 Contract Recovery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recover, normalize, and freeze the field-level Exact V1 owner contract for the seven mandatory B01 canonical objects without creating any B01 production Python model.

**Architecture:** P2.0 is a normative recovery pipeline, not runtime implementation. It starts from the frozen global contract and source matrix, resolves object classification and field decisions into a traceable ledger, then emits one scoped owner contract plus a cross-spec audit. Every final field must have an explicit source/decision state and owner boundary.

**Tech Stack:** Markdown normative contracts, GitHub branch/PR governance, existing Exact V1 authority chain, SHA-256 source manifest.

**Spec:** `docs/superpowers/specs/2026-09-04-p2-0-b01-contract-recovery-design.md`

## Global Constraints

- P0 and P1 remain `FROZEN`.
- P2 implementation remains `NOT AUTHORIZED` throughout P2.0.
- Do not create `src/design_intelligence/contracts/b01/*.py`.
- Do not create DI shadows of ARSO primitives.
- `di_contracts_v1/` is evidence only and MUST NOT become owner authority.
- A lower-priority source MUST NOT override `DI-V5-EXACT-CONTRACT`.
- Genuine contradiction -> `SPEC_CONFLICT` and stop the affected object path.
- Missing exact contract without an approved recovery decision -> `SPEC_GAP`; do not guess.
- `StyleBrief != ReferenceTaskSpec`.
- `DesignSpec != GenerationPackage` and `DesignSpec != ordinary SystemArtifact`.
- `ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding`.

---

### Task R0: Freeze shared B01 canonical classification policy

**Files:**
- Create: `B01_FIELD_DECISION_LEDGER.md`
- Read: `B01_SOURCE_RECOVERY_MATRIX.md`
- Read: `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`

**Produces:** Per-object classification rows for all seven B01 objects covering object class, versioning, persistent reference kind, historical SSOT, authoring logical-ref allowance, snapshot/intervention/artifact eligibility, and CanonicalPayload shell policy.

- [ ] Re-read global identity/reference/registry rules and the B01 source matrix.
- [ ] Add a seven-object classification table to the ledger.
- [ ] For every classification value, tag `DIRECT_FROZEN`, `NORMALIZED_RECOVERY`, or `NEW_FREEZE_DECISION` with source/rationale.
- [ ] Verify no row derives owner truth solely from `di_contracts_v1`.
- [ ] Commit the classification ledger baseline.

### Task R1: Recover `DesignTaskBinding`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`
- Read: Engineering and Cross-Spec sections containing `DesignTaskBinding` YAML.

**Produces:** Exact field decisions for `DesignTaskBinding`.

- [ ] Record the direct-source fields: `id`, `design_state_ref`, `style_brief_ref`, `evaluation_contract_ref`, `enterprise_hard_policy_refs`, `risk_policy_ref`, `budget_policy_ref`, `intervention_policy_ref`, `reference_task_spec_ref`, `created_at`.
- [ ] Resolve each target owner and persistent ref kind without creating ARSO shadow types.
- [ ] Decide requiredness/cardinality only where the source or an explicit P2.0 normalization supports it.
- [ ] Record CanonicalPayload include/exclude policy for every field.
- [ ] Scan for duplication of `ReferenceTaskSpec`; reject any duplicated ARSO-owned task fields.
- [ ] Commit R1.

### Task R2: Recover `StyleBrief`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`
- Read: Application Specification sections defining StyleBrief semantics and requirement strengths.

**Produces:** Exact StyleBrief field/nested-value decisions that preserve `Constraint != Preference`.

- [ ] Group stable semantics into minimal typed owner values instead of copying prose headings blindly.
- [ ] Freeze requirement-strength vocabulary: `MUST`, `PREFER`, `EXPLORE`, `AVOID`, `FORBID`.
- [ ] Separate business context, design intent, constraints, preferences, references, fit/material context, and novelty intent.
- [ ] Reject prompt-only or ARSO-task-owned fields.
- [ ] Define CanonicalPayload policy for all StyleBrief fields.
- [ ] Commit R2.

### Task R3: Recover `ReferenceIntentBinding`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`
- Read: N06 and reference-intent vocabulary sources.

**Produces:** Minimal exact B01 reference-intent contract.

- [ ] Freeze the target `ReferenceAsset` relation without duplicating asset metadata.
- [ ] Freeze intent semantics sufficient to express use-purpose, scope/application region, preserve/edit intent, and semantic strength.
- [ ] Preserve the known intent vocabulary as an explicit value set only if source evidence supports a closed set; otherwise use a typed value plus documented minimum vocabulary.
- [ ] Reject compiled execution fields owned by B03.
- [ ] Define CanonicalPayload policy.
- [ ] Commit R3.

### Task R4: Recover `DesignContextBinding`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`

**Produces:** Exact binding-only context contract.

- [ ] Identify the minimum relation back to `StyleBrief` needed by the semantic chain.
- [ ] Identify context references that may point to B02, Infrastructure, enterprise knowledge, or ARSO-owned context without copying their schemas.
- [ ] Freeze cardinality/requiredness only with source-backed or explicit normalization decisions.
- [ ] Reject embedded copies of ontology, grammar, assets, or ARSO task/evaluation objects.
- [ ] Define CanonicalPayload policy.
- [ ] Commit R4.

### Task R5: Recover `DesignDecision`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`

**Produces:** Exact strategy/allocation contract.

- [ ] Freeze `brief_ref` as the relation required by N14 semantic closure.
- [ ] Normalize Primary/Secondary Focus, Visual Hierarchy, Silhouette Strategy, Volume Distribution, Construction Emphasis, Surface/Material Expression, Novelty Allocation, and Commercial/Risk Allocation into minimal typed decision values.
- [ ] Reject garment-description/specification fields.
- [ ] Define CanonicalPayload policy.
- [ ] Commit R5.

### Task R6: Recover `DesignRoute`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`

**Produces:** Exact controlled-route contract.

- [ ] Freeze `decision_ref` as required by N14.
- [ ] Normalize route identity/intent, mechanism/strategy, route-level constraints, and selection-relevant semantics without introducing runtime execution configuration.
- [ ] Reject random-variant semantics and B03 compiler/executor fields.
- [ ] Define CanonicalPayload policy.
- [ ] Commit R6.

### Task R7: Recover `DesignSpec`

**Files:**
- Modify: `B01_FIELD_DECISION_LEDGER.md`

**Produces:** Exact authoritative-structured-intent contract.

- [ ] Freeze `route_ref` as required by N14.
- [ ] Recover the minimal structured design-intent surface needed to compile downstream while remaining distinct from prompt/GenerationPackage.
- [ ] Preserve global negative registry rules: `artifact_eligible=false`, `system_intervention_target_eligible=false`.
- [ ] Reject B03 execution/package fields and mutable generation state.
- [ ] Freeze owner-specific CanonicalPayload policy.
- [ ] Commit R7.

### Task R8: Emit scoped B01 owner authority

**Files:**
- Create: `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md`
- Modify: `B01_FIELD_DECISION_LEDGER.md`

**Produces:** `DI-B01-EXACT-CONTRACT`, a field-level scoped authority subordinate to the global Exact Contract.

- [ ] Convert only resolved ledger decisions into normative object schemas.
- [ ] Include shared nested value contracts and enums/value sets required by those schemas.
- [ ] Include per-object registry policy and CanonicalPayload policy.
- [ ] Include explicit semantic-closure relations and negative boundaries.
- [ ] Include a decision register identifying every `NEW_FREEZE_DECISION`.
- [ ] Verify all 7 objects are covered and no field lacks provenance.
- [ ] Commit R8.

### Task R9: Cross-spec freeze audit and governance update

**Files:**
- Create: `B01_CROSS_SPEC_FREEZE_AUDIT.md`
- Modify: `SPEC_AUTHORITY.md`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `specs/SPEC_SOURCE_CHECKSUMS.sha256`
- Modify: PR #4 description

**Produces:** P2.0 freeze candidate and explicit P2 authorization recommendation.

- [ ] Audit every owner schema against the seven-source authority chain and frozen distinctions.
- [ ] Count unresolved `SPEC_CONFLICT` and blocking field-level `SPEC_GAP`.
- [ ] Verify no B01 production Python files were added.
- [ ] Add `DI-B01-EXACT-CONTRACT` to the authority order as scoped 1B without overriding global 1A.
- [ ] Recompute/record the source checksum manifest to include the new normative owner contract while preserving existing source hashes.
- [ ] Update governance state to `P2.0 COMPLETE / AWAITING FREEZE REVIEW` only if blockers are zero; otherwise mark `BLOCKED`.
- [ ] Perform independent Freeze Review on the final PR diff.
- [ ] Do not merge or authorize P2 without explicit user Freeze approval.
