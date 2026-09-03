# P0 Core Nominal Types + Base Classes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 在不进入 P1 的前提下，实现 Exact V1 已冻结的 P0 nominal identity type、canonical object class 值与最小 Pydantic base model policy，并留下可审计的 TDD/回归证据。

**Architecture:** P0 只在 `src/design_intelligence/contracts/core/` 建立基础类型和 base model，不实现 refs/hash/registry。Nominal identity 使用互不相同的 `RootModel[str]` runtime 类型；canonical domain model 通过 `FrozenDIModel` 固化 `extra="forbid"`、`strict=True`、`frozen=True`。对高优先级规范未冻结的 ID/SchemaVersion/ObjectType lexical regex 不从 candidate baseline 擅自继承，而是在阶段审计中记录为 `SPEC_GAP`/baseline delta。

**Tech Stack:** Python >= 3.12、Pydantic v2、pytest 8.x、Git（沙箱工作副本分支 `p0-core-contracts`）。

**Spec:** `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`

## Global Constraints

- 规范权威顺序严格遵守 `AGENTS.md` 与 `SPEC_AUTHORITY.md`。
- `di_contracts_v1/` 只读、只用于差异分析和 46-test regression；不得修改。
- P0 只实现 nominal types + base classes；P1 的 `ExactObjectRef`、`ObjectRef`、`LogicalObjectRef`、canonical hash、registry 明确禁止。
- Global schema policy：Python >= 3.12、Pydantic v2、opaque identifiers、strict validation。
- Core canonical Pydantic models：`extra="forbid"`、`frozen=True`。
- Nominal identity 必须区分 `ObjectId`、`LogicalId`、`SchemaVersion`、`ObjectType`；`ID != LogicalID != Revision != SchemaVersion`。
- Object class wire values固定为：`CANONICAL_REVISION`、`IMMUTABLE_FACT`、`IMMUTABLE_ROOT`、`IMMUTABLE_GRAPH_NODE`、`SNAPSHOT`、`OPERATIONAL_CONTROL_STATE`、`DERIVED_VIEW`。
- 最高优先级规范未冻结 Python 类型名 `ObjectClass`；实现使用 baseline 已存在且不冲突的 `CanonicalObjectClass` 名称，不创建额外 alias。
- 不修改 7 份规范正文与 `specs/SPEC_SOURCE_CHECKSUMS.sha256`。

---

### Task 1: Phase transition governance + P0 scope guard

**Files:**
- Create: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `SPEC_AUTHORITY.md`
- Modify: `PHASE_1_SKELETON_AUDIT.md`
- Modify: `tests/repository/test_phase1_skeleton.py`
- Create: `tests/repository/test_p0_scope.py`

**Interfaces:**
- Consumes: 用户已批准 Phase 1 Freeze Checkpoint 并授权进入 P0。
- Produces: 当前阶段状态 `P0: AUTHORIZED / IN PROGRESS`，以及禁止 P1 符号提前出现的 repository guard。

- [x] **Step 1: 创建 `.gitignore`，避免沙箱工作副本把 cache/构建物纳入版本控制**

```gitignore
.DS_Store
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
dist/
build/
*.egg-info/
```

- [x] **Step 2: 更新治理文档的当前阶段状态，不重写历史审计结论**

`AGENTS.md` 当前说明改为：Phase 0/1 已完成并经用户批准；P0 已授权；P0 Freeze 前不得进入 P1。

`SPEC_AUTHORITY.md` 当前阶段门禁改为：

```text
Phase 0: COMPLETE / REVIEWED / APPROVED
Phase 1: COMPLETE / VERIFIED / FROZEN
P0: AUTHORIZED / IN PROGRESS
P1: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

`PHASE_1_SKELETON_AUDIT.md` 只追加“人工评审结果”小节，保留原自动验证快照：

```text
User Freeze Review: APPROVED
Phase 1: FROZEN
P0: AUTHORIZED
```

- [x] **Step 3: 将 Phase 1 的永久 `no class` 断言改为历史骨架约束**

删除 `test_phase1_does_not_implement_contract_types()`，避免它与已授权 P0 冲突；其历史结果继续由 `PHASE_1_SKELETON_AUDIT.md` 保留。

- [x] **Step 4: 写 P0 scope guard（RED）**

`tests/repository/test_p0_scope.py`：

```python
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "src" / "design_intelligence" / "contracts" / "core"

