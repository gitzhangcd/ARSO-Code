# P1｜Exact References + Canonical Hash + Registry Design Specification

**日期：** 2026-09-03  
**状态：** `DESIGN REVIEW CANDIDATE`  
**阶段：** F6.1 Exact V1 Contract Implementation — P1  
**前置冻结：** P0 `FROZEN`  
**后续门禁：** P2 `NOT AUTHORIZED`  

## 1. 目标

P1 只冻结后续所有 canonical object 共同依赖的三类基础机制：

1. Exact / immutable reference data contracts；
2. RFC 8785 canonical JSON + SHA-256 content hash engine；
3. Object Registry 的 schema、reference-policy invariant 与 lookup/index behavior。

P1 **不得**提前冻结 B01–B08 的 exact object schema、object-specific canonical payload field set、完整 registry inventory、resolver/store/CAS 行为或 ARSO shadow types。

---

## 2. Normative Authority

实现必须遵循仓库既有权威顺序，优先读取：

1. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`

P1 设计遵循以下 frozen contract：

```text
CANONICAL_REVISION -> ExactObjectRef
IMMUTABLE_FACT     -> ObjectRef
IMMUTABLE_ROOT     -> ObjectRef
IMMUTABLE_GRAPH_NODE -> ObjectRef
SNAPSHOT           -> ObjectRef
OPERATIONAL_CONTROL_STATE -> no persistent ref
DERIVED_VIEW       -> no persistent ref unless materialized
```

Canonical hash normative target：

```text
content_hash = SHA256(RFC8785_CanonicalJSON(CanonicalPayload))
```

`CanonicalPayload` 必须排除：

```text
content_hash itself
transport-only metadata
mutable operational fields
```

对于 semantic revision，V1 默认排除：

```text
created_at
created_by
```

除非后续 owner-specific exact identity policy 明确另有规定。

---

## 3. 设计边界

### 3.1 P1 允许新增

```text
ExactObjectRef
ObjectRef
LogicalObjectRef
ContentHash
ReferenceKind
PrimitiveOwner
StateDomain
canonical_json_bytes(payload)
compute_content_hash(payload)
ObjectRegistryEntry
ObjectRegistryManifest
RegistryIndex
registry invariant validation
RFC 8785 cross-language fixtures
```

### 3.2 P1 明确禁止

```text
B01 exact models
B02 exact models
B03-B08 production model migration
ARSO canonical shadow types
object-specific CanonicalPayload extractor
complete Exact V1 registry inventory
ExactReferenceResolver implementation
CanonicalObjectStore implementation
CAS / BranchHead implementation
Command / Event / Protocol implementation
snapshot firewall implementation
```

`di_contracts_v1/` 继续作为只读 `FREEZE CANDIDATE` baseline，不是规范权威。

---

## 4. Reference Contracts

### 4.1 ExactObjectRef

```python
class ExactObjectRef(FrozenDIModel):
    object_type: ObjectType
    logical_id: LogicalId
    version_id: ObjectId
    content_hash: ContentHash
```

用途：`CANONICAL_REVISION` 的 persistent reference。

P1 只冻结结构、nominal typing、immutability 和 schema。目标解析后四项一致性属于 P13 semantic resolver：

```text
ref.object_type == target.object_type
ref.logical_id == target.logical_id
ref.version_id == target.id
ref.content_hash == target canonical hash
```

### 4.2 ObjectRef

```python
class ObjectRef(FrozenDIModel):
    object_type: ObjectType
    object_id: ObjectId
    content_hash: ContentHash
```

用途：非 versioned immutable historical objects。

### 4.3 LogicalObjectRef

```python
class LogicalObjectRef(FrozenDIModel):
    object_type: ObjectType
    logical_id: LogicalId
```

只允许 authoring workflow 使用。P1 提供 contract type；“进入 commit/compile/run/evaluate/snapshot 前必须 resolve exact”的运行时 enforcement 属于后续 resolver/runtime gate。

禁止任何 `latest/current/newest/most recent` implicit reference semantics。

---

## 5. ContentHash Normalization

高优先级规范冻结 SHA-256 算法，但未冻结字符串 wire encoding。P1 将该非冲突缺口正式 normalise 为：

```text
ContentHash := "sha256:" + 64 lowercase hexadecimal characters
```

Python contract：

```python
class ContentHash(RootModel[str]):
    # strict + frozen
    # exact lexical form: ^sha256:[0-9a-f]{64}$
```

理由：

- hash algorithm self-describing；
- 避免裸 64-hex 在未来多算法环境中失去语义；
- 与 candidate baseline 一致；
- 不改变规范已冻结的 SHA-256 算法。

P1 不借此冻结 `ObjectId`、`LogicalId`、`SchemaVersion` 或 `ObjectType` 的 lexical grammar；P0-GAP-01..03 继续保留。

---

## 6. Canonical JSON / Hash Architecture

### 6.1 核心分离原则

P1 必须把：

```text
owner-specific payload selection
```

和：

```text
canonicalization + hashing
```

完全分离。

禁止提供类似：

```python
semantic_payload(model)
```

并通过通用字段黑名单自动决定 canonical identity。

正确数据流：

```text
Owner exact contract (P2+)
        |
        v
