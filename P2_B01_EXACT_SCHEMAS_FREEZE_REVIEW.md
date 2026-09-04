# P2｜Full B01 Exact Schemas 独立 Freeze Review

Review 日期：2026-09-05  
Review 模式：实现完成后的独立 criteria-based Freeze Review  
Review 对象：PR #6 `p2-b01-exact-schemas`  
发布基线：`main@8beef2baa733a346e0aa81ac5ffd652f926be84b`  
审查起始 exact head：`fc2209c9181b41f4d74d558e3c6ee9d3611af84a`  
结论：`PASS / READY FOR USER FREEZE DECISION`

> 本文件与 P2 implementation execution / audit 分离，重新从冻结 authority 出发审查实现，不把既有实现或 candidate baseline 当作规范来源。本 Review 不自行 merge PR #6，也不自动授权 P3。

## 1. Review 方法

本次正式 Freeze Review 重新执行以下审查链：

1. 重新读取 `DI_B01_Exact_V1_Owner_Contract.md`，逐项核对 7/7 B01 canonical objects、exact owner fields、classification、reference policy、registry policy、CanonicalPayload policy、negative boundary；
2. 重新读取 `DI_Shared_Canonical_Shell_Exact_V1_Contract.md`，核对 Actor/Tenant/Provenance/ObjectRevision、canonical structural bases、UTC rule、support-type registry exclusion 与 P0/P1 compatibility；
3. 对照 `P2_B01_EXACT_SCHEMAS_AUDIT.md`，但不把 audit 自述作为通过依据；
4. 检查 PR #6 changed-file inventory 与 `main...head` compare，确认实现范围与未授权 surface；
5. 逐项复核 production code：shared shell、B01 models、owner-specific hashing、B01 registry、public exports；
6. 逐项复核 schema/unit/hash/registry/AC-01 tests 与 deterministic exporter；
7. 核对 committed 7 个 JSON Schema artifacts 的 role 与 AC-01 reproducibility gate；
8. 核对 final exact-head GitHub Actions，包括 P1 regression、root tests、candidate baseline、9/9 normative checksum、compile、whitespace、source drift 与 authority scope；
9. 单独检查 schema/runtime divergence、dependency-driven schema drift、P2→P3 leakage、candidate promotion、implicit latest/current semantics、B03 runtime contamination。

## 2. Authority / Baseline Integrity

### 2.1 Normative source integrity

Final exact-head verification confirms:

```text
9 / 9 registered normative source checksums = PASS
DI_Shared_Canonical_Shell registered digest = PASS
original frozen authority sources = unchanged
candidate baseline di_contracts_v1/ = unchanged
```

P2 implementation therefore does not rewrite its own authority basis.

### 2.2 P0 / P1 compatibility

Frozen P1 public star-export sets remain unchanged. P2 shared-shell symbols are explicit `contracts.core` module attributes but are intentionally excluded from the P1-frozen `__all__`; the B01 registry manifest is likewise available as an explicit module attribute while the P1 registry `__all__` remains exact.

Verdict: `PASS`.

## 3. Shared Canonical Shell Conformance

| Review item | Frozen requirement | Implementation | Result |
|---|---|---|---|
| ActorId | strict, non-empty nominal string | strict RootModel + min length | PASS |
| ActorType | strict, non-empty, open vocabulary; standard codes recognized | open nominal RootModel; tests cover USER/SERVICE/AGENT/SYSTEM/EXTERNAL + custom value | PASS |
| ActorRef | exactly actor_type + actor_id | exact FrozenDIModel shape | PASS |
| TenantId | strict, non-empty nominal string | strict RootModel + min length | PASS |
| TenantScopeType | exactly GLOBAL / TENANT | closed StrEnum | PASS |
| TenantScope coupling | GLOBAL=>null; TENANT=>non-null | model validator | PASS |
| Provenance | exactly source_refs + external_source_refs | exact frozen shape | PASS |
| Provenance refs | persistent CanonicalRef only; LogicalObjectRef forbidden | CanonicalRef tuple, regression test rejects logical ref | PASS |
| external_source_refs | strict non-empty strings | Annotated min-length string tuple | PASS |
| ObjectRevision | strict integer >=1 | strict RootModel + ge=1 | PASS |
| CanonicalObject | exact 8-field required shell | exact required field set | PASS |
| CanonicalRevision | CanonicalObject + logical_id/revision/parent_refs | exact required extension | PASS |
| ImmutableFact | adds no shared fields | exact structural base | PASS |
| UTC created_at | reject naive; normalize aware to UTC | field validator + tests | PASS |
| JSONValue numbers | finite only | recursive finite validation | PASS |
| Registry exclusion | support/nested/base types not registered | no shared-shell registry entries | PASS |

No shared-core blocker found.

## 4. B01 Exact Model Conformance

Exactly seven canonical B01 models are implemented:

