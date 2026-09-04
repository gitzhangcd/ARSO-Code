# ARSO-Code

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0A: FROZEN AS INCLUDED REMEDIATION
P2.0: FROZEN BY USER DECISION / MAIN PUBLICATION PENDING
P2: AUTHORIZATION APPROVED / EFFECTIVE AFTER VERIFIED MAIN PUBLICATION
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

Freeze decision：[`P2_0_FREEZE_DECISION.md`](P2_0_FREEZE_DECISION.md)。

## P2.0 frozen scope

B01 owner contract covers exactly seven canonical objects：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

Frozen B01 contract surface：

```text
field-level wire shape
requiredness / cardinality
reference policy
object classification
registry policy
B01 CanonicalPayload policy
semantic closure / negative ownership boundaries
```

Scoped contract：

```text
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

P2.0A closes the shared canonical-shell prerequisites：

```text
ActorId / ActorType / ActorRef
TenantId / TenantScopeType / TenantScope
Provenance
ObjectRevision
CanonicalObject structural base
CanonicalRevision structural base
ImmutableFact structural base
UTC datetime normalization
```

Scoped shared-shell contract：

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

Independent review result：

```text
SC01-SC04 = CLOSED
Critical = 0
Important = 0
Minor = 0
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
SPEC_CONFLICT = 0
P2 contract-level implementability = PASS
```

## Normative manifest

`specs/` 是唯一规范入口；权威顺序见 [`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

```text
9 / 9 normative files registered
```

原 Phase 1 sources、B01 owner contract 与 shared-core contract 都由 `specs/SPEC_SOURCE_CHECKSUMS.sha256` 固定内容。

## Candidate baseline

`di_contracts_v1/` 继续只读，仅作为 executable evidence；不得 bulk-copy 或 silent promotion。

## Verification

PR #5 final verified head：

```text
ce041aecb3af381c1349aac057b7630e243a25de
P1 run 33898835918 = SUCCESS
P2.0/P2.0A run 33898836017 = SUCCESS
```

PR #5 merge 后的 combined PR #4 head：

```text
455b1254eca17d2ecb819b66a58b86f710e4bd80
P1 run 33900293912 = SUCCESS
P2.0/P2.0A run 33900293877 = SUCCESS
```

Freeze-decision/governance commit 之后必须再次 fresh verify exact PR #4 head，之后才允许 merge 到 `main`。

## P2 authorization

用户已经批准 P2｜Full B01 Exact Schemas，但授权只在以下条件全部完成后生效：

```text
P2.0 freeze-decision head verification PASS
-> PR #4 merged to main with expected-head protection
-> resulting main checkpoint fresh verification PASS
-> P2 = AUTHORIZED
```

在此之前禁止新增 `src/design_intelligence/contracts/b01/*.py` production implementation。

Exact V1 全局状态仍为 `FREEZE CANDIDATE`；只有完整 mandatory schemas、ARSO imports、Command/Event/Protocol、resolver、CAS、snapshot firewalls、CS-01–CS-32 与 AC-01–AC-18 全部通过且无 unresolved `SPEC_CONFLICT` 后才可全局冻结。
