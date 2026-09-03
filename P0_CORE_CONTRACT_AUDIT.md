# P0 Core Nominal Types + Base Classes 审计报告

审计日期：2026-09-03
阶段：F6.1 Exact V1 Contract Implementation — P0
规范状态：`Exact V1 = FREEZE CANDIDATE`
阶段结论：**P0 自动验证通过，等待用户 Freeze Checkpoint；P1 尚未授权。**

## 1. 范围结论

本阶段只实现：

```text
ObjectId
LogicalId
SchemaVersion
ObjectType
CanonicalObjectClass
DIModel
FrozenDIModel
```

本阶段没有实现：

```text
ExactObjectRef
ObjectRef
LogicalObjectRef
CanonicalPayload
canonical hash / RFC 8785
Object Registry
B01-B08 exact schema
ARSO canonical primitive
Command / Event / Protocol
Resolver / Store / CAS / Snapshot fixture
```

`di_contracts_v1/` 全程保持只读 candidate baseline，没有移动、改写或提升为规范权威。

---

## 2. P0 Requirement Matrix

| ID | 冻结/适用要求 | Normative source | 测试证据 | 实现 | 状态 |
|---|---|---|---|---|---|
| P0-R01 | Python >= 3.12、Pydantic v2 | Exact Contract §3.1 | root package + full pytest | `pyproject.toml` | PASS |
| P0-R02 | `strict validation` | Exact Contract §3.1 | `test_base_model_uses_strict_validation`、`test_base_model_validates_default_values_strictly` | `DIModel` / `FrozenDIModel` | PASS |
| P0-R03 | Core canonical model `extra="forbid"` | Exact Contract §3.1 | `test_base_model_forbids_extra_fields` | `DIModel` / `FrozenDIModel` | PASS |
| P0-R04 | Core canonical model immutable / `frozen=True` | Exact Contract §3.1；历史 truth immutable | `test_frozen_model_rejects_mutation` | `FrozenDIModel` | PASS |
| P0-R05 | 区分 `ObjectId`、`LogicalId`、`SchemaVersion`、`ObjectType` | Exact Contract §5.1 | nominal runtime distinct / cross-type rejection tests | 四个独立 `RootModel[str]` | PASS |
| P0-R06 | opaque identifiers；不得把四类 identity 混成普通 string identity | Exact Contract §3.1、§5.1 | strict string / cross-nominal tests | `_NominalString` + 四个 nominal subclasses | PASS |
| P0-R07 | 七类 canonical object class wire values固定 | Exact Contract §4.1 | `test_canonical_object_class_values_match_frozen_contract` | `CanonicalObjectClass(StrEnum)` | PASS |
| P0-R08 | P0 不得提前进入 refs/hash/registry | Exact Contract §30 + 用户 P0 授权边界 | `tests/repository/test_p0_scope.py` | scope guard | PASS |
| P0-R09 | 规范源不得漂移 | `SPEC_AUTHORITY.md` + Phase 1 checksum policy | `sha256sum -c` 7/7 OK | 无规范正文修改 | PASS |

### 关于 `strict validation`

Pydantic v2 默认不会验证字段默认值。为了让“strict validation”对默认值同样成立，
P0 的 `DIModel` 使用：

```python
ConfigDict(
    extra="forbid",
    strict=True,
    validate_default=True,
)
```

`FrozenDIModel` 在此基础上增加 `frozen=True`。

---

## 3. Baseline Delta

| Candidate baseline 项 | 处理 | P0 production 结论 | 原因 |
|---|---|---|---|
| `DIModel` | `ADAPTED` | 吸收 `extra="forbid"`、`strict=True`、`validate_default=True` | 与 Global Schema Policy 一致 |
| `FrozenDIModel` | `ADAPTED` | 吸收 strict/extra/default validation，并冻结 | 与 Core canonical model policy 一致 |
| `str_strip_whitespace=False` | `REJECTED FOR P0` | 未显式迁入 | 高优先级 P0 contract 未要求；Pydantic 默认行为已是不自动 strip |
| `allow_inf_nan=False` | `DEFERRED FROM P0` | 未迁入 | 可能与 P1 canonical JSON/hash 有关，但 P0 未冻结该约束；不得提前扩大 contract |
| `ObjectId` | `ADAPTED` | 保留 nominal `RootModel[str]`；不迁入 regex | 规范冻结 nominal/opaque 语义，未冻结 lexical grammar |
| `LogicalId` | `ADAPTED` | 同上 | 同上 |
| `SchemaVersion` | `ADAPTED` | 保留 nominal type；不迁入 `MAJOR.MINOR` regex | 高优先级规范区分语义但未冻结 lexical format |
| `ObjectType` | `ADAPTED` | 保留 nominal type；不迁入 namespaced regex | 高优先级规范未冻结 namespace grammar |
| `CanonicalObjectClass` | `REUSED` | 精确复用七个 wire value | 与 Exact Contract §4.1 完全一致 |
| `ObjectClass` alias | `REJECTED` | 未创建 | 规范冻结 `object_class` 语义和值，但没有冻结该 Python alias 名称 |

