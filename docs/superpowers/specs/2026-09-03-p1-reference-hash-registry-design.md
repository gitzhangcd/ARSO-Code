# P1｜Exact References + Canonical Hash + Registry Design Specification

**日期：** 2026-09-03  
**状态：** `DESIGN REVIEW CANDIDATE`  
**阶段：** F6.1 Exact V1 Contract Implementation — P1  
**前置冻结：** P0 `FROZEN`  
**后续门禁：** P2 `NOT AUTHORIZED`  

## 1. 目标

P1 只冻结后续 canonical object 共同依赖的三类基础机制：

1. Exact / immutable reference data contracts；
2. RFC 8785 canonical JSON + SHA-256 content hash engine；
3. Object Registry 的 entry schema、generic invariant engine 与 lookup/index behavior。

P1 **不得**提前冻结：

```text
B01-B08 exact object schema
object-specific CanonicalPayload field set
complete Exact V1 registry inventory
semantic resolver/store/CAS behavior
ARSO shadow types
```

---

## 2. Normative Authority

实现必须遵循仓库既有权威顺序，优先读取：

1. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`

P1 直接实现以下 frozen reference matrix：

```text
CANONICAL_REVISION      -> ExactObjectRef
IMMUTABLE_FACT          -> ObjectRef
IMMUTABLE_ROOT          -> ObjectRef
IMMUTABLE_GRAPH_NODE    -> ObjectRef
SNAPSHOT                -> ObjectRef
OPERATIONAL_CONTROL_STATE -> none
DERIVED_VIEW            -> none unless materialized
```

Canonical hash normative target：

```text
content_hash = SHA256(RFC8785_CanonicalJSON(CanonicalPayload))
```

`CanonicalPayload` 排除：

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
generic registry invariant validation
RFC 8785 official/reference fixtures
Python <-> Node cross-language fixtures
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

P1 只冻结结构、nominal typing、immutability 和 JSON Schema。目标解析后的四项一致性属于 P13 semantic resolver：

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

## 5. P1-N01｜ContentHash Wire Normalization

高优先级规范冻结 SHA-256 算法，但未冻结字符串 wire encoding。经 P1 设计决策，将该非冲突缺口 normalise 为：

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

P1 冻结 canonicalization engine，不冻结下游 object 的 payload composition policy。

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

P1 测试必须覆盖并拒绝至少：

```text
non-string object keys
NaN
+Infinity
-Infinity
其他 RFC8785 implementation 明确拒绝的非 canonicalizable input
```

P1 不冻结新的公共 error taxonomy；调用失败必须显式抛错并保留 cause，但不把第三方 exception class 或新自定义 exception 升格为 public Exact V1 contract。

### 6.3 Python RFC 8785 implementation

P1 使用：

```text
rfc8785==0.1.4
```

2026-09-03 核验：PyPI 最新 release 为 0.1.4；pure Python、Python >=3.8、无 runtime dependency，并直接输出 UTF-8 `bytes`。

不得使用 `json.dumps(sort_keys=True)` 替代 JCS，因为 RFC 8785 还要求 ECMAScript primitive serialization、I-JSON constraints 和 deterministic property sorting。

---

## 7. Cross-Language Canonicalization Gate

P1 Freeze 必须证明 Python 与独立 ECMAScript implementation 对同一 fixture 产生 byte-identical canonical JSON。

### 7.1 Test oracle

Python production side：

```text
rfc8785==0.1.4
```

Node test oracle：

```text
canonicalize@4.0.0
```

2026-09-03 核验：npm `canonicalize` 4.0.0 明确声明 RFC 8785 compatibility、0 runtime dependencies。它只作为 dev/test oracle，不进入 Python production dependency。

测试目录维护独立 Node dev fixture：

```text
tests/cross_language/node/package.json
tests/cross_language/node/package-lock.json
tests/cross_language/node/canonicalize.mjs
```

依赖必须锁定，测试准备使用 `npm ci`，不得依赖未锁版本的 `npx latest`。

### 7.2 Fixtures

测试源：

1. RFC 8785 / reference repository canonicalization vectors；
2. 本仓库固定 fixture，覆盖：
   - property ordering；
   - Unicode preservation；
   - escape behavior；
   - booleans / null；
   - arrays / nested objects；
   - representative IEEE-754-compatible numeric cases。

P1 Freeze 条件：

```text
Python canonical bytes == Node canonical bytes
```

若 cross-language fixture 未通过：

```text
P1 = BLOCKED
Hash Implementation = FREEZE CANDIDATE
```

不得以“Python deterministic”代替 cross-language proof。

---

## 8. Registry Contract

### 8.1 Exact Contract §20 correction

最高优先级 Exact Contract 明确要求每个 registry entry **至少**声明：

```text
object_type
python_type
schema_version
canonical
primitive_owner
capability_owners
object_class
state_domain
versioned
persistent_ref_kind
historical_ssot
logical_authoring_ref_allowed
system_snapshot_eligible
knowledge_snapshot_eligible
review_snapshot_eligible
system_intervention_target_eligible
artifact_eligible
```

因此 P1 不得采用只含 owner/class/ref 的缩减 registry entry。

### 8.2 ReferenceKind

P1 冻结 closed enum：

```python
class ReferenceKind(StrEnum):
    EXACT_OBJECT_REF = "EXACT_OBJECT_REF"
    OBJECT_REF = "OBJECT_REF"
    NONE = "NONE"