P0_REQUIRED_SYMBOLS = (
    "ObjectId",
    "LogicalId",
    "SchemaVersion",
    "ObjectType",
    "CanonicalObjectClass",
    "DIModel",
    "FrozenDIModel",
)

P1_FORBIDDEN_SYMBOLS = (
    "ExactObjectRef",
    "ObjectRef",
    "LogicalObjectRef",
    "CanonicalPayload",
    "canonical_hash",
    "compute_content_hash",
    "ObjectRegistry",
)


def test_p0_required_core_symbols_are_present() -> None:
    text = "\n".join(path.read_text(encoding="utf-8") for path in CORE.glob("*.py"))
    for symbol in P0_REQUIRED_SYMBOLS:
        assert symbol in text


def test_p1_symbols_are_not_implemented_early() -> None:
    source_root = ROOT / "src" / "design_intelligence"
    text = "\n".join(path.read_text(encoding="utf-8") for path in source_root.rglob("*.py"))
    for symbol in P1_FORBIDDEN_SYMBOLS:
        assert symbol not in text


def test_non_core_contract_namespaces_remain_skeleton_only() -> None:
    source_root = ROOT / "src" / "design_intelligence"
    for path in source_root.rglob("*.py"):
        if CORE in path.parents or path == CORE / "__init__.py":
            continue
        text = path.read_text(encoding="utf-8")
        assert "BaseModel" not in text
        assert "RootModel" not in text
```

- [x] **Step 5: 运行 RED 测试**

Run:

```bash
PYTHONPATH=src python -m pytest tests/repository/test_p0_scope.py -q
```

Expected: `test_p0_required_core_symbols_are_present` FAIL；其余 scope guard PASS。

---

### Task 2: Base Pydantic model policy

**Files:**
- Create: `tests/unit/test_core_base_models.py`
- Create: `src/design_intelligence/contracts/core/base.py`

**Interfaces:**
- Consumes: Pydantic v2 `BaseModel`, `ConfigDict`。
- Produces: `DIModel` 与 `FrozenDIModel`，后续 P1+ canonical model 依赖这两个基础类。

- [x] **Step 1: 写 base model 行为测试（RED）**

```python
import pytest
from pydantic import ValidationError

from design_intelligence.contracts.core.base import DIModel, FrozenDIModel


class StrictProbe(DIModel):
    count: int


class CanonicalProbe(FrozenDIModel):
    name: str


def test_base_model_forbids_extra_fields() -> None:
    with pytest.raises(ValidationError):
        StrictProbe(count=1, extra_field=True)


def test_base_model_uses_strict_validation() -> None:
    with pytest.raises(ValidationError):
        StrictProbe(count="1")


def test_frozen_model_rejects_mutation() -> None:
    probe = CanonicalProbe(name="alpha")
    with pytest.raises(ValidationError):
        probe.name = "beta"


def test_frozen_model_inherits_strict_and_extra_forbid() -> None:
    with pytest.raises(ValidationError):
        CanonicalProbe(name=123)
    with pytest.raises(ValidationError):
        CanonicalProbe(name="alpha", unexpected="x")
```

- [x] **Step 2: 运行测试并确认因 module 缺失而 RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/unit/test_core_base_models.py -q
```

Expected: collection/import ERROR because `core.base` 尚不存在。修正测试导入路径以确保真正的 feature-missing RED 后继续。

- [x] **Step 3: 最小实现 `base.py`**

```python
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class DIModel(BaseModel):
    """Strict Pydantic base for DI contract DTOs."""

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )


class FrozenDIModel(DIModel):
    """Immutable base for canonical historical contract models."""

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        frozen=True,
    )
```

- [x] **Step 4: 运行 GREEN**

Run:

```bash
PYTHONPATH=src python -m pytest tests/unit/test_core_base_models.py -q
```

Expected: `4 passed`。

---

### Task 3: Nominal identity runtime types

**Files:**
- Create: `tests/unit/test_core_nominal_types.py`
- Create: `src/design_intelligence/contracts/core/types.py`