CanonicalPayload (JSON-native value)
        |
        v
canonical_json_bytes(payload)
        |
        v
RFC 8785 canonical UTF-8 bytes
        |
        v
SHA-256
        |
        v
ContentHash("sha256:...")
```

因此 P1 冻结的是 canonicalization engine，而不是下游 object 的 payload composition policy。

### 6.2 API

```python
JsonScalar = None | bool | int | float | str
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


def canonical_json_bytes(payload: JsonValue) -> bytes:
    ...


def compute_content_hash(payload: JsonValue) -> ContentHash:
    ...
```

输入必须已是 JSON-native / I-JSON-compatible payload；Pydantic model 到 payload 的转换不由此 API 猜测。

### 6.3 RFC 8785 implementation

P1 使用 `rfc8785==0.1.4` 作为 Python canonicalizer。2026-09-03 核验的 PyPI 最新 release 为 0.1.4；该实现为 pure Python、无运行时依赖，并直接输出 UTF-8 `bytes`。

依赖必须 exact-pin：

```text
rfc8785==0.1.4
```

不得使用 `json.dumps(sort_keys=True)` 替代 JCS，因为 RFC 8785 还冻结 ECMAScript primitive serialization、I-JSON constraints 和 deterministic property sorting。

### 6.4 Error contract

P1 不引入新的跨阶段错误 taxonomy。`canonical_json_bytes` 对非 JCS/I-JSON-compatible payload 保留底层 canonicalization exception 的 cause，并在 P1 module 内统一转译为一个 P1-local exception：

```python
class CanonicalizationError(ValueError):
    pass
```

该错误不是 ARSO canonical primitive，也不进入 registry。

---

## 7. Cross-Language Canonicalization Gate

P1 Freeze 必须证明 Python 与独立 ECMAScript oracle 对同一 fixture 产生 byte-identical canonical JSON。

测试源分为两类：

1. RFC 8785 / reference repository 的 canonicalization vectors；
2. 本仓库固定 cross-language fixture，覆盖：
   - property ordering；
   - Unicode preservation；
   - escape behavior；
   - booleans / null；
   - arrays / nested objects；
   - representative IEEE-754-safe numeric cases。

Node fixture 只用于测试 oracle，不进入 production runtime dependency。

P1 Freeze 条件：

```text
Python canonical bytes == Node/reference canonical bytes
```

若 cross-language fixture 未通过：

```text
P1 = BLOCKED
Hash Implementation = FREEZE CANDIDATE
```

不得以“Python deterministic”代替 cross-language proof。

---

## 8. Registry Architecture

### 8.1 ReferenceKind

P1 可安全冻结 closed enum：

```python
class ReferenceKind(StrEnum):
    EXACT_OBJECT_REF = "EXACT_OBJECT_REF"
    OBJECT_REF = "OBJECT_REF"
    NONE = "NONE"
```

因为三类值已经被 Persistence / Reference Matrix 完整覆盖。

### 8.2 PrimitiveOwner / StateDomain

P1 不把 candidate baseline 的 owner/domain 列表自动升格为 closed enum。

定义 nominal string shells：

```python
class PrimitiveOwner(RootModel[str]): ...
class StateDomain(RootModel[str]): ...
```

它们必须 strict + frozen，但 P1 不冻结 lexical pattern 或 closed value inventory。

完整 owner/domain inventory 随 B01/B02/ARSO exact owner contracts 冻结。

### 8.3 ObjectRegistryEntry

```python
class ObjectRegistryEntry(FrozenDIModel):
    object_type: ObjectType
    object_class: CanonicalObjectClass
    primitive_owner: PrimitiveOwner
    state_domain: StateDomain | None
    historical_ssot: bool
    versioned: bool
    persistent_ref_kind: ReferenceKind
```

P1 不加入 object-specific字段，例如 schema class pointer、artifact eligibility、snapshot-specific flags 或 domain lifecycle metadata；这些必须由后续 owner contracts 提供明确依据后再扩展。

### 8.4 ObjectRegistryManifest

```python
class ObjectRegistryManifest(FrozenDIModel):
    entries: tuple[ObjectRegistryEntry, ...]
```

Manifest 必须拒绝重复 `object_type`。

P1 不提供“完整 Exact V1 manifest”；测试使用最小 synthetic entries 验证 invariant engine。

### 8.5 RegistryIndex

```python
class RegistryIndex:
    def __init__(self, manifest: ObjectRegistryManifest) -> None: ...
    def get(self, object_type: ObjectType) -> ObjectRegistryEntry: ...
    def contains(self, object_type: ObjectType) -> bool: ...
