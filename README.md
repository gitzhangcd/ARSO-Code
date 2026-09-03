# ARSOFashion

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: COMPLETE / REVIEWED / FROZEN
P1: AUTHORIZED / DESIGN IN PROGRESS
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已实现并冻结 core nominal identity、canonical object class wire values 与最小 Pydantic
base model policy。最终 Freeze 决策见 [`P0_FREEZE_DECISION.md`](P0_FREEZE_DECISION.md)，
实现审计与 baseline delta 见 [`P0_CORE_CONTRACT_AUDIT.md`](P0_CORE_CONTRACT_AUDIT.md)。

P1 已获授权，范围是 Exact refs + RFC 8785 canonical hash + registry foundation。
P1 必须先完成设计/规范消歧，再按 TDD 实现；在 P1 Freeze 前不得进入 P2。

## 规范入口

`specs/` 是唯一规范入口。规范优先级和冲突处理方式见
[`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

## Candidate baseline

`di_contracts_v1/` 是只读 `FREEZE CANDIDATE` executable baseline，不是规范权威。
其使用限制见 [`BASELINE_POLICY.md`](BASELINE_POLICY.md)。

## 验证 P0 Frozen Checkpoint

```bash
PYTHONPATH=src python -m pytest \
  tests/unit tests/schemas tests/repository/test_p0_scope.py -q

PYTHONPATH=src python -m pytest -q

(cd di_contracts_v1 && python -m pytest -q)

sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
```

P0 Freeze Review 的验证结果：

```text
P0 targeted: 24 passed
Root repository: 29 passed
Candidate baseline: 46 passed
Spec checksums: 7 / 7 OK
Non-core AST class scan: 0 classes
```
