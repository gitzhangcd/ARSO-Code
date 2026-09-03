# ARSOFashion

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: COMPLETE / AUTOMATED CHECKS PASS / AWAITING USER FREEZE REVIEW
P1: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已实现 core nominal identity、canonical object class wire values 与最小 Pydantic
base model policy。详细证据与 baseline delta 见
[`P0_CORE_CONTRACT_AUDIT.md`](P0_CORE_CONTRACT_AUDIT.md)。

在用户批准 P0 Freeze Checkpoint 之前，不得进入 P1 refs/hash/registry。

## 规范入口

`specs/` 是唯一规范入口。规范优先级和冲突处理方式见
[`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

## Candidate baseline

`di_contracts_v1/` 是只读 `FREEZE CANDIDATE` executable baseline，不是规范权威。
其使用限制见 [`BASELINE_POLICY.md`](BASELINE_POLICY.md)。

## 验证 P0

```bash
PYTHONPATH=src python -m pytest \
  tests/unit tests/schemas tests/repository/test_p0_scope.py -q

PYTHONPATH=src python -m pytest -q

(cd di_contracts_v1 && python -m pytest -q)

sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
```

当前已验证结果：

```text
P0 targeted: 24 passed
Root repository: 29 passed
Candidate baseline: 46 passed
Spec checksums: 7 / 7 OK
```