```

因为三类值已经被 Persistence / Reference Matrix 完整覆盖。

### 8.3 PrimitiveOwner / StateDomain

P1 不把 candidate baseline 的 owner/domain 列表自动升格为 closed enum。

定义 strict + frozen nominal string shells：

```python
class PrimitiveOwner(RootModel[str]): ...
class StateDomain(RootModel[str]): ...
```

P1 不冻结 lexical pattern 或 closed value inventory。

`state_domain` 在 registry entry 中必须是**必填**，不得为 `None`，因为 Exact Contract §8 明确规定：

```text
A registry entry MUST declare state_domain.
```

完整 owner/domain inventory 随 B01/B02/ARSO exact owner contracts 冻结。

### 8.4 ObjectRegistryEntry

P1 采用以下 exact field surface；所有字段均要求调用方显式声明，不通过默认值隐式补齐“必须声明”的治理属性：

```python
class ObjectRegistryEntry(FrozenDIModel):
    object_type: ObjectType
    python_type: str
    schema_version: SchemaVersion
    canonical: bool
    primitive_owner: PrimitiveOwner
    capability_owners: tuple[PrimitiveOwner, ...]
    object_class: CanonicalObjectClass
    state_domain: StateDomain
    versioned: bool
    persistent_ref_kind: ReferenceKind
    historical_ssot: bool
    logical_authoring_ref_allowed: bool
    system_snapshot_eligible: bool
    knowledge_snapshot_eligible: bool
    review_snapshot_eligible: bool
    system_intervention_target_eligible: bool
    artifact_eligible: bool
```

字段类型依据：

- high-priority Exact Contract 冻结字段名与语义；
- candidate baseline 仅作为不冲突的可执行类型映射证据；
- P1 不迁移 candidate 的完整 object inventory 或旧 eligibility 值。

特别注意 N08 normalization：candidate baseline 中部分 Knowledge object 的 `artifact_eligible=True` 已被高优先级规范修正，不能作为正式 inventory 真值。

### 8.5 ObjectRegistryManifest

Exact Contract §20 没有冻结 candidate manifest 的：

```text
manifest_id
generated_at
manifest content_hash
```

因此 P1 **不迁移这些 candidate-only metadata**。

P1 manifest 仅作为 immutable registry entry container：

```python
class ObjectRegistryManifest(FrozenDIModel):
    entries: tuple[ObjectRegistryEntry, ...]
