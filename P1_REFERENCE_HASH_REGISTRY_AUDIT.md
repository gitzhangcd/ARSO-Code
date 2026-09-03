# P1｜Exact References + Canonical Hash + Registry 实现审计

审计日期：2026-09-03
阶段：F6.1 Exact V1 Contract Implementation — P1
结论：`COMPLETE / AUTOMATED CHECKS PASS / AWAITING USER FREEZE REVIEW`
后续门禁：P2 `NOT AUTHORIZED`
Exact V1：`FREEZE CANDIDATE`

## 1. 审计范围

P1 仅实现后续 canonical object 共同依赖的三类基础机制：

1. exact / immutable reference data contracts；
2. RFC 8785 canonical JSON + SHA-256 content hash engine；
3. Object Registry 的 minimum entry schema、generic invariant validation 与 derived lookup/index behavior。

明确未进入：B01–B08 production schemas、ARSO canonical shadow/import layer、resolver/store/CAS、Command/Event/Protocol、完整 registry inventory、owner-specific CanonicalPayload composition。

## 2. 规范权威

本轮重新以以下顺序核验：

1. `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`
2. `specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt`
3. `specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt`
4. `specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt`

P1 书面设计规范：

`docs/superpowers/specs/2026-09-03-p1-reference-hash-registry-design.md`

Implementation Plan：

`docs/superpowers/plans/2026-09-03-p1-reference-hash-registry-implementation.md`

## 3. 实现结果

### 3.1 Reference contracts

已实现并导出：

- `ContentHash`
- `ExactObjectRef`
- `ObjectRef`
- `LogicalObjectRef`
- `CanonicalRef`

Exact field surface：

```text
ExactObjectRef:
  object_type
  logical_id
  version_id
  content_hash

ObjectRef:
  object_type
  object_id
  content_hash

LogicalObjectRef:
  object_type
  logical_id
```

所有 reference model 继承 frozen/extra-forbid contract policy；cross-nominal identity misuse 有回归测试。

### 3.2 P1-N01｜ContentHash normalization

P1 经已批准书面 Spec 将规范未冻结的 hash wire encoding 正常化为：

```text
^sha256:[0-9a-f]{64}$
```

该 normalization 不改变上游已冻结的 SHA-256 algorithm contract，也不扩展到 `ObjectId`、`LogicalId`、`SchemaVersion`、`ObjectType` lexical grammar。

### 3.3 RFC 8785 canonical hash engine

production dependency：

```text
rfc8785==0.1.4
```

实现 API：

```text
canonical_json_bytes(payload)
compute_content_hash(payload)
```

数据流严格保持：

```text
owner-specific CanonicalPayload selection [DEFERRED]
-> JSON-native payload
-> RFC 8785 canonical UTF-8 bytes
-> SHA-256
-> ContentHash
```

P1 没有实现 generic model-to-payload blacklist extractor。

测试覆盖 property ordering、Unicode、nested JSON、RFC 8785 official vector、NaN/Infinity rejection、non-string object-key rejection。

### 3.4 Cross-language conformance

独立 Node oracle：

```text
canonicalize@4.0.0
```

并提交锁定的 `package-lock.json`。

Python `rfc8785` 与 Node `canonicalize` 对 repository fixtures 做 byte-identical comparison；该 gate 已在最终 GitHub Actions 中通过。

### 3.5 Object Registry minimum contract

`ObjectRegistryEntry` 已覆盖 Exact Contract §20 的完整最低字段面：

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

所有字段均为 required；没有通过 default 隐式填充必须显式声明的治理属性。

P1 同时实现：

- `PrimitiveOwner` strict nominal string shell；
- `StateDomain` strict nominal string shell；
- closed `ReferenceKind = EXACT_OBJECT_REF | OBJECT_REF | NONE`；
- immutable `ObjectRegistryManifest`；
- duplicate `object_type` rejection。

完整 owner/domain inventory 未被提前冻结。

### 3.6 Generic persistence/reference invariants

已编码并测试：

```text
CANONICAL_REVISION
  historical_ssot=true
  versioned=true
  persistent_ref_kind=EXACT_OBJECT_REF

IMMUTABLE_FACT / IMMUTABLE_ROOT / IMMUTABLE_GRAPH_NODE / SNAPSHOT
  historical_ssot=true
  versioned=false
  persistent_ref_kind=OBJECT_REF

OPERATIONAL_CONTROL_STATE
  historical_ssot=false
  versioned=false
  persistent_ref_kind=NONE

DERIVED_VIEW [P1 executable/unmaterialized]
  historical_ssot=false
  versioned=false
  persistent_ref_kind=NONE
```

