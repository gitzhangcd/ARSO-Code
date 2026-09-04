# ARSO-Code

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: FROZEN
P1: FROZEN
P2.0: B01 OWNER-FIELD RECOVERY PASS / FREEZE BLOCKED BY SHARED-CORE SPEC_GAP
P2.0A: RECOMMENDED / NOT AUTHORIZED
P2: NOT AUTHORIZED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已冻结 core nominal identity、canonical object class wire values 与最小 Pydantic base-model policy。最终决策见 [`P0_FREEZE_DECISION.md`](P0_FREEZE_DECISION.md)。

P1 已冻结 Exact refs + RFC 8785 canonical hash + registry foundation。最终决策见 [`P1_FREEZE_DECISION.md`](P1_FREEZE_DECISION.md)。

## P2.0｜B01 Contract Recovery

P2.0 已完成 B01 owner-field recovery，且没有写 production Python schemas。

Recovery / review artifacts：

```text
B01_SOURCE_RECOVERY_MATRIX.md
B01_FIELD_DECISION_LEDGER.md
B01_CROSS_SPEC_FREEZE_AUDIT.md
B01_P2_0_FREEZE_REVIEW.md
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

B01 owner-field recovery 结果：

```text
7 / 7 object coverage
B01 SPEC_CONFLICT = 0
blocking B01 owner-field SPEC_GAP = 0
P2.0 automated verification = PASS
```

独立 Freeze Review 进一步发现 shared canonical-shell exact contract 尚不完整：

```text
P2.0-SC01 ActorRef exact wire contract missing
P2.0-SC02 TenantScope exact wire contract missing
P2.0-SC03 Provenance exact wire contract missing
P2.0-SC04 ObjectRevision exact wire contract missing
```

这些不是 B01 primitive-ownership gap，但每个 B01 canonical model 都依赖该 shared shell，因此当前仍不能在“不猜 contract”的前提下实现完整 P2 schemas。

结论：

```text
P2.0 FREEZE = BLOCKED
P2 = NOT AUTHORIZED
```

推荐下一规范阶段：

```text
P2.0A｜Shared Canonical Shell Support Contract Recovery
```

在 P2.0A 获得独立授权前不得自行从 `di_contracts_v1` 复制 `ActorRef / TenantScope / Provenance / ObjectRevision` 等 candidate structure。

## 规范入口

`specs/` 是唯一规范入口，优先级见 [`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

Phase 1 的 7 个原始 source checksum 保持不变；P2.0 新增 scoped `DI-B01-EXACT-CONTRACT` 后，`specs/SPEC_SOURCE_CHECKSUMS.sha256` 验证 `8 / 8` normative files。

## Candidate baseline

`di_contracts_v1/` 是只读 `FREEZE CANDIDATE` executable evidence，不是规范权威。禁止 bulk-copy 或把 candidate-only field/registry value 静默升级成 owner truth。

## Verification

P1 regression：`.github/workflows/p1-contracts.yml`。  
P2.0 scoped verification：`.github/workflows/p2-0-b01-contract-freeze.yml`。

在独立 Review 前的 head `2c75d9db4959cf0191ca0cce8065893c5100a399` 上：

```text
P2.0 workflow run 33887779202 = SUCCESS
P1 regression run 33887779153 = SUCCESS
8 / 8 normative checksums = PASS
7 / 7 B01 surface = PASS
No B01 production implementation leakage = PASS
```

自动门禁通过不能覆盖独立规范审查发现的 shared-core `SPEC_GAP`。

Exact V1 只有在所有 mandatory schemas、ARSO authoritative imports、完整 Command/Event/Protocol、resolver、CAS、snapshot firewalls、CS-01–CS-32 与 AC-01–AC-18 全部通过且没有 unresolved `SPEC_CONFLICT` 后，才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
