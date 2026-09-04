# P2 Freeze Decision

## 决策

```text
P2: FROZEN
```

用户于 2026-09-05 明确批准 `P2 | Full B01 Exact Schemas` Freeze。

本决策仅冻结已经通过正式独立 Freeze Review 的 P2 实现范围，不自动授权 P3 或 Exact V1 全局发布。

## 冻结基线

Parent published checkpoint:

```text
main@8beef2baa733a346e0aa81ac5ffd652f926be84b
```

Formal Freeze Review head:

```text
e76358d843adfcff9350fd286446a8a752ea348d
```

Formal review result:

```text
Critical = 0
Important = 0
Minor = 3 / NON-BLOCKING
P2 FREEZE REVIEW = PASS
```

Review record:

```text
P2_B01_EXACT_SCHEMAS_FREEZE_REVIEW.md
```

Implementation audit:

```text
P2_B01_EXACT_SCHEMAS_AUDIT.md
```

## 冻结范围

### Shared canonical shell support required by B01

```text
ActorId
ActorType
ActorRef
TenantId
TenantScopeType
TenantScope
Provenance
ObjectRevision
CanonicalObject
CanonicalRevision
ImmutableFact
JsonValue finite-number validation
UTC created_at normalization
```

These remain shared support/nested/structural types and do not become independent registry primitives.

### B01 nested/value types

```text
RequirementStrength
BriefRequirement
ContextRefBinding
DesignSpecAssignment
STANDARD_REFERENCE_INTENT_CODES
```

### B01 canonical objects

Exactly seven B01 canonical objects are frozen:

```text
StyleBrief
ReferenceIntentBinding
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
DesignTaskBinding
```

Classification split:

```text
6 x CANONICAL_REVISION
1 x IMMUTABLE_FACT (DesignTaskBinding)
```

### B01 canonical payload / content hash

The explicit owner-specific CanonicalPayload allow-list is frozen for all seven B01 object types.

Included:

```text
schema_version
object_type
owner semantic/binding fields
extensions
```

Excluded:

```text
id
logical_id
revision
parent_refs
created_at
created_by
tenant_scope
provenance
content_hash
```

The existing P1 RFC 8785 + SHA-256 hash engine remains unchanged.

### B01 registry

The exact seven-entry B01 registry manifest is frozen:

```text
StyleBrief                 -> CANONICAL_REVISION / EXACT_OBJECT_REF
ReferenceIntentBinding     -> CANONICAL_REVISION / EXACT_OBJECT_REF
DesignContextBinding       -> CANONICAL_REVISION / EXACT_OBJECT_REF
DesignDecision             -> CANONICAL_REVISION / EXACT_OBJECT_REF
DesignRoute                -> CANONICAL_REVISION / EXACT_OBJECT_REF
DesignSpec                 -> CANONICAL_REVISION / EXACT_OBJECT_REF
DesignTaskBinding          -> IMMUTABLE_FACT     / OBJECT_REF
```

The six revision objects allow logical authoring references and are review-snapshot eligible. `DesignTaskBinding` allows neither.

### AC-01 and deterministic schemas

The following are frozen as executable P2 conformance evidence:

```text
tests/conformance/ac/test_ac_01_b01_exact_schemas.py
tools/export_b01_json_schemas.py
generated/json_schema/di.b01.style_brief.schema.json
generated/json_schema/di.b01.reference_intent_binding.schema.json
generated/json_schema/di.b01.design_context_binding.schema.json
generated/json_schema/di.b01.design_decision.schema.json
generated/json_schema/di.b01.design_route.schema.json
generated/json_schema/di.b01.design_spec.schema.json
generated/json_schema/di.b01.design_task_binding.schema.json
```

AC-01 freezes the 7/7 inventory, exact field set/requiredness, `additionalProperties=false`, fixed JSON Schema `object_type.const`, registry-to-model agreement, and deterministic committed artifact equality.

## 明确未冻结 / 未授权范围

The P2 Freeze does not authorize or claim completion of:

```text
P3 / Full B02 Exact Schemas
B03-B08 production models or runtime lowering
semantic closure resolver tests reserved for later gates
ARSO production primitive completion beyond existing frozen refs
Command/Event/Protocol completion
CanonicalObjectStore / CAS / resolver infrastructure
snapshot firewalls
UI / executor / image-generation integration
optimizer / deployment behavior
Exact V1 global release
```

In particular, B01 semantic closure target agreement remains a later resolver-level proof and is not falsely claimed as schema-level validation.

## Non-blocking maintenance findings

The formal review recorded three non-blocking maintenance items:

```text
1. GitHub Actions Node 20 compatibility/deprecation warnings.
2. Two test assertions use deprecated instance-level Pydantic `model_fields` access.
3. JSON Schema renderer bytes are sensitive to Pydantic 2.x minor versions; committed artifact equality prevents silent drift, while final release tooling should pin or qualify the renderer environment.
```

These do not alter B01 wire semantics and do not block the P2 Freeze.

## Decision-head verification

The first decision record head was:

```text
c1408d8a3a5689b59367a635617336d16176162e
```

Fresh verification on that exact decision head:

```text
P1 contract verification
run 33926245681 = SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33926245684 = SUCCESS
```

The two runs cover root tests including AC-01, candidate-baseline regression, 9/9 normative checksums, shared-core digest, B01/shared-core source coverage, production compilation, whitespace/placeholder checks, frozen-source drift, and authority-source scope.

This verification evidence is historical evidence for the decision content. Because this paragraph itself creates a new commit, the final PR head containing it MUST again receive fresh verification before merge.

## 发布门禁

Before merge:

```text
1. final PR head containing this decision record MUST receive fresh P1 verification PASS;
2. final PR head MUST receive fresh P2.0/B01 + Shared-Core verification PASS;
3. PR #6 MUST still target main and remain mergeable;
4. merge MUST use the expected exact PR head SHA.
```

After merge:

```text
1. published main MUST contain this P2_FREEZE_DECISION.md;
2. published main tree MUST be verified against the tested final PR head;
3. current P1/P2 workflows are PR-only, so tree equality with the tested final head is the publication-equivalence proof unless a separate main/push run exists;
4. no semantic change may be introduced during merge.
```

## 状态

```text
P0 = FROZEN
P1 = FROZEN
P2.0/P2.0A = FROZEN
P2 = FROZEN / PENDING FINAL-HEAD VERIFICATION + PUBLICATION TO main
P3+ = NOT AUTHORIZED
Exact V1 global = FREEZE CANDIDATE
```

This record is the explicit human Freeze decision for P2. It does not itself authorize P3.