materialized derived-view identity/reference policy仍由后续 owner-specific contract 冻结，P1 未猜测。

### 3.7 RegistryIndex

已实现 derived runtime index：

- exact `ObjectType` lookup；
- unknown object type 显式失败；
- persistent reference kind compatibility；
- system snapshot eligibility；
- knowledge snapshot eligibility；
- review snapshot eligibility；
- system intervention target eligibility。

P1 index 不 resolve target，不验证 target `content_hash`，也不承担 P13 semantic closure。

## 4. TDD 证据

P1 production behavior 按 RED → GREEN 推进。

代表性 RED 证据：

- refs/ContentHash 初始测试因 production symbols 不存在而失败；
- registry invariant 新增后 9 个 case 因错误组合未被拒绝而失败；
- RegistryIndex 新增前 8 个 behavior tests 仅因 `RegistryIndex` 不存在而失败；
- cross-language gate 在 `package-lock.json` 尚未正式进入仓库前保持 RED。

对应 production implementation 均在 RED 后加入并重新验证 GREEN。

## 5. 最终 Verification Evidence

验证对象：PR #3 head `c3fa772edc46adf7a373d36aa123ec9394d61051`
GitHub Actions run：`33745660896`
Job：`100617411480`
结论：`SUCCESS`

最终 gate：

| Gate | 结果 |
|---|---|
| P1 targeted tests | `49 PASS` |
| Full root repository tests | `76 PASS` |
| Candidate baseline regression | `46 PASS` |
| Specification SHA-256 manifest | `7 / 7 OK` |
| `compileall src/design_intelligence` | `PASS` |
| Non-Markdown patch whitespace | `PASS` |
| Markdown trailing-whitespace policy | `PASS` |
| Authoritative `specs/` drift | `PASS / NO CHANGES` |
| `di_contracts_v1/` baseline drift | `PASS / NO CHANGES` |

## 6. Baseline Delta

`di_contracts_v1/` 继续是只读 `FREEZE CANDIDATE` evidence，不是规范权威。

正式 P1 没有 bulk-copy baseline；关键差异包括：

- 使用已批准的 P1-N01 hash wire normalization；
- 补上真实 RFC 8785 cross-language proof；
- Registry entry 采用 Exact Contract §20 完整最低字段面；
- 不迁移 candidate-only manifest metadata；
- 不迁移完整 candidate registry inventory；
- 不把 candidate owner/domain value list 升格为 closed enum；
- 不把 candidate object-specific eligibility 值视为正式 owner truth。

最终 baseline 自身 46 tests 保持全绿，目录无改动。

## 7. Deferred / Non-P1 Gaps

以下项目仍为后续阶段责任，不构成 P1 blocker：

- B01/B02 exact field-level owner schemas；
- authoritative ARSO primitive imports/adaptation；
- complete Exact V1 registry inventory；
- owner-specific CanonicalPayload composition；
- exact target resolution / semantic closure；
- revision-parent validation；
- CAS / BranchHead fixtures；
- snapshot firewalls；
- complete Command/Event inventory；
- Protocol signatures/static conformance；
- CS-01–CS-32 + AC-01–AC-18 full release surface。

因此 `Exact V1` 仍只能保持 `FREEZE CANDIDATE`。

## 8. 非阻断维护项

GitHub Actions 当前输出 `actions/checkout@v4` 与 `actions/setup-python@v5` 的 Node 20 deprecation warning；平台在本次 run 中强制使用 Node 24，所有 gate 均成功。

分类：`MINOR / NON-BLOCKING`。

该项属于 CI maintenance，不改变 P1 schema/API contract，不作为 P1 Freeze blocker。

## 9. 审计结论

未发现 P1 范围内未解决的 `SPEC_CONFLICT`。

未发现需要通过猜测补齐的 P1 `SPEC_GAP`。

未发现 P2 capability leakage。

最终状态：

```text
P0: FROZEN
P1: COMPLETE / AUTOMATED CHECKS PASS / AWAITING USER FREEZE REVIEW
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

本审计不自行把 P1 标记为 `FROZEN`。P1 是否进入 Frozen Checkpoint 仍需用户明确批准。