```

Manifest 必须拒绝重复 `object_type`。

P1 不提供“完整 Exact V1 manifest”；测试使用 synthetic entries 验证 schema 与 generic invariant engine。

### 8.6 RegistryIndex

```python
class RegistryIndex:
    def __init__(self, manifest: ObjectRegistryManifest) -> None: ...
    def require(self, object_type: ObjectType) -> ObjectRegistryEntry: ...
    def contains(self, object_type: ObjectType) -> bool: ...
    def validate_reference_kind(self, ref: ExactObjectRef | ObjectRef) -> None: ...
    def require_system_snapshot_eligible(self, ref: ExactObjectRef | ObjectRef) -> None: ...
    def require_knowledge_snapshot_eligible(self, ref: ExactObjectRef | ObjectRef) -> None: ...
    def require_review_snapshot_eligible(self, ref: ExactObjectRef | ObjectRef) -> None: ...
    def require_system_intervention_target_eligible(self, ref: ExactObjectRef | ObjectRef) -> None: ...
```

Index 是 derived runtime view，不是 canonical object，不进入 registry 自身。

未知 `object_type` 必须显式失败，不允许 fallback、namespace guessing 或 fuzzy matching。

---

## 9. Registry Generic Invariants

P1 必须自动验证：

### 9.1 object_type unique / one primitive owner

`ObjectRegistryManifest` 中 `object_type` 唯一。单值 `primitive_owner` 字段保证每个 entry 只能声明一个 primitive owner。

### 9.2 CANONICAL_REVISION

```text
historical_ssot = true
versioned = true
persistent_ref_kind = EXACT_OBJECT_REF
```

### 9.3 IMMUTABLE_FACT / IMMUTABLE_ROOT / IMMUTABLE_GRAPH_NODE / SNAPSHOT

```text
historical_ssot = true
versioned = false
persistent_ref_kind = OBJECT_REF
```

### 9.4 OPERATIONAL_CONTROL_STATE

```text
historical_ssot = false
versioned = false
persistent_ref_kind = NONE
```

### 9.5 DERIVED_VIEW

当前没有 materialized derived-view exact schema。P1 对可执行 registry entry 只接受：

```text
historical_ssot = false
versioned = false
persistent_ref_kind = NONE
```

这不是取消规范中的 `unless materialized`；而是明确：materialized view 在 owner-specific materialization contract 冻结前**不可进入 P1 executable registry**。P1 不猜测 materialization identity/reference policy。

---

## 10. Frozen Object-Specific Registry Policies：记录但不伪造 inventory

Exact Contract §20 还冻结：

```text
DesignSpec.system_intervention_target_eligible = false
DesignSpec.artifact_eligible = false
GenerationCompiler.artifact_eligible = true
GenerationCompiler.system_intervention_target_eligible = true
BranchHeadPointer.historical_ssot = false
InterventionTransaction.historical_ssot = false
```

其中当前高优先级规范没有为所有这些对象冻结可执行 `object_type` wire identifier；B01/B02 owner exact contract 也仍缺失。

因此 P1：

1. 在 design/audit 中保留这些 frozen policy；
2. registry model 必须具备承载这些字段的能力；
3. **不根据 candidate baseline 猜 object_type mapping 来硬编码 object-specific validator**；
4. 等完整 registry inventory / owner exact object_type mapping 冻结后，在 downstream registry gate / AC-14 对这些 policy 做 executable enforcement。

唯一已经在最高优先级规范显式出现的 `di.b06.intervention_transaction` 也不单独提前特殊化，以避免形成部分 hard-code、部分 deferred 的不一致 registry policy。

P1 Freeze 不得宣称“§20 所有 object-specific registry policy 已 executable-complete”。

---

## 11. Public API Boundary

P1 完成后的 public surface 仅增加：

```text
ContentHash
ExactObjectRef
ObjectRef
LogicalObjectRef
canonical_json_bytes
compute_content_hash
ReferenceKind
PrimitiveOwner
StateDomain
ObjectRegistryEntry
ObjectRegistryManifest
RegistryIndex
```

不新增公共 canonicalization exception type。

P0 public types 保持兼容，不重命名、不改变 wire behavior。

---

## 12. Planned File Boundaries

```text
src/design_intelligence/contracts/core/
  refs.py        # reference + ContentHash contracts
  hashing.py     # RFC8785 canonicalization and SHA-256 only
  types.py       # P0 types + P1 nominal registry types as planned