```text
StyleBrief
ReferenceIntentBinding
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
DesignTaskBinding
```

Classification split is exact:

```text
6 x CANONICAL_REVISION
1 x IMMUTABLE_FACT = DesignTaskBinding
```

### 4.1 Field / requiredness review

For every object, production `model_fields` equals:

```text
exact inherited structural shell
+
exact owner field set from DI-B01-EXACT-CONTRACT
```

All exact wire fields are required. Nullable fields remain required-but-nullable. Tuple fields may be empty except the three owner-frozen non-empty sequences.

Frozen non-empty owner rules are implemented for:

```text
ReferenceIntentBinding.intent_codes
DesignRoute.mechanisms
DesignSpec.assignments
```

Verdict: `7 / 7 PASS`.

### 4.2 object_type exactness

Each model has two independent protections:

```text
runtime -> model validator rejects mismatched ObjectType
JSON Schema -> object_type property publishes exact const
```

This closes the runtime/schema divergence exposed by AC-01 RED.

Verdict: `PASS`.

### 4.3 Reference-policy review

B01 committed refs use only:

```text
ExactObjectRef
ObjectRef
CanonicalRef = ExactObjectRef | ObjectRef
```

`LogicalObjectRef` is not admitted to committed B01 owner fields. Cross-object target agreement remains correctly deferred to the later resolver/semantic-closure stage rather than being guessed inside P2 schema-local validation.

Verdict: `PASS`.

### 4.4 Negative boundary review

The exact model surfaces do not contain or accept the forbidden drift fields, including:

```text
prompt / negative_prompt
executor / model_parameters
resolution / aspect_ratio
generation_status
route selected/status flags
embedded B02 definitions
compiled reference masks/positions
embedded ARSO task policy contents
```

`extra="forbid"` turns these into explicit validation failures.

Verdict: `PASS`.

## 5. Requirement / Reference Intent Value Semantics

`RequirementStrength` is exactly:

```text
MUST
PREFER
EXPLORE
AVOID
FORBID
```

No numeric collapse was introduced.

Reference intent vocabulary recognizes the frozen minimum standard codes while remaining open to additional codes; the implementation does not incorrectly convert the upstream typical categories into a closed enum.

Verdict: `PASS`.

## 6. CanonicalPayload / Content Hash Review

The B01 payload implementation uses an explicit owner-type allow-list, not a generic blacklist/introspection rule.

Included exactly:

```text
schema_version
object_type
owner semantic/binding fields
extensions
```

Excluded exactly:

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

Tests independently show:

```text
identity/revision/audit metadata changes -> semantic hash unchanged
owner semantic change -> hash changes
extensions change -> hash changes
non-B01 canonical object -> rejected
```

The implementation reuses the frozen P1 RFC8785/SHA-256 engine and does not redefine canonicalization.

Verdict: `PASS`.

## 7. Registry Review

The manifest contains exactly seven B01 entries. Common frozen properties are explicit:

```text
schema_version = 1.0
canonical = true
primitive_owner = DI_B01
capability_owners = [DI_B01]
state_domain = TASK
historical_ssot = true
system_snapshot_eligible = false
knowledge_snapshot_eligible = false
system_intervention_target_eligible = false
artifact_eligible = false
```

Six authored revisions are:

```text
CANONICAL_REVISION
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
logical_authoring_ref_allowed = true
review_snapshot_eligible = true
```

`DesignTaskBinding` is:

```text
IMMUTABLE_FACT
versioned = false
persistent_ref_kind = OBJECT_REF
logical_authoring_ref_allowed = false
review_snapshot_eligible = false
```

AC-01 resolves every registry `python_type` and proves object_type <-> model <-> JSON Schema const agreement.

Verdict: `PASS`.

## 8. AC-01 / JSON Schema Artifact Review

AC-01 covers exactly the seven B01 canonical objects and no B02+ object.

For every model it checks:

```text
JSON Schema exists
additionalProperties = false
properties = exact field set
required = exact field set
object_type.const = exact B01 object type
registry/model path agreement
registry/schema object_type agreement
```

Generated artifact gate checks:

```text
exactly 7 di.b01.*.schema.json files
UTF-8 JSON
sorted keys
indent = 2
final newline
committed JSON == current model_json_schema()
```

The exporter deletes unexpected B01 schema files and re-renders only the seven frozen models.

Verdict: `AC-01 PASS`.

## 9. Scope / Leakage Review

PR #6 final changed-file inventory is confined to:

```text
P2 authorization / plan / audit / review evidence
P2.0 stage-gate narrowing required after authorization
shared canonical-shell support implementation
B01 models + hashing
B01 registry manifest
P2 tests + AC-01
deterministic JSON Schema exporter + seven artifacts
P1 scope test transition from P2-forbidden to P3-forbidden
```

No production implementation was found for:

