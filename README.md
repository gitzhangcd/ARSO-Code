# ARSOFashion

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: COMPLETE / REVIEWED / FROZEN
P1: COMPLETE / AUTOMATED CHECKS PASS / INDEPENDENT FREEZE REVIEW PASS / AWAITING USER FREEZE REVIEW
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

P0 已实现并冻结 core nominal identity、canonical object class wire values 与最小 Pydantic
base model policy。最终 Freeze 决策见 [`P0_FREEZE_DECISION.md`](P0_FREEZE_DECISION.md)，
实现审计与 baseline delta 见 [`P0_CORE_CONTRACT_AUDIT.md`](P0_CORE_CONTRACT_AUDIT.md)。

P1 已完成 Exact refs + RFC 8785 canonical hash + registry foundation 的 TDD 实现、自动验证与独立二次 Freeze Review。
实现审计见 [`P1_REFERENCE_HASH_REGISTRY_AUDIT.md`](P1_REFERENCE_HASH_REGISTRY_AUDIT.md)，
独立 review 见 [`P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md`](P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md)。
P1 尚未由用户标记为 `FROZEN`；在用户 Freeze Checkpoint 之前不得进入 P2。

## 规范入口

`specs/` 是唯一规范入口。规范优先级和冲突处理方式见
[`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

## Candidate baseline

`di_contracts_v1/` 是只读 `FREEZE CANDIDATE` executable baseline，不是规范权威。
其使用限制见 [`BASELINE_POLICY.md`](BASELINE_POLICY.md)。

## 验证 P1 Freeze Candidate

```bash
PYTHONPATH=src python -m pytest \
  tests/unit/test_p1_refs.py \
  tests/schemas/test_p1_reference_schemas.py \
  tests/hashing \
  tests/cross_language \
  tests/registry \
  tests/repository/test_p1_scope.py -q

PYTHONPATH=src python -m pytest -q

(cd di_contracts_v1 && PYTHONPATH=. python -m pytest -q)

sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
python -m compileall -q src/design_intelligence
```

PR #3 在 implementation head `c3fa772` 上的最终功能验证结果：

```text
P1 targeted: 49 passed
Root repository: 76 passed
Candidate baseline: 46 passed
Spec checksums: 7 / 7 OK
Compile: PASS
Patch whitespace gates: PASS
Authoritative specs/baseline drift: PASS / NO CHANGES
```

Audit、Freeze Review 与状态文档提交后，最终 Freeze 决策必须再次引用当前 PR final head 的 fresh CI evidence。
