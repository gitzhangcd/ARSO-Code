# ARSO-Code

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0A: RECOVERY PASS / INDEPENDENT REVIEW PASS / NOT FROZEN
P2.0: B01 RECOVERY PASS / RE-REVIEW PASS / READY FOR USER FREEZE DECISION
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已冻结 core nominal identity / object-class wire values / base-model policy。  
P1 已冻结 Exact refs + RFC 8785 canonical hash + registry foundation。

## P2.0｜B01 Contract Recovery

B01 owner-field recovery 已覆盖 exactly seven canonical objects：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

结果：

```text
7 / 7 object coverage
B01 owner-field SPEC_GAP = 0
B01 SPEC_CONFLICT = 0
```

## P2.0A｜Shared Canonical Shell Recovery

Scoped candidate：

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

Independent Review 已关闭：

```text
SC01 ActorRef
SC02 TenantScope
SC03 Provenance
SC04 ObjectRevision
```

并冻结候选：

```text
ActorId / ActorType
TenantId / TenantScopeType
CanonicalObject structural base
CanonicalRevision structural base
ImmutableFact structural base
UTC canonical timestamp normalization
```

关键边界：

```text
ActorType = open typed vocabulary
TenantScopeType = GLOBAL | TENANT
GLOBAL != public/permissionless
Provenance.command_ref:ObjectRef = rejected
Provenance.run_ref:ObjectRef = deferred
ObjectRevision = integer >=1 ordering metadata
parentage = parent_refs
```

P2.0A evidence：

```text
SHARED_CORE_SOURCE_RECOVERY_MATRIX.md
SHARED_CORE_FIELD_DECISION_LEDGER.md
SHARED_CORE_CROSS_SPEC_FREEZE_AUDIT.md
P2_0A_FREEZE_REVIEW.md
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

Independent result：

```text
Critical = 0
Important = 0
Minor = 0
shared-core blocking SPEC_GAP = 0
SPEC_CONFLICT = 0
```

## P2.0 Re-review

`B01_P2_0_FREEZE_REVIEW.md` 已完成 remediation re-review：

```text
SC01-SC04 = CLOSED
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
P2 contract-level implementability = PASS
P2.0 independent re-review = PASS
```

因此当前：

```text
P2.0 = READY FOR USER FREEZE DECISION
P2.0 != FROZEN
P2 = NOT AUTHORIZED
```

## 规范与 checksum

`specs/` 是唯一规范入口，权威顺序见 [`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

当前 normative manifest：

```text
9 / 9 files
```

原 Phase 1 sources 与 B01 contract digest 保持不变；shared canonical-shell contract 作为第 9 个 scoped normative candidate 登记。

## Candidate baseline

`di_contracts_v1/` 只读、只作为 executable evidence，不是 normative authority。禁止 bulk-copy 或 silent promotion。

## Verification

- P1 regression：`.github/workflows/p1-contracts.yml`
- P2.0/P2.0A scoped verification：`.github/workflows/p2-0-b01-contract-freeze.yml`

P2.0/P2.0A gate 证明：

```text
9 / 9 normative checksums
B01 7 / 7 surface
shared-core required surface
no original-source drift
no candidate-baseline drift
no production core/B01 leakage
P0/P1 regression
compile / placeholder / whitespace / authority-scope gates
```

下一治理动作必须由用户明确批准：

```text
P2.0 Freeze
-> merge PR #5 into PR #4 branch
-> fresh PR #4 verification
-> record freeze decision
-> merge PR #4 to main
-> verify main
-> then authorize P2 explicitly
```

Exact V1 只有在 mandatory schemas、ARSO imports、Command/Event/Protocol、resolver、CAS、snapshot firewalls、CS-01–CS-32 与 AC-01–AC-18 全部通过且没有 unresolved `SPEC_CONFLICT` 后，才能升级为 `FROZEN`。
