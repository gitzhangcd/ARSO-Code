# ARSOFashion

本仓库用于实现 Design Intelligence V5.0 的 ARSO V2.2.1 Reference Application。

## 当前阶段

```text
Phase 0: COMPLETE / REVIEWED
Phase 1: COMPLETE / AWAITING REVIEW
P0: NOT STARTED
```

Phase 1 已建立 Contract Repository Skeleton、规范路径、校验测试和版本治理，
没有实现 P0 nominal type、base contract 或任何 B01-B08 schema。进入 P0 前仍需
人工 Freeze Checkpoint。

## 规范入口

`specs/` 是唯一规范入口。规范优先级和冲突处理方式见
[`SPEC_AUTHORITY.md`](SPEC_AUTHORITY.md)。

## 现有候选基线

`di_contracts_v1/` 是 Phase 0 审计时发现的 `FREEZE CANDIDATE` 基线，
不是规范权威，也不会在 Phase 1 中直接迁移为正式 contract。具体规则见
[`BASELINE_POLICY.md`](BASELINE_POLICY.md)。

## 验证 Phase 1 骨架

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with 'pytest>=8,<9' \
  python -m pytest -p no:cacheprovider tests/repository/test_phase1_skeleton.py -q
```
