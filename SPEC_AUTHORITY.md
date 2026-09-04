# Exact V1 规范权威说明

审计日期：2026-09-05  
仓库：ARSO-Code  
阶段：规范摄取、冻结治理与 Exact V1 分阶段实现  
结论：P0、P1、P2.0/P2.0A 已获人工 Freeze；P2 授权已获批准，但只有在 P2.0 checkpoint 发布到 `main` 并完成 fresh verification 后生效；Exact V1 全局仍为 `FREEZE CANDIDATE`。

## 规范入口与 manifest

`specs/` 是唯一规范入口。

当前 normative manifest：

```text
9 / 9 files
```

组成：Phase 1 的 7 份原始来源 + shared canonical-shell scoped contract + B01 scoped owner contract。

## 规范权威顺序

| 优先级 | 仓库内规范 | scoped status | 规范职责 |
|---:|---|---|---|
| 1A | `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md` | Global Exact V1 `FREEZE CANDIDATE` | 全局 normalization、cross-domain invariants、CS/AC release gates。 |
| 1B | `specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md` | `FROZEN` by `P2_0_FREEZE_DECISION.md` | Shared support/nested types 与 CanonicalObject/CanonicalRevision structural shell。 |
| 1C | `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md` | `FROZEN` by `P2_0_FREEZE_DECISION.md` | B01 field-level owner contract；消费 1B shared shell。 |
| 2 | `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt` | upstream authority | 工程、运行时、对象所有权与边界。 |
| 3 | `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt` | upstream freeze authority | normalization 与跨规范冻结边界。 |
| 4 | `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt` | upstream authority | ARSO primitive 与集成边界 canonical owner。 |
| 5 | `specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt` | upstream | 产品语义与 B01-B08 应用职责。 |
| 6 | `specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt` | upstream | 集成蓝图与实施背景。 |
| 7 | `specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt` | research | 科学依据与研究主张边界。 |

重要说明：1B/1C 文件头仍保留其 recovery 生成时的 `V1.0-FC1 / FREEZE CANDIDATE` 文档身份；`P2_0_FREEZE_DECISION.md` 冻结的是这些 **exact bytes / checksum-registered scoped contracts**。不得通过直接改写已登记 contract 状态文本来绕过 checksum / review history。

Rules：

```text
1B MUST NOT override 1A.
1C MUST NOT override 1A/1B.
1B support types are not new canonical domain primitives.
2+ MUST NOT override frozen 1A/1B/1C scope.
```

## 解析规则

1. 先查 1A global Exact Contract。
2. Canonical shell support internals 查 1B。
3. B01 business/design field-level contract 查 1C。
4. 1B/1C 的 frozen status 由 `P2_0_FREEZE_DECISION.md` 与 checksum-registered bytes 共同确定。
5. 未定义区域按 2→7 恢复；缺 exact contract → `SPEC_GAP`，不得从 candidate baseline 猜测。
6. 真实不可兼容要求 → `SPEC_CONFLICT` 并停止 affected path。
7. `OPEN` / `DEFERRED` 不因实现便利自动升级。

## P2.0 frozen scope

### B01 owner layer

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

冻结：

```text
field-level wire shapes
requiredness / cardinality
persistent reference policy
object classification
registry policy
B01 CanonicalPayload policy
semantic closure
negative ownership/runtime boundaries
```

### Shared canonical shell remediation

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

关键 invariants：

```text
ActorType = open typed vocabulary
TenantScopeType = GLOBAL | TENANT
GLOBAL != public/permissionless
Provenance.command_ref:ObjectRef = forbidden
Provenance.run_ref:ObjectRef = deferred
ObjectRevision = integer >= 1 ordering metadata
parentage = parent_refs
support/nested/structural types != canonical domain primitives
```

## Freeze evidence

```text
P2_0_FREEZE_DECISION.md
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
B01_P2_0_FREEZE_REVIEW.md
SHARED_CORE_SOURCE_RECOVERY_MATRIX.md
SHARED_CORE_FIELD_DECISION_LEDGER.md
SHARED_CORE_CROSS_SPEC_FREEZE_AUDIT.md
P2_0A_FREEZE_REVIEW.md
```

Review result：

```text
7 / 7 B01 objects covered
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
SC01-SC04 = CLOSED
SPEC_CONFLICT = 0
P2.0A Critical = 0
P2.0A Important = 0
P2.0A Minor = 0
P2 contract-level implementability = PASS
```

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

## P2 activation gate

用户已明确批准 `P2｜Full B01 Exact Schemas`，但必须按顺序完成：

```text
P2_0_FREEZE_DECISION committed
-> exact decision head verification PASS
-> PR #4 merge to main with expected-head protection
-> resulting main checkpoint fresh verification PASS
-> P2 authorization becomes effective
```

P2 生效后只能在独立 P2 branch 上进入 planning/TDD/implementation；不得直接在 `main` 编写 P2 production models。

## Exact V1 最终发布规则

只有 mandatory schemas、authoritative ARSO imports、完整 Command/Event/Protocol、semantic resolver、CAS、snapshot firewalls、CS-01–CS-32、AC-01–AC-18 全部通过且不存在 unresolved `SPEC_CONFLICT` 时，Exact V1 才能全局从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
