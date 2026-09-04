# P2.0｜B01 Owner Contract Recovery 独立 Freeze Review

Review 日期：2026-09-04  
Review 对象：PR #4 `p2-0-b01-contract-recovery`  
基线：`main@7102c7e264784bd18bf0b423c2f4b12065a17ab9`  
审查起始 head：`2c75d9db4959cf0191ca0cce8065893c5100a399`  
Review 模式：实现/恢复过程之外的第二遍 criteria-based review  
最终结论：`BLOCKED / NOT READY FOR P2.0 FREEZE`

> 本 Review 独立于 `B01_CROSS_SPEC_FREEZE_AUDIT.md`。前者从 recovery 产物内部检查 B01 owner contract；本文件进一步检查“P2 是否真的能在不猜 contract 的条件下实现完整 B01 canonical models”。后者发现一个此前未计入的 shared-core exactness blocker，因此本文件的结论优先于 preliminary freeze recommendation。

---

## 1. Review 方法

重新从最高优先级规范与已冻结 P0/P1 checkpoint 出发，检查：

1. N11 七个 B01 mandatory objects 是否完整；
2. 每个 B01 owner field 是否有 provenance / type / cardinality / requiredness / ref policy；
3. 是否存在 closed-enum over-freeze；
4. 是否越权冻结其他 primitive owner 的 object class；
5. 是否把 mutable selection/runtime/execution state 放入 B01 canonical semantics；
6. B01 CanonicalPayload 是否显式而非 candidate-derived；
7. P0/P1 frozen source 和 baseline 是否保持不变；
8. P2 若按当前 owner contract实现完整 canonical models，是否仍需要猜任何 shared canonical-shell contract。

---

## 2. Positive findings

### 2.1 B01 mandatory surface

`DI-V5-EXACT-CONTRACT` N11 要求：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

`DI-B01-EXACT-CONTRACT` 覆盖：`7 / 7`。

Verdict：`PASS`。

### 2.2 Owner-field traceability

`B01_FIELD_DECISION_LEDGER.md` 对 owner fields 显式记录：

```text
wire type
cardinality
requiredness
semantic owner
reference kind
recovery decision
CanonicalPayload policy
```

并使用：

```text
DIRECT_FROZEN
NORMALIZED_RECOVERY
NEW_FREEZE_DECISION
DEFERRED
REJECTED
```

避免将新 normalization 冒充上游直接定义。

Verdict：`PASS`。

### 2.3 ReferenceIntentBinding 没有 closed-enum over-freeze

上游仅把 reference intent categories描述为典型值，因此 owner contract 将：

```text
SILHOUETTE_REFERENCE
DETAIL_REFERENCE
MATERIAL_REFERENCE
COLOR_REFERENCE
STRUCTURE_REFERENCE
MOOD_REFERENCE
KEEP_REFERENCE
EDIT_REFERENCE
```

冻结为 minimum recognized vocabulary，而不是 exhaustive closed enum。

Verdict：`PASS`。

### 2.4 Cross-owner reference boundary

B01 没有替 B02 / B04 / Infrastructure 等 owner 猜 object class；目标 class 未冻结时使用：

```text
CanonicalRef = ExactObjectRef | ObjectRef
```

而不是 `LogicalObjectRef` 或隐式 latest。

Verdict：`PASS`。

### 2.5 Runtime / mutable-state leakage

未在 DesignRoute 中写入：

```text
selected/status
executor/model
random_seed
```

未在 DesignSpec 中写入：

```text
prompt
mask
model_parameters
resolution
aspect_ratio
generation_status
```

未在 ReferenceIntentBinding 中写入 compiled execution fields。

Verdict：`PASS`。

### 2.6 DesignTaskBinding classification

P2.0 将 `DesignTaskBinding` normalise 为 `IMMUTABLE_FACT`，而非 mutable binding state。其输入变化产生新 fact，不覆写历史 binding。

该决定与：

```text
HistoricalTruthImmutable
StyleBrief != ReferenceTaskSpec
```

一致。

Verdict：`PASS / NEW_FREEZE_DECISION`。

### 2.7 B01 CanonicalPayload

P1 hash engine故意不猜 owner payload。P2.0 已显式冻结 B01 include/exclude policy，没有直接复制 candidate blacklist。

Verdict：`PASS`。

### 2.8 Source and implementation leakage

自动 gate 已验证：

```text
8 / 8 normative checksums
7 / 7 B01 surface
No B01 production Python leakage
P0/P1 regression PASS
candidate baseline regression PASS
compile PASS
placeholder/whitespace/scope PASS
```

P2.0 workflow run：`33887779202` -> `SUCCESS`。  
P1 regression workflow run：`33887779153` -> `SUCCESS`。

Verdict：`PASS`。