**Interfaces:**
- Consumes: Pydantic v2 `RootModel`, `ConfigDict`。
- Produces: `ObjectId`, `LogicalId`, `SchemaVersion`, `ObjectType`。

- [x] **Step 1: 写 nominal identity 测试（RED）**

```python
import pytest
from pydantic import BaseModel, ConfigDict, ValidationError

from design_intelligence.contracts.core.types import LogicalId, ObjectId, ObjectType, SchemaVersion


class IdentityProbe(BaseModel):
    model_config = ConfigDict(strict=True)
    object_id: ObjectId
    logical_id: LogicalId
    schema_version: SchemaVersion
    object_type: ObjectType


def test_nominal_identity_types_are_runtime_distinct() -> None:
    assert ObjectId is not LogicalId
    assert ObjectId is not SchemaVersion
    assert LogicalId is not SchemaVersion
    assert ObjectType is not SchemaVersion


def test_nominal_identity_accepts_strict_strings() -> None:
    probe = IdentityProbe(
        object_id="object-opaque-value",
        logical_id="logical-opaque-value",
        schema_version="candidate-version",
        object_type="candidate.object.type",
    )
    assert isinstance(probe.object_id, ObjectId)
    assert isinstance(probe.logical_id, LogicalId)
    assert isinstance(probe.schema_version, SchemaVersion)
    assert isinstance(probe.object_type, ObjectType)


def test_nominal_identity_rejects_non_strings() -> None:
    with pytest.raises(ValidationError):
        ObjectId(123)
    with pytest.raises(ValidationError):
        LogicalId(123)
    with pytest.raises(ValidationError):
        SchemaVersion(123)
    with pytest.raises(ValidationError):
        ObjectType(123)


def test_nominal_identity_rejects_cross_type_instances() -> None:
    object_id = ObjectId("object-opaque-value")
    with pytest.raises(ValidationError):
        IdentityProbe(
            object_id=object_id,
            logical_id=object_id,
            schema_version="candidate-version",
            object_type="candidate.object.type",
        )


def test_nominal_identity_values_are_frozen() -> None:
    object_id = ObjectId("object-opaque-value")
    with pytest.raises(ValidationError):
        object_id.root = "changed"
```

- [x] **Step 2: 运行 RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/unit/test_core_nominal_types.py -q
```

Expected: import ERROR because `core.types` 尚不存在。

- [x] **Step 3: 最小实现 nominal string shell，不引入 baseline regex**

```python
from __future__ import annotations

from pydantic import ConfigDict, RootModel


class _NominalString(RootModel[str]):
    model_config = ConfigDict(strict=True, frozen=True)


class ObjectId(_NominalString):
    """Opaque identity of one exact immutable object/version."""


class LogicalId(_NominalString):
    """Long-lived identity of one logical entity."""


class SchemaVersion(_NominalString):
    """Nominal schema-version identity; lexical format is not frozen in P0 authority."""


class ObjectType(_NominalString):
    """Nominal canonical object-type identity; lexical format is not frozen in P0 authority."""
```

- [x] **Step 4: 运行 GREEN**

Run:

```bash
PYTHONPATH=src python -m pytest tests/unit/test_core_nominal_types.py -q
```

Expected: `5 passed`。

---

### Task 4: Canonical object class wire values + public core exports

**Files:**
- Create: `tests/unit/test_core_object_class.py`
- Modify: `src/design_intelligence/contracts/core/types.py`
- Modify: `src/design_intelligence/contracts/core/__init__.py`
- Modify: `src/design_intelligence/contracts/__init__.py`

**Interfaces:**
- Consumes: Python `enum.StrEnum`。
- Produces: `CanonicalObjectClass` exact seven-value enum and explicit core exports。

- [x] **Step 1: 写 object class 测试（RED）**

```python
from design_intelligence.contracts.core.types import CanonicalObjectClass


def test_canonical_object_class_values_match_frozen_contract() -> None:
    assert {member.value for member in CanonicalObjectClass} == {
        "CANONICAL_REVISION",
        "IMMUTABLE_FACT",
        "IMMUTABLE_ROOT",
        "IMMUTABLE_GRAPH_NODE",
        "SNAPSHOT",
        "OPERATIONAL_CONTROL_STATE",
        "DERIVED_VIEW",
    }


