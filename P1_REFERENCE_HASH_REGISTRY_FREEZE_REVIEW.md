# P1｜Exact References + Canonical Hash + Registry 独立 Freeze Review

Review 日期：2026-09-03
Review 模式：实现完成后的独立二次规范审查
Review 对象：PR #3 `p1-refs-hash-registry`
基线：`main@dbb3b2a8d5c5a19426169b25d31c79f2d2bf09cc`
审查起始 head：`c3fa772edc46adf7a373d36aa123ec9394d61051`
结论：`PASS / READY FOR USER FREEZE REVIEW`

> 本文件是与 implementation execution 分离的第二遍 criteria-based review。它不替代用户 Freeze Checkpoint，也不把 P1 自动升级为 `FROZEN`。

## 1. Review 方法

重新从最高优先级规范出发，不以 candidate baseline 或实现过程中的既有假设作为权威：

1. 重新读取 `DI-V5-EXACT-CONTRACT` 中 canonical hash、reference matrix、Exact/Object/Logical ref、Registry §20 与 release blockers；
2. 对照已批准 P1 Design Specification；
3. 检查 PR #3 changed-file inventory；
4. 逐项复核 production code：refs、hashing、registry models、generic validation、RegistryIndex、public exports；
5. 复核 tests 和 P1 scope guard；
6. 复核最终 CI 与 authoritative-source drift gate；
7. 单独检查是否有 P2 leakage、owner-specific policy over-freeze、baseline promotion 或规范漂移。

## 2. 规范符合性矩阵

| Review 项 | 规范要求 | PR #3 结果 | 结论 |
|---|---|---|---|
| ExactObjectRef | `object_type + logical_id + version_id + content_hash` | exact field surface | PASS |
| ObjectRef | `object_type + object_id + content_hash` | exact field surface | PASS |
| LogicalObjectRef | authoring-only结构，不引入 latest semantics | exact structure，无 implicit latest | PASS |
| ContentHash | SHA-256；wire form由批准的 P1-N01 normalise | `sha256:` + 64 lowercase hex | PASS |
| Canonicalization | RFC 8785，不得用普通 sorted JSON 替代 | `rfc8785==0.1.4` | PASS |
| Cross-language release condition | canonical bytes 必须跨语言一致 | Python vs Node locked oracle | PASS |
| Payload ownership | P1 不得猜 owner-specific CanonicalPayload | hashing 仅接受 prepared JSON-native value | PASS |
| Registry §20 | 最低治理字段全部显式声明 | 17 个 required fields 全覆盖 | PASS |
| Registry primitive owner | exactly one primitive owner | single `primitive_owner` field | PASS |
| Registry object_type | unique | manifest duplicate rejection | PASS |
| Persistence matrix | object class 与 history/version/ref kind 一致 | generic validator | PASS |
| Registry lookup | exact object_type，unknown 显式失败 | RegistryIndex exact lookup | PASS |
| Eligibility guards | registry flag 驱动 | 4 类 guard | PASS |
| Full inventory | P1 不得伪造 | 未实现 | PASS |
| Resolver/content-target proof | 属 P13 | 未提前实现 | PASS |
| ARSO primitives | 禁止 DI shadow | 无新增 ARSO shadow class | PASS |
| B01/B02 | exact owner contract 未授权进入 P1 | 无 production models | PASS |
| Candidate baseline | evidence only / read-only | 无目录修改 | PASS |
| Authoritative specs | 不得修改 | 无目录修改，7/7 checksum OK | PASS |

## 3. Production Code Review

### 3.1 `refs.py`

- `ContentHash` frozen + strict lexical pattern；
- three reference types inherit frozen/extra-forbid base policy；
- `CanonicalRef` 仅包含 persistent exact ref categories，不把 `LogicalObjectRef` 当作 canonical runtime ref。

未发现 blocker。

### 3.2 `hashing.py`

- production API 极小；
- SHA-256 直接作用于 RFC 8785 canonical bytes；
- 没有 Pydantic model introspection；
- 没有 blacklist-based generic payload selection；
- rejection 保留第三方 canonicalization error semantics，没有新增未经规范冻结的 public error taxonomy。

未发现 blocker。

### 3.3 `registry/models.py` + `validation.py`

- §20 最低字段面完整；
- required governance properties 无 hidden default；
- `PrimitiveOwner` / `StateDomain` 保持 nominal shell，未把 candidate 值表升格为规范；
- generic persistence validator只编码 canonical object-class matrix；
- 未编码 DesignSpec、GenerationCompiler、B08 knowledge 等 object-specific policy。

未发现 blocker。

### 3.4 `RegistryIndex`

- derived runtime view，不是 canonical object；
- exact `ObjectType` lookup；
- reference-kind guard先于 eligibility guard；
- 不进行 resolver target lookup 或 content-hash target verification。

未发现 blocker。

## 4. Scope / Leakage Review

PR changed files集中于：

```text
P1 design/plan/audit/review docs
pyproject dependency
core refs/hash
registry models/validation/index
P1 tests
P1 CI workflow
P0/P1 scope regression tests
```

未发现以下 production implementation：

```text
B01-B08 object models
ARSO shadow models
ExactReferenceResolver
CanonicalObjectStore
CAS / BranchHead runtime
Commands
Events
Protocols
Snapshot firewall
UI / LLM / image / vector DB / optimizer
```

结论：`NO P2 LEAKAGE`。

## 5. Verification Review

在实现审查前取得的功能验证基线：

```text
PR head: c3fa772edc46adf7a373d36aa123ec9394d61051
Actions run: 33745660896
P1 targeted: 49 PASS
Root repository: 76 PASS
Candidate baseline: 46 PASS
Spec checksums: 7 / 7 OK
Compile: PASS
Whitespace gates: PASS
Authoritative source drift: PASS
```

Audit/Review 文档提交后必须再次以最终 head 跑同一 CI；最终 Freeze 状态只能引用最终 head 的 fresh evidence。

## 6. Findings

### Critical

`0`

### Important

`0`

### Minor

`1`

`CI-M01`：GitHub runner 对 `actions/checkout@v4` 和 `actions/setup-python@v5` 输出 Node 20 deprecation warning。当前平台使用 Node 24 compatibility path，所有 verification step 成功。

处置：`NON-BLOCKING / CI MAINTENANCE`。不在 P1 contract freeze 中升级 action major version，以避免把非 contract maintenance 混入阶段收尾。

## 7. Freeze Review Decision

P1 本身满足已批准 P1 written Spec 的实现与 conformance 要求，未发现需要重开 P1 contract design 的 Critical/Important 问题。

Review verdict：

```text
P1 IMPLEMENTATION: PASS
P1 SPEC CONFORMANCE: PASS
P1 SCOPE BOUNDARY: PASS
P1 BASELINE/SPEC DRIFT: PASS
P1 FREEZE REVIEW: PASS
```

推荐状态：

```text
P0: FROZEN
P1: COMPLETE / AUTOMATED CHECKS PASS / INDEPENDENT FREEZE REVIEW PASS / AWAITING USER FREEZE REVIEW
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

只有用户明确批准 P1 Frozen Checkpoint 后，才允许把 P1 标记为 `FROZEN` 并讨论是否授权 P2。