```text
B02 canonical schemas
B03 GenerationPackage/runtime lowering
B04-B08 canonical production models
B07 resolver / DesignState semantic closure
ARSO primitive completion
Command/Event/Protocol completion
CanonicalObjectStore / CAS
snapshot firewall
UI / LLM / image generation integration
optimizer / deployment behavior
```

Verdict: `NO P3 LEAKAGE / PASS`.

## 10. Verification Evidence

### 10.1 AC-01 RED proof

Exact RED head:

```text
5405ba11eadb8d0cb40fd255a7525d03b2d75dd3
```

Run:

```text
P2.0 B01 + Shared-Core contract verification
33925174082 = EXPECTED FAILURE
```

Failure was limited to the intended AC-01 gaps:

```text
object_type JSON Schema const missing
registry/schema const assertion failed
seven generated B01 JSON Schema artifacts missing
```

Normative checksum and source-surface checks passed before the failing root test.

### 10.2 Implementation GREEN proof

Pre-audit implementation head:

```text
83a16e81f0f31dd66c83c52e4453de6a05425998
```

```text
P1 run 33925467255 = SUCCESS
P2.0/B01 run 33925467269 = SUCCESS
```

### 10.3 Final pre-review exact-head proof

Audit-record head:

```text
fc2209c9181b41f4d74d558e3c6ee9d3611af84a
```

Fresh verification:

```text
P1 contract verification
run 33925550659 = SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33925550654 = SUCCESS
```

Final workflows confirm success for:

```text
P1 targeted tests
root tests including AC-01
candidate baseline regression
9/9 normative source checksums
shared-core digest equality
B01 7/7 source coverage
shared-core source coverage
production compile
placeholder scan
non-Markdown diff whitespace
Markdown whitespace policy
frozen-source / candidate-baseline drift
P2.0/P2.0A authority-source scope
```

## 11. Findings

### Critical

```text
0
```

### Important

```text
0
```

### Minor

#### P2-M01 | GitHub Actions Node compatibility warnings

`actions/checkout@v4` / `actions/setup-python@v5` emit Node 20 deprecation/compatibility warnings while the hosted runner forces the Node 24 compatibility path.

Disposition:

```text
NON-BLOCKING / CI MAINTENANCE
```

This is inherited tooling maintenance and does not alter the P2 contract or verification result.

#### P2-M02 | Two tests use deprecated instance.model_fields access

`tests/unit/test_p2_shared_canonical_shell.py` accesses `actor.model_fields` and `provenance.model_fields` through instances. Pydantic 2.13 reports `PydanticDeprecatedSince211`; class-level access should eventually replace it.

Disposition:

```text
NON-BLOCKING / TEST MAINTENANCE
```

Production code is unaffected and Pydantic 3 is currently outside the supported dependency range (`<3`).

#### P2-M03 | JSON Schema rendering is Pydantic-minor-version sensitive

The package declares:

```text
pydantic>=2.12,<3
```

while committed JSON Schema artifacts are renderer output from the verified environment (Pydantic 2.13.5). A future Pydantic 2.x release could change renderer formatting/structure even if semantic wire behavior remains compatible.

Disposition:

```text
NON-BLOCKING / RELEASE-TOOLCHAIN GOVERNANCE
```

This cannot silently change the frozen repository because AC-01 compares committed bytes/JSON against `model_json_schema()` and will fail on renderer drift. Before an eventual packaged Exact V1 release, dependency locking or an explicit schema-renderer compatibility matrix should be considered. P2 should not broaden scope merely to preempt a future dependency upgrade.

## 12. Freeze Review Decision

No Critical or Important defect was found that requires reopening P2 contract design or implementation.

Formal verdict:

```text
P2 IMPLEMENTATION        = PASS
P2 SPEC CONFORMANCE      = PASS
SHARED-SHELL CONFORMANCE = PASS
B01 7/7 EXACTNESS        = PASS
B01 CANONICALPAYLOAD     = PASS
B01 REGISTRY             = PASS
AC-01                    = PASS
P0/P1 REGRESSION         = PASS
SPEC / BASELINE DRIFT    = PASS
P3+ SCOPE BOUNDARY       = PASS
P2 FREEZE REVIEW         = PASS
```

Recommended checkpoint:

```text
P0: FROZEN
P1: FROZEN
P2.0/P2.0A: FROZEN
P2: IMPLEMENTATION COMPLETE / FREEZE REVIEW PASS / AWAITING USER FREEZE DECISION
P3+: NOT AUTHORIZED
Exact V1 global: FREEZE CANDIDATE
```

This Review does **not** itself mark P2 `FROZEN` and does **not** merge PR #6. The next valid transition is an explicit user P2 Freeze decision. If approved, record the freeze decision on the exact review head, run fresh verification for that decision head, then use expected-head merge to `main`; the published `main` checkpoint must receive fresh verification before any P3 authorization decision.
