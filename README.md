# ARSOFashion

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: COMPLETE / REVIEWED / FROZEN
P1: COMPLETE / REVIEWED / FROZEN
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已冻结 core nominal identity、canonical object class wire values 与最小 Pydantic base model policy。最终决策见 [`P0_FREEZE_DECISION.md`](P0_FREEZE_DECISION.md)。

P1 已完成 Exact refs + RFC 8785 canonical hash + registry foundation，并通过自动验证与独立 Freeze Review。最终决策见 [`P1_FREEZE_DECISION.md`](P1_FREEZE_DECISION.md)，实现审计见 [`P1_REFERENCE_HASH_REGISTRY_AUDIT.md`](P1_REFERENCE_HASH_REGISTRY_AUDIT.md)，独立复核见 [`P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md`](P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md)。

P2 尚未授权。P1 merge 后必须先独立确认 B01 owner exact contract 是否足以支持 `Full B01 Exact Schemas`；若仍存在字段级缺口，必须先执行 contract recovery / spec freeze，不得猜测实现。

## 规范入口

`specs/` 是唯一规范入口。规范优先级和冲突处理方式见 [`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

## Candidate baseline

`di_contracts_v1/` 是只读 `FREEZE CANDIDATE` executable baseline，不是规范权威。其使用限制见 [`BASELINE_POLICY.md`](BASELINE_POLICY.md)。

## 验证当前 P1 Freeze Candidate / Checkpoint

GitHub Actions workflow: `.github/workflows/p1-contracts.yml`

关键门禁：

```text
P1 targeted tests
Full root regression
Candidate baseline regression
7-source specification checksum
compileall
Non-Markdown whitespace gate
Markdown whitespace policy
Authoritative specs / candidate baseline drift gate
```

Exact V1 只有在所有 mandatory schemas、ARSO authoritative imports、完整 Command/Event/Protocol、semantic resolver、CAS、snapshot firewalls、CS-01–CS-32 与 AC-01–AC-18 全部通过且无未解决 `SPEC_CONFLICT` 后，才能从 `FREEZE CANDIDATE` 升级为 `FROZEN`。
