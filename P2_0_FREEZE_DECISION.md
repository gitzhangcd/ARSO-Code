# P2.0 Freeze Decision

## 决策

```text
P2.0: FROZEN
P2.0A: FROZEN AS INCLUDED REMEDIATION
```

用户于 2026-09-05 明确批准：

```text
批准 P2.0 Freeze
→ 合并 PR #5 到 PR #4
→ fresh verification
→ 记录 P2_0_FREEZE_DECISION
→ 合并 PR #4 到 main
→ 验证 main checkpoint
→ 授权 P2｜Full B01 Exact Schemas
```

本决策冻结的是 **contract checkpoint**，不是 production implementation。

## 冻结范围

### P2.0｜B01 Owner Contract Recovery

冻结 exactly seven B01 canonical-object owner contracts：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

冻结内容包括：

```text
field-level wire shape
requiredness / cardinality
reference policy
object classification
registry policy
B01 CanonicalPayload policy
cross-object semantic closure requirements
negative ownership/runtime boundaries
```

Normative scoped contract：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

### P2.0A｜Shared Canonical Shell Support Contract Recovery

P2.0A 作为 P2.0 的 remediation 子阶段一并冻结：

```text
ActorId
ActorType
ActorRef
TenantId
TenantScopeType
TenantScope
Provenance
ObjectRevision
CanonicalObject structural base
CanonicalRevision structural base
ImmutableFact structural base
UTC datetime normalization
```

Normative scoped contract：

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

关键 normalization：

```text
ActorType = open typed vocabulary
standard codes = USER / SERVICE / AGENT / SYSTEM / EXTERNAL

TenantScopeType = GLOBAL | TENANT
GLOBAL != public / permissionless

Provenance = source_refs + external_source_refs
candidate command_ref:ObjectRef = REJECTED
candidate run_ref:ObjectRef = DEFERRED

ObjectRevision = JSON integer >= 1
revision = ordering metadata only
parentage = parent_refs
```

Shared support types不是新的 Object Registry domain primitives。

## 冻结依据

### P2.0A 独立 Review

`P2_0A_FREEZE_REVIEW.md`：

```text
Critical:  0
Important: 0
Minor:     0
SPEC_CONFLICT = 0
blocking shared-core SPEC_GAP = 0
SC01-SC04 = CLOSED
```

### P2.0 remediation re-review

`B01_P2_0_FREEZE_REVIEW.md`：

```text
7 / 7 B01 objects covered
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
SPEC_CONFLICT = 0
P2 contract-level implementability = PASS
P2.0 independent re-review = PASS
```

### PR #5 final verification

PR #5 final verified head：

```text
ce041aecb3af381c1349aac057b7630e243a25de
```

Fresh runs：

```text
P1 contract verification
run 33898835918 = SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33898836017 = SUCCESS
```

PR #5 was merged into `p2-0-b01-contract-recovery` with merge commit：

```text
455b1254eca17d2ecb819b66a58b86f710e4bd80
```

### PR #4 combined-head verification before this decision record

Combined PR #4 head：

```text
455b1254eca17d2ecb819b66a58b86f710e4bd80
```

Fresh runs：

```text
P1 contract verification
run 33900293912 = SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33900293877 = SUCCESS
```

Verified gates include：

```text
9 / 9 normative checksums
registered shared-core digest equality
B01 7 / 7 surface
shared-core required surface
no production core/B01 leakage
P0/P1 regression
candidate baseline regression
compile
placeholder scan
whitespace gates
authority-source scope gate
```

## 明确不包含

P2.0 Freeze 不冻结或实现：

```text
B01 production Pydantic models
B02-B08 production models
ARSO authoritative primitive imports
Command/Event/Protocol completion
semantic resolver/store/CAS
snapshot firewalls
full registry inventory
physical DB/storage/event bus
algorithms/models/thresholds
DEFERRED production self-modification capabilities
```

`di_contracts_v1/` 继续保持只读 executable evidence，不成为 normative authority。

## P2 授权条件

用户已经明确批准 P2 授权，但授权按以下顺序生效：

```text
P2_0_FREEZE_DECISION committed
→ exact decision head fresh verification PASS
→ PR #4 merged to main with expected-head protection
→ resulting main checkpoint fresh verification PASS
→ P2 = AUTHORIZED
```

在 `main` checkpoint 验证完成之前：

```text
P2: AUTHORIZATION APPROVED / NOT YET EFFECTIVE
```

验证完成之后：

```text
P2: AUTHORIZED
Scope: Full B01 Exact Schemas
```

本授权只允许进入 P2 的 planning/TDD/implementation workflow，不自动授权 P3 或任何后续阶段。

## Exact V1 状态

```text
P0: FROZEN
P1: FROZEN
P2.0: FROZEN
P2.0A: FROZEN AS INCLUDED REMEDIATION
P2: AUTHORIZATION APPROVED / EFFECTIVE AFTER VERIFIED MAIN PUBLICATION
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

Exact V1 全局状态保持 `FREEZE CANDIDATE`；本决策只冻结 P2.0/P2.0A scoped contract checkpoint。