---

## 4. Implementation Drift

candidate baseline 中存在以下 P0 候选约束，但没有进入正式 production P0：

```text
_OPAQUE_ID_RE
_SCHEMA_VERSION_RE
_OBJECT_TYPE_RE
allow_inf_nan=False
```

其中前三项属于 exact lexical contract 未冻结；最后一项可能在 P1 canonical serialization/hash
阶段重新评估。当前 production P0 不会把 candidate implementation 的额外限制倒灌为规范事实。

这不是 baseline regression failure：`di_contracts_v1` 自己的 46 项测试仍全部通过。

---

## 5. Remaining SPEC_GAP

### P0-GAP-01｜ObjectId / LogicalId lexical wire constraints

**状态：** `SPEC_GAP / NON-BLOCKING FOR NOMINAL SHELL`

高优先级规范要求 opaque identifier 与 nominal distinction，但没有冻结字符集、长度、前缀或编码规则。
因此 P0 不迁入 candidate baseline 的 `^[A-Za-z0-9][A-Za-z0-9._:-]{15,127}$`。

### P0-GAP-02｜SchemaVersion lexical format

**状态：** `SPEC_GAP / NON-BLOCKING FOR NOMINAL SHELL`

规范明确 `SchemaVersion != ObjectRevision`，但没有冻结 `MAJOR.MINOR`、SemVer 或其他 wire grammar。
因此 P0 不迁入 candidate baseline 的 `^[1-9][0-9]*\.[0-9]+$`。

### P0-GAP-03｜ObjectType namespace grammar

**状态：** `SPEC_GAP / NON-BLOCKING FOR NOMINAL SHELL`

规范大量使用 namespaced object type 示例，但没有给出 exact lexical grammar。
因此 P0 不迁入 candidate baseline 的 namespace regex。

### P0-GAP-04｜`object_class` Python nominal type name

**状态：** `SPEC_GAP / NON-BLOCKING IMPLEMENTATION NAME`

规范冻结字段语义与七个 wire value，但没有声明 Python type 必须叫 `ObjectClass` 或
`CanonicalObjectClass`。P0 采用 candidate baseline 已存在且无规范冲突的
`CanonicalObjectClass`，同时明确不创建额外 `ObjectClass` alias。

### SPEC_CONFLICT

```text
NONE FOUND IN P0
```

---

## 6. 自动验证证据

### P0 targeted

```bash
PYTHONPATH=src python -m pytest \
  tests/unit tests/schemas tests/repository/test_p0_scope.py -q
```

结果：

```text
24 passed
```

### Root repository regression

```bash
PYTHONPATH=src python -m pytest -q
```

结果：

```text
29 passed
```

### Candidate baseline regression

```bash
cd di_contracts_v1
python -m pytest -q
```

结果：

```text
46 passed
```

### 规范源 checksum

```bash
sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
```

结果：

```text
7 / 7 OK
```

### Compile / import

```text
src/design_intelligence compileall: PASS
P0 public core import: P0_IMPORT_PASS
```

---

## 7. P0 Public API

```python
from design_intelligence.contracts.core import (
    CanonicalObjectClass,
    DIModel,
    FrozenDIModel,
    LogicalId,
    ObjectId,
    ObjectType,
    SchemaVersion,
)
```

没有任何 P1 symbol 对外导出。

---

## 8. Freeze Checkpoint

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: COMPLETE / AUTOMATED CHECKS PASS / AWAITING USER FREEZE REVIEW
P1: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

### 用户批准 P0 之前

不得实现：

```text
ExactObjectRef
ObjectRef
LogicalObjectRef
canonical hash
RFC 8785 serializer
Object Registry
```

用户若批准 P0 Freeze Checkpoint，下一阶段才进入：

```text
P1｜Exact refs + canonical hash + registry
```