def test_canonical_object_class_is_string_enum() -> None:
    assert CanonicalObjectClass.CANONICAL_REVISION == "CANONICAL_REVISION"
```

- [x] **Step 2: 运行 RED**

Run:

```bash
PYTHONPATH=src python -m pytest tests/unit/test_core_object_class.py -q
```

Expected: import ERROR，因为 enum 尚不存在。

- [x] **Step 3: 在 `types.py` 添加 exact seven-value enum**

```python
from enum import StrEnum


class CanonicalObjectClass(StrEnum):
    CANONICAL_REVISION = "CANONICAL_REVISION"
    IMMUTABLE_FACT = "IMMUTABLE_FACT"
    IMMUTABLE_ROOT = "IMMUTABLE_ROOT"
    IMMUTABLE_GRAPH_NODE = "IMMUTABLE_GRAPH_NODE"
    SNAPSHOT = "SNAPSHOT"
    OPERATIONAL_CONTROL_STATE = "OPERATIONAL_CONTROL_STATE"
    DERIVED_VIEW = "DERIVED_VIEW"
```

- [x] **Step 4: 显式导出 P0 public API**

`core/__init__.py`：

```python
from .base import DIModel, FrozenDIModel
from .types import CanonicalObjectClass, LogicalId, ObjectId, ObjectType, SchemaVersion

__all__ = [
    "CanonicalObjectClass",
    "DIModel",
    "FrozenDIModel",
    "LogicalId",
    "ObjectId",
    "ObjectType",
    "SchemaVersion",
]
```

`contracts/__init__.py` 保持 namespace 边界，仅从 `.core` 显式 re-export 同一组 P0 symbols；不得导出任何 P1+ symbol。

- [x] **Step 5: 运行 GREEN + P0 scope guard**

Run:

```bash
PYTHONPATH=src python -m pytest \
  tests/unit/test_core_base_models.py \
  tests/unit/test_core_nominal_types.py \
  tests/unit/test_core_object_class.py \
  tests/repository/test_p0_scope.py -q
```

Expected: all PASS。

---

### Task 5: P0 JSON Schema behavior tests

**Files:**
- Create: `tests/schemas/test_p0_core_schemas.py`

**Interfaces:**
- Consumes: P0 RootModel types and enum。
- Produces: schema-level evidence that nominal IDs remain separate named string schemas and object class enum values are exact。

- [x] **Step 1: 写 schema behavior tests**

```python
from pydantic import BaseModel

from design_intelligence.contracts.core.types import (
    CanonicalObjectClass,
    LogicalId,
    ObjectId,
    ObjectType,
    SchemaVersion,
)


class SchemaProbe(BaseModel):
    object_id: ObjectId
    logical_id: LogicalId
    schema_version: SchemaVersion
    object_type: ObjectType
    object_class: CanonicalObjectClass


def test_nominal_types_generate_distinct_named_definitions() -> None:
    schema = SchemaProbe.model_json_schema()
    defs = schema["$defs"]
    assert {"ObjectId", "LogicalId", "SchemaVersion", "ObjectType"}.issubset(defs)
    for name in ("ObjectId", "LogicalId", "SchemaVersion", "ObjectType"):
        assert defs[name]["type"] == "string"


def test_object_class_schema_has_exact_wire_enum() -> None:
    schema = SchemaProbe.model_json_schema()
    enum_values = set(schema["$defs"]["CanonicalObjectClass"]["enum"])
    assert enum_values == {
        "CANONICAL_REVISION",
        "IMMUTABLE_FACT",
        "IMMUTABLE_ROOT",
        "IMMUTABLE_GRAPH_NODE",
        "SNAPSHOT",
        "OPERATIONAL_CONTROL_STATE",
        "DERIVED_VIEW",
    }
```

- [x] **Step 2: 运行 schema tests**

Run:

```bash
PYTHONPATH=src python -m pytest tests/schemas/test_p0_core_schemas.py -q
```

Expected: `2 passed`。如果 Pydantic schema shape 与预期不同，只能调整测试到等价的规范行为，不得添加未冻结 lexical pattern。

---

### Task 6: P0 audit, baseline delta, and full regression

**Files:**
- Create: `P0_CORE_CONTRACT_AUDIT.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: P0 implementation + all fresh test evidence。
- Produces: P0 Requirement Matrix、Baseline Delta、Implementation Drift、Remaining SPEC_GAP、Freeze Checkpoint。