src/design_intelligence/registry/
  models.py      # ReferenceKind + full §20 registry entry surface + manifest
  validation.py  # generic class/ref/history invariants
  index.py       # RegistryIndex derived lookup/eligibility checks
  __init__.py

tests/unit/
tests/schemas/
tests/hashing/
tests/registry/
tests/cross_language/
  node/
tests/repository/
```

Implementation plan 可以在不改变责任边界的前提下微调具体 nominal type 所在文件，但不得合并 payload selection 与 hashing responsibility。

---

## 13. TDD / P1 Freeze Acceptance

P1 必须逐项 RED -> GREEN，并至少满足：

```text
ExactObjectRef exact schema                 PASS
ObjectRef exact schema                      PASS
LogicalObjectRef exact schema               PASS
ContentHash exact wire validation           PASS
Refs immutable / extra forbidden            PASS
RFC 8785 official/reference vectors         PASS
Python <-> Node byte equality               PASS
SHA-256 deterministic fixture               PASS
Invalid JCS/I-JSON inputs rejected           PASS
Registry entry complete §20 field surface   PASS
Registry state_domain required              PASS
Registry duplicate object_type rejected     PASS
Registry generic class/ref invariants        PASS
Registry reference-kind lookup validation   PASS
Registry eligibility lookup behavior        PASS
Registry unknown lookup explicit failure    PASS
No complete B01-B08 inventory migration     PASS
No B01-B08 production schema implementation PASS
No ARSO shadow type                         PASS
Root repository regression                  PASS
di_contracts_v1 46-test regression          PASS
7/7 authoritative spec checksum             PASS
git diff --check                            CLEAN
```

GitHub CI 若仍未配置，必须标记：

```text
NOT CONFIGURED
```

不得写成 PASS。

P1 Freeze report 必须明确以下仍未完成：

```text
§20 object-specific policy executable binding
complete Exact V1 registry inventory
```

---

## 14. Explicitly Deferred Gates

以下不属于 P1 完成声明：

```text
object-specific CanonicalPayload field selection
complete Exact V1 registry inventory
§20 object-specific policy -> exact object_type executable binding
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
CanonicalPayload owner policy      -> P2+
Complete registry inventory        -> downstream + AC-14 / P14
Object-specific registry policy    -> inventory/AC-14
Semantic resolver closure          -> P13
Cross-stage conformance            -> P14
```

---

## 15. Remaining Known Gaps After P1 Design

```text
P0-GAP-01 ObjectId / LogicalId lexical grammar
P0-GAP-02 SchemaVersion lexical grammar
P0-GAP-03 ObjectType lexical grammar
P0-GAP-04 object_class Python naming
B01 exact field-level owner contract
B02 exact field-level owner contract
ARSO authoritative exact imports
complete registry inventory
object-specific registry object_type binding
```

这些 gap 不得通过 P1 implementation convenience 隐式解决。

---

## 16. P1 State Machine

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

---

## 17. External Technical Reference Check

2026-09-03 设计核验：

- RFC 8785 官方文本定义 JCS：ECMAScript primitive serialization + I-JSON constraints + deterministic property sorting。
- PyPI `rfc8785` 最新 release 为 `0.1.4`（2024-09-27），pure Python、Python >=3.8、无 runtime dependency，并返回 UTF-8 `bytes`。
- npm `canonicalize` 当前 latest 为 `4.0.0`，声明 RFC 8785 compatibility、0 dependencies；仅用于 cross-language test oracle。

这些外部事实只用于实现库和 conformance tooling 选择；仓库内 frozen DI/ARSO specs 仍拥有 contract authority。