```

Index 是 derived runtime view，不是 canonical object，不进入 registry 自身。

未知 `object_type` 必须显式失败，不允许 fallback、namespace guessing 或 fuzzy matching。

---

## 9. Registry Invariants

P1 必须自动验证：

### 9.1 CANONICAL_REVISION

```text
historical_ssot = true
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
```

### 9.2 IMMUTABLE_FACT / IMMUTABLE_ROOT / IMMUTABLE_GRAPH_NODE / SNAPSHOT

```text
historical_ssot = true
versioned = false
persistent_ref_kind = OBJECT_REF
```

### 9.3 OPERATIONAL_CONTROL_STATE

```text
historical_ssot = false
versioned = false
persistent_ref_kind = NONE
```

### 9.4 DERIVED_VIEW

P1 默认冻结：

```text
historical_ssot = false
versioned = false
persistent_ref_kind = NONE
```

若未来存在 materialized derived view，需要由 owner-specific contract 显式定义新 policy；P1 不从“unless materialized”猜测 materialization schema。

### 9.5 OneCanonicalObject => OnePrimitiveOwner

每个 `object_type` 在一个 manifest 内只能出现一次，因此不能同时拥有多个 `primitive_owner`。

---

## 10. Public API Boundary

P1 完成后的 public surface 仅增加：

```text
ContentHash
ExactObjectRef
ObjectRef
LogicalObjectRef
canonical_json_bytes
compute_content_hash
CanonicalizationError
ReferenceKind
PrimitiveOwner
StateDomain
ObjectRegistryEntry
ObjectRegistryManifest
RegistryIndex
```

P0 public types 保持兼容，不重命名、不改变 wire behavior。

---

## 11. Planned File Boundaries

```text
src/design_intelligence/contracts/core/
  refs.py        # reference + ContentHash contracts
  hashing.py     # RFC8785 canonicalization and SHA-256 only
  types.py       # P0 types + P1 nominal registry types if appropriate

src/design_intelligence/registry/
  models.py      # ReferenceKind, registry entry/manifest
  validation.py  # object-class/reference invariants
  index.py       # RegistryIndex derived lookup
  __init__.py

tests/unit/
tests/schemas/
tests/hashing/
tests/registry/
tests/cross_language/
tests/repository/
```

Implementation plan 可以在不改变这些责任边界的前提下微调具体类型所在文件，但不得合并 payload selection 与 hashing responsibility。

---

## 12. TDD / Freeze Acceptance

P1 必须逐项 RED -> GREEN，并至少满足：

```text
ExactObjectRef exact schema             PASS
ObjectRef exact schema                  PASS
LogicalObjectRef exact schema           PASS
ContentHash exact wire validation       PASS
Refs immutable / extra forbidden        PASS
RFC 8785 official/reference vectors     PASS
Python <-> Node/reference byte equality PASS
SHA-256 deterministic fixture           PASS
Registry entry schema                   PASS
Registry duplicate object_type reject   PASS
Registry class/ref invariants           PASS
Registry unknown lookup explicit fail   PASS
No B01-B08 early implementation         PASS
No ARSO shadow type                     PASS
Root repository regression              PASS
di_contracts_v1 46-test regression      PASS
7/7 authoritative spec checksum         PASS
git diff --check                        CLEAN
```

GitHub CI 若仍未配置，必须标记 `NOT CONFIGURED`，不得写成 PASS。

---

## 13. Explicitly Deferred Gates

以下不属于 P1 完成声明：

```text
object-specific CanonicalPayload field selection
complete Exact V1 registry inventory
semantic target resolution / four-field closure
store persistence
CAS behavior
snapshot negative firewall
B01/B02 exact schemas
ARSO exact primitive integration
complete Command/Event/Protocol surface
```

对应后续门禁：

```text
CanonicalPayload owner policy -> P2+
Complete registry inventory    -> downstream + AC-14 / P14
Semantic resolver closure      -> P13
Cross-stage conformance        -> P14
```

---

## 14. Remaining Known Gaps After P1 Design

```text
P0-GAP-01 ObjectId / LogicalId lexical grammar
P0-GAP-02 SchemaVersion lexical grammar
P0-GAP-03 ObjectType lexical grammar
P0-GAP-04 object_class Python naming
B01 exact field-level owner contract
B02 exact field-level owner contract
ARSO authoritative exact imports
complete registry inventory
```

这些 gap 不得通过 P1 implementation convenience 隐式解决。

---

## 15. P1 State Machine

书面设计批准后：

```text
P1 DESIGN APPROVED
      -> implementation plan
      -> TDD implementation
      -> automated verification
      -> independent Freeze Review
      -> user Freeze approval
      -> merge
      -> P1 FROZEN
      -> P2 AUTHORIZED
```

在用户批准 P1 Freeze 之前：

```text
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

## 16. External Technical Reference Check

2026-09-03 设计核验：

- RFC 8785 官方文本定义 JCS：ECMAScript primitive serialization + I-JSON constraints + deterministic property sorting。
- PyPI `rfc8785` 最新 release 为 `0.1.4`（2024-09-27），pure Python、Python >=3.8、无 runtime dependency，并返回 UTF-8 `bytes`。

这些外部事实仅用于选择实现库和验证测试；仓库内 frozen DI/ARSO specs 仍然拥有 contract authority。