- [x] **Step 1: 运行 P0 tests**

Run:

```bash
PYTHONPATH=src python -m pytest \
  tests/unit \
  tests/schemas \
  tests/repository/test_p0_scope.py -q
```

Expected: 0 failures。

- [x] **Step 2: 运行完整 root repository regression**

Run:

```bash
PYTHONPATH=src python -m pytest -q
```

Expected: 0 failures。

- [x] **Step 3: 运行只读 candidate baseline regression**

Run:

```bash
cd di_contracts_v1 && python -m pytest -q
```

Expected: `46 passed`。

- [x] **Step 4: 验证规范 checksum 未漂移**

Run:

```bash
sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
```

Expected: 7 个 `OK`。

- [x] **Step 5: 验证 P1 forbidden symbol absence + package compile/import**

Run:

```bash
PYTHONPATH=src python -m compileall -q src/design_intelligence
PYTHONPATH=src python - <<'PY'
from design_intelligence.contracts.core import (
    CanonicalObjectClass, DIModel, FrozenDIModel,
    LogicalId, ObjectId, ObjectType, SchemaVersion,
)
print("P0_IMPORT_PASS")
PY
```

Expected: compile exit 0 and `P0_IMPORT_PASS`。

- [x] **Step 6: 写 `P0_CORE_CONTRACT_AUDIT.md`**

报告必须包含以下具体结论：

1. **P0 Requirement Matrix**：逐项映射规范、测试、实现、状态。
2. **Baseline Delta**：
   - `DIModel` / `FrozenDIModel`: `ADAPTED`（只吸收冻结配置，拒绝未冻结额外 config）。
   - `ObjectId` / `LogicalId`: `ADAPTED`（保留 nominal RootModel，拒绝 baseline opaque regex）。
   - `SchemaVersion`: `ADAPTED`（保留 nominal type，拒绝 baseline `MAJOR.MINOR` regex，因高优先级规范未冻结 lexical format）。
   - `ObjectType`: `ADAPTED`（保留 nominal type，拒绝 baseline namespaced regex，因高优先级规范未冻结 lexical format）。
   - `CanonicalObjectClass`: `REUSED` semantics/wire values；Python 名称视为非冲突 implementation name。
3. **Implementation Drift**：candidate baseline 中的 `_OPAQUE_ID_RE`、`_SCHEMA_VERSION_RE`、`_OBJECT_TYPE_RE` 未迁入 production P0。
4. **Remaining SPEC_GAP**：
   - `P0-GAP-01`: opaque ID lexical wire constraints 未冻结；本阶段不加 regex。
   - `P0-GAP-02`: SchemaVersion lexical wire constraints 未冻结；本阶段不加 `MAJOR.MINOR` 限制。
   - `P0-GAP-03`: ObjectType lexical namespace grammar 未冻结；本阶段不加 regex。
   - `P0-GAP-04`: `object_class` Python nominal type name 未冻结；实现采用 `CanonicalObjectClass`，不创建 `ObjectClass` alias。
5. **Freeze Checkpoint**：

```text
P0: COMPLETE / AUTOMATED CHECKS PASS / AWAITING USER FREEZE REVIEW
P1: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

如果任一验证失败，则报告实际失败并保持：

```text
P0: IN PROGRESS / BLOCKED
P1: NOT AUTHORIZED
```

- [x] **Step 7: 更新 README 当前阶段**

README 只陈述实际验证后的状态，并链接 `P0_CORE_CONTRACT_AUDIT.md`；不得宣称 Exact V1 `FROZEN`。

---

## Plan self-review result

- Spec coverage: P0 实施顺序、Global Schema Policy、四个 nominal identity、七类 object class、P1 禁止项均有对应任务。
- Scope: 没有 B01/B02、ARSO、refs/hash/registry、Command/Event/Protocol 实现。
- Type consistency: 后续任务统一使用 `CanonicalObjectClass`；没有 `ObjectClass` alias。
- Placeholder scan: 无 `TBD`/`TODO`/“稍后实现”等占位步骤。
- Candidate-baseline discipline: 仅差异分析和 regression；未把 baseline regex 当规范权威。
