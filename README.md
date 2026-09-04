# ARSO-Code

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0: RECOVERY IMPLEMENTATION COMPLETE / FINAL VERIFICATION IN PROGRESS
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已冻结 core nominal identity、canonical object class wire values 与最小 Pydantic base-model policy。最终决策见 [`P0_FREEZE_DECISION.md`](P0_FREEZE_DECISION.md)。

P1 已冻结 Exact refs + RFC 8785 canonical hash + registry foundation。最终决策见 [`P1_FREEZE_DECISION.md`](P1_FREEZE_DECISION.md)，实现审计见 [`P1_REFERENCE_HASH_REGISTRY_AUDIT.md`](P1_REFERENCE_HASH_REGISTRY_AUDIT.md)，独立复核见 [`P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md`](P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md)。

## P2.0｜B01 Contract Recovery

P2.0 只处理 B01 owner-contract recovery，不包含 production Python schemas。

当前 recovery artifacts：

```text
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md
```

`DI-B01-EXACT-CONTRACT` 覆盖 exactly seven B01 objects：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

当前 recovery candidate 已得到：

```text
7 / 7 object coverage
SPEC_CONFLICT = 0
blocking B01 field-level SPEC_GAP = 0
```

但 P2.0 尚未经过最终 independent Freeze Checkpoint，因此 **P2 仍未授权**，不得实现 `src/design_intelligence/contracts/b01/*.py`。

## 规范入口

`specs/` 是唯一规范入口，优先级见 [`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

Phase 1 的 7 个原始 source checksum 保持不变；P2.0 新增 scoped `DI-B01-EXACT-CONTRACT` 后，`specs/SPEC_SOURCE_CHECKSUMS.sha256` 现在验证 `8 / 8` normative files。

## Candidate baseline

`di_contracts_v1/` 是只读 `FREEZE CANDIDATE` executable evidence，不是规范权威。禁止 bulk-copy 或把 candidate-only field/registry value 静默升级成 owner truth。

## Verification

P1 frozen verification：`.github/workflows/p1-contracts.yml`。  
P2.0 B01 contract-freeze verification：`.github/workflows/p2-0-b01-contract-freeze.yml`。

P2.0 关键门禁包括：

```text
8 / 8 normative checksum
7 / 7 B01 owner-contract surface
No B01 production implementation leakage
P0/P1 root regression
candidate baseline regression
compileall
placeholder scan
whitespace policy
scoped authority-source change gate
```

Exact V1 只有在所有 mandatory schemas、ARSO authoritative imports、完整 Command/Event/Protocol、resolver、CAS、snapshot firewalls、CS-01–CS-32 与 AC-01–AC-18 全部通过且没有 unresolved `SPEC_CONFLICT` 后，才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