---

# 3. Important finding｜Shared Canonical Shell Exactness

## P2.0-SC01｜`ActorRef` exact wire contract missing

Global Exact Contract §6 freezes the **field role**:

```text
created_by
```

and the P2.0 owner contract names its dependency as：

```text
created_by: ActorRef
```

However, the authoritative source chain does not freeze `ActorRef`'s exact internal wire fields/value types.

The only complete structure currently present in the repository is in `di_contracts_v1` candidate, for example:

```text
actor_type
actor_id
```

Candidate baseline is not normative authority and therefore cannot be copied into P2 production as owner truth.

Status：`SPEC_GAP / IMPORTANT / P2 IMPLEMENTATION BLOCKER`。

## P2.0-SC02｜`TenantScope` exact wire contract missing

Global canonical metadata requires:

```text
tenant_scope
```

but does not freeze the exact `TenantScope` internal field shape/value set in the authoritative chain.

Candidate has one proposed representation, but candidate-only structure cannot be silently promoted.

Status：`SPEC_GAP / IMPORTANT / P2 IMPLEMENTATION BLOCKER`。

## P2.0-SC03｜`Provenance` exact wire contract missing

Global metadata requires:

```text
provenance
```

but exact fields, cardinalities, optionality, and target reference policies are not frozen by the authority chain.

Candidate provides `source_refs / command_ref / run_ref / external_source_refs`, but this remains candidate evidence only.

Status：`SPEC_GAP / IMPORTANT / P2 IMPLEMENTATION BLOCKER`。

## P2.0-SC04｜`ObjectRevision` exact wire contract missing

The global contract freezes the semantics：

```text
revision = server-assigned ordering metadata
revision != SchemaVersion
parentage = parent_refs
```

but does not freeze the exact wire type/range/lexical contract of `ObjectRevision`.

P2.0 canonical revisions require `revision`, so a complete P2 Pydantic schema cannot be exact until this support type is frozen.

Status：`SPEC_GAP / IMPORTANT / P2 IMPLEMENTATION BLOCKER`。

---

# 4. Why this blocks P2.0 Freeze

This is not a B01 primitive-ownership conflict. B01 correctly does **not** own the internals of `ActorRef`, `TenantScope`, `Provenance`, or `ObjectRevision`.

But P2.0's stated success criterion is stronger than “B01 business fields are known”. It requires the resulting owner contract to make P2 `Full B01 Exact Schemas` implementable without guessing.

Every B01 canonical model imports the shared shell. Therefore:

```text
B01 owner fields complete
+
shared canonical shell incomplete
=
full B01 exact model still not safely implementable
```

The earlier audit statement that shared-core internals “do not count as a P2.0 blocker” is therefore too weak for the approved P2.0 Freeze Gate.

This Review supersedes that preliminary recommendation.

---

# 5. Findings summary

```text
Critical:  0
Important: 4 shared-core SPEC_GAP items
Minor:     0
```

No `SPEC_CONFLICT` found.

B01 owner-field result:

```text
7 / 7 objects covered
B01 owner-field SPEC_GAP = 0
B01 cross-spec conflict = 0
```

End-to-end P2 implementability result:

```text
Shared-core exact SPEC_GAP = 4
P2 implementability = BLOCKED
```

---

# 6. Required remediation

Do NOT solve SC01–SC04 by copying `di_contracts_v1`.

Required next contract-recovery substage：

```text
P2.0A｜Shared Canonical Shell Support Contract Recovery
```

Minimum scope：

```text
ActorRef
ActorId / ActorType as required
TenantScope
TenantId / TenantScopeType as required
Provenance
ObjectRevision
```

The substage must determine which items are nominal open strings versus closed enums, exact cardinalities/optionality, and shared CanonicalPayload/metadata semantics where applicable.

It MUST NOT modify already frozen P0/P1 semantics; it should add a scoped shared-core companion contract under the global Exact Contract.

After P2.0A is independently reviewed, this PR's B01 owner contract can be re-evaluated against the completed shared shell.

---

# 7. Freeze Review Decision

```text
P2.0 B01 OWNER-FIELD RECOVERY: PASS
P2.0 B01 CROSS-SPEC CONSISTENCY: PASS
P2.0 AUTOMATED VERIFICATION: PASS
P2.0 SHARED-CANONICAL-SHELL CLOSURE: BLOCKED
P2.0 FREEZE REVIEW: BLOCKED
```

Current recommended governance state：

```text
P0: FROZEN
P1: FROZEN
P2.0: BLOCKED BY SHARED-CORE SPEC_GAP
P2.0A: RECOMMENDED / NOT YET AUTHORIZED
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

PR #4 MUST remain Draft and MUST NOT be merged as a Frozen checkpoint in this state.
