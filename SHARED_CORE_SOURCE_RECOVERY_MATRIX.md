# Shared Canonical Shell Source Recovery Matrix

日期：2026-09-05  
阶段：P2.0A｜Shared Canonical Shell Support Contract Recovery  
状态：`RECOVERY CANDIDATE / WRITTEN DESIGN PREPARATION`

## 1. 目的

P2.0 独立 Freeze Review 已确认：B01 owner fields 已经收敛，但完整 B01 canonical models 仍依赖未冻结的 shared canonical-shell support contract。

当前 blocking surface：

```text
P2.0-SC01 ActorRef
P2.0-SC02 TenantScope
P2.0-SC03 Provenance
P2.0-SC04 ObjectRevision
```

为避免把 `di_contracts_v1` candidate 直接提升为 authority，本矩阵先恢复现有规范真正提供的语义证据，再区分：

```text
DIRECT_FROZEN
STRONG_RECOVERY
NORMALIZED_RECOVERY
NEW_FREEZE_DECISION
REJECTED_CANDIDATE
DEFERRED
```

本矩阵本身不成为新的 normative contract；它是 P2.0A written spec 的 provenance。

---

# 2. Authority evidence

## 2.1 Global Exact Contract

`DI-V5-EXACT-CONTRACT` 已冻结：

```text
Python >= 3.12
Pydantic v2
ISO-8601 UTC timestamps
opaque identifiers
strict validation
extra="forbid"
frozen=True for core canonical models
```

稳定 DI canonical objects require, where applicable：

```text
schema_version
id
object_type
created_at
created_by
tenant_scope
provenance
extensions
```

Versioned revision additionally requires：

```text
logical_id
revision
parent_refs
```

Revision semantics 已冻结：

```text
revision = server-assigned ordering metadata only
parentage = parent_refs
revision + 1 MUST NOT infer lineage
ID != LogicalID != Revision != SchemaVersion
```

Global Exact Contract 同时明确：

```text
Commands and events have their own identity/correlation metadata
and MUST NOT be registered as canonical domain primitives merely because persisted.
```

这一条对 candidate `Provenance.command_ref: ObjectRef` 构成直接约束。

## 2.2 ARSO Engineering

ARSO Engineering 的 Common Data Contract 对 stable model 至少要求：

```text
schema_version
id
created_at
created_by
provenance
```

并要求：

```text
ISO-8601 UTC
opaque ID
extra="forbid"
```

Tenant isolation 章节明确：

```text
tenant-specific evidence
tenant-specific artifacts
tenant-specific preference
```

默认不得直接进入 global knowledge。

因此 shared tenant scope 的核心职责是 **isolation boundary**，而不是承载 Brand/Project/Category 等领域语义 scope。

## 2.3 P0 frozen implementation boundary

P0 正式冻结的 production core 只包括：

```text
ObjectId
LogicalId
SchemaVersion
ObjectType
CanonicalObjectClass
DIModel
FrozenDIModel
```

P0 没有冻结：

```text
ActorId
ActorType
ActorRef
TenantId
TenantScopeType
TenantScope
Provenance
ObjectRevision
CanonicalObject / CanonicalRevision structural base
```

因此这些不能以“P0 已经有 core”作为隐式授权。

## 2.4 P1 frozen boundary

P1 正式冻结：

```text
ContentHash
ExactObjectRef
ObjectRef
LogicalObjectRef
CanonicalRef
RFC8785 canonical hash engine
registry foundation
```

因此 P2.0A 可直接依赖：

```text
CanonicalRef := ExactObjectRef | ObjectRef
```

但不能重新定义 persistent reference semantics。

## 2.5 Candidate baseline

`di_contracts_v1` 当前 candidate proposes：

```text
ActorId = opaque string
TenantId = opaque string

ActorType = USER | SERVICE | AGENT | SYSTEM | EXTERNAL
TenantScopeType = GLOBAL | TENANT

ActorRef:
  actor_type
  actor_id

TenantScope:
  scope_type
  tenant_id?

Provenance:
  source_refs
  command_ref
  run_ref
  external_source_refs

ObjectRevision = integer >= 1
```

这些只能作为 structural evidence。

---

# 3. Recovery strategy comparison

## Approach A｜Candidate-convergent clone

直接复制 candidate：

```text
ActorType closed 5-value enum
TenantScopeType GLOBAL/TENANT
Provenance source_refs + command_ref + run_ref + external_source_refs
ObjectRevision int>=1
```

优点：最快；与 baseline 兼容。

缺点：

- `ActorType` closed enum 缺少 authority 依据；
- `command_ref: ObjectRef` 与 command/event 非 canonical-domain-primitive 边界存在潜在冲突；
- `run_ref` 会提前决定 ARSO `RunRecord` ref/class integration；
- 会把 candidate-specific convenience 误升格为 global contract。

结论：`REJECTED`。

## Approach B｜Minimal normalized shared shell

只冻结 P2/P3… 所有 canonical models 真正需要的最小 global support surface：

```text
ActorId
ActorType [open typed vocabulary]
ActorRef

TenantId
TenantScopeType [GLOBAL/TENANT]
TenantScope

Provenance [canonical source refs + external source refs only]

ObjectRevision [positive integer ordering metadata]

CanonicalObject / CanonicalRevision shared structural shell
UTC timestamp normalization rule
```

优点：

- 不替 Command/Event/ARSO RunRecord 提前决定 ref policy；
- tenant scope 只承担 isolation，不混入 domain scope；
- actor taxonomy 可扩展；
- 足以解除 B01 exact model 的 shared-shell blocker。

结论：`RECOMMENDED`。

## Approach C｜Generic open envelope

例如：

```text
created_by: str
tenant_scope: dict
provenance: dict
revision: int
```

优点：扩展性最大。

缺点：失去 strict typing、tenant invariant、reference safety、conformance 可测试性。

结论：`REJECTED`。

---

# 4. Actor recovery matrix

## 4.1 ActorId

### Authority evidence

Global contracts require opaque identifiers and a stable `created_by` identity, but do not freeze actor-id lexical grammar.

### Candidate evidence

Candidate defines `ActorId` using the same opaque-string regex family as ObjectId/LogicalId.

### Recovery decision

```text
ActorId = distinct nominal strict string identity
```

V1 does **not** copy the candidate opaque-id regex because P0 deliberately did not freeze that lexical grammar even for ObjectId/LogicalId.

Required semantic rules：

```text
ActorId != ObjectId
ActorId != LogicalId
ActorId != TenantId
ActorId carries no display-name/email/business semantics
```

Decision：`NEW_FREEZE_DECISION`。

## 4.2 ActorType

### Authority evidence

Current authority chain needs to distinguish creator/actor identity for audit, but does not define a complete actor taxonomy.

### Candidate evidence

```text
USER
SERVICE
AGENT
SYSTEM
EXTERNAL
```

### Recovery decision

Freeze `ActorType` as an **open typed string vocabulary**, not a closed enum.

Exact V1 standard codes recognized at minimum：

```text
USER
SERVICE
AGENT
SYSTEM
EXTERNAL
```

Additional non-empty actor-type codes remain allowed. The five standard values retain their exact meanings and spellings.

Reason：Actor kinds can expand without requiring a global schema revision; current source does not prove exhaustiveness.

Decision：`NORMALIZED_RECOVERY + NEW_FREEZE_DECISION(open-set policy)`。

## 4.3 ActorRef

Proposed exact nested value：

```yaml
ActorRef:
  actor_type: ActorType
  actor_id: ActorId
```

Both fields required.

Rejected fields：

```text
display_name
email
role
organization
permissions
authentication_provider
```

Those belong to identity/IAM or business profile systems, not immutable canonical metadata.

Decision：`NORMALIZED_RECOVERY`。

---

# 5. Tenant recovery matrix

## 5.1 TenantId

Authority proves multi-tenant isolation but not lexical tenant-id format.

Decision：

```text
TenantId = distinct nominal strict string identity
```

No V1 regex copied from candidate.

Decision：`NEW_FREEZE_DECISION`。

## 5.2 TenantScopeType

Authority distinguishes tenant-specific state from global knowledge/isolation.

Candidate values：

```text
GLOBAL
TENANT
```

For the shared **tenant isolation** shell, Brand/Project/Collection/User etc. are not alternative tenant-scope classes; they belong to domain-specific scope models inside a tenant.

Therefore V1 freezes a closed enum：

```text
GLOBAL
TENANT
```

Decision：`STRONG_RECOVERY / CLOSED TWO-VALUE ENUM`。

## 5.3 TenantScope

Proposed exact nested value：

```yaml
TenantScope:
  scope_type: TenantScopeType
  tenant_id: TenantId | null
```

Both wire fields required.

Invariant：

```text
scope_type = GLOBAL  -> tenant_id MUST be null
scope_type = TENANT  -> tenant_id MUST be non-null
```

Forbidden：

```text
tenant_ids: []
project_id
brand_id
user_id
knowledge_scope
cross_tenant_use
```

Cross-tenant/global promotion must be an explicit governance action producing a new canonical state where allowed; it is not represented by a multi-tenant TenantScope object.

Decision：`STRONG_RECOVERY`。

---

# 6. Provenance recovery matrix

## 6.1 Stable semantic requirement

The authority chain repeatedly requires `provenance` on stable model families, snapshots, artifacts, evaluation/evidence objects, etc.

Therefore Provenance must support at least：

```text
canonical upstream sources
external/non-canonical upstream sources
```

It must remain immutable structured metadata and must not become a second event log.

## 6.2 Candidate structure audit

Candidate：

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  command_ref: ObjectRef | null
  run_ref: ObjectRef | null
  external_source_refs: Tuple[str]
```

### `source_refs`

Consistent with P1 exact persistent refs.

Verdict：`KEEP`。

### `external_source_refs`

Useful for imported files, URLs, publication IDs, legacy dataset IDs, etc. without pretending they are canonical objects.

Verdict：`KEEP`, but the exact URI/identifier grammar remains open.

### `command_ref: ObjectRef`

Global Exact Contract says Commands/Events have their own identity/correlation metadata and must not be registered as canonical domain primitives merely because persisted.

`ObjectRef` is a persistent canonical-object reference class.

Therefore candidate `command_ref: ObjectRef` would prematurely conflate command persistence with canonical primitive identity.

Verdict：`REJECTED_CANDIDATE`。

### `run_ref: ObjectRef`

`RunRecord` is ARSO-owned and its authoritative exact import/classification is scheduled for P4/AC-03. P2.0A must not pre-empt that owner decision.

If/when an ARSO RunRecord becomes a canonical source, it can participate through `source_refs` with the ref kind frozen by its owner.

Verdict：`DEFERRED / NOT IN SHARED V1 PROVENANCE SHAPE`。

## 6.3 Proposed exact Provenance

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  external_source_refs: Tuple[str]
```

Both fields required; either tuple may be empty.

Rules：

```text
source_refs MUST contain only persistent exact refs
LogicalObjectRef forbidden
external_source_refs are opaque non-empty strings
ordering preserved
no mutable status
no command/event lifecycle state
```

Decision：`NORMALIZED_RECOVERY`。

---

# 7. ObjectRevision recovery matrix

## 7.1 Direct semantics

Global Exact Contract directly freezes：

```text
revision = server-assigned ordering metadata only
revision != SchemaVersion
revision does not define parentage
parentage = parent_refs
branching legal
```

## 7.2 Candidate representation

```text
ObjectRevision = integer >= 1
```

This representation matches examples `v12 -> v13/v14` and provides a simple sortable wire scalar without embedding lineage.

## 7.3 Proposed exact V1 wire

```text
ObjectRevision = JSON integer >= 1
```

Additional rules：

```text
server assigned
not client authority
not a concurrency token
not an object identity
not a schema version
not required to be contiguous
MUST NOT infer parent_refs from revision arithmetic
```

P2.0A does not freeze revision-allocation/store uniqueness policy; AC-08/P13 store semantics remain responsible for lineage/concurrency behavior.

Decision：`STRONG_RECOVERY + NEW_FREEZE_DECISION(wire type/range)`。

---

# 8. Shared canonical structural shell

The global authority already freezes the field roles. P2.0A should therefore freeze the **exact structural dependency mapping**, without creating new registry primitives.

## 8.1 CanonicalObject structural base

```yaml
CanonicalObject:
  schema_version: SchemaVersion
  id: ObjectId
  object_type: ObjectType
  created_at: UTC datetime
  created_by: ActorRef
  tenant_scope: TenantScope
  provenance: Provenance
  extensions: map[str, JSONValue]
```

All fields required in canonical wire shape.

## 8.2 CanonicalRevision structural base

Adds：

```yaml
  logical_id: LogicalId
  revision: ObjectRevision
  parent_refs: Tuple[ExactObjectRef]
```

`parent_refs` required and may be empty only where the owner/store semantics permit an initial/root revision.

## 8.3 ImmutableFact structural base

No additional common fields beyond CanonicalObject.

Object class remains owner/registry metadata, not a serialized mutable field.

## 8.4 Support types are not canonical primitives

```text
ActorRef
TenantScope
Provenance
ObjectRevision
CanonicalObject structural base
CanonicalRevision structural base
```

are shared contract-support types. They do not receive Object Registry manifest entries and do not create a new `primitive_owner` domain.

Their authority is the global Exact Contract + scoped shared-core companion contract.

---

# 9. UTC timestamp recovery

Global Exact Contract already requires ISO-8601 UTC timestamps.

P2.0A proposes exact runtime normalization：

```text
naive datetime -> reject
aware datetime -> normalize to UTC
canonical JSON -> UTC timestamp representation
```

This matches candidate behavior without importing candidate as authority.

The exact byte representation still remains subject to RFC8785 JSON serialization after the model has produced JSON-native values.

Decision：`NORMALIZED_RECOVERY`。

---

# 10. CanonicalPayload interaction

P2.0A MUST NOT impose one global hash-field selection across all owners.

Global N09 remains：

```text
content_hash itself excluded
transport-only metadata excluded
mutable operational fields excluded
created_at / created_by excluded for semantic revision hashes unless owner overrides
```

B01 owner contract already freezes its owner-specific exclusion policy, including：

```text
tenant_scope
provenance
revision
parent_refs
```

P2.0A only defines exact types; it does not override B01 or future owner-specific CanonicalPayload policies.

---

# 11. Deferred / rejected surface

P2.0A intentionally does not freeze：

```text
ObjectId / LogicalId lexical regex [P0 nonblocking gap remains]
SchemaVersion lexical regex
ObjectType namespace regex
ConcurrencyVersion
OperationalControlState full exact schema
Command/Event identity metadata
ARSO RunRecord exact class/ref
ExternalSourceRef URI/checksum schema
IAM / authentication / permissions
Brand/Project/User domain scope
full canonical store behavior
revision allocation uniqueness policy
```

These are either already nonblocking frozen-stage gaps or belong to later owner/protocol/runtime stages.

---

# 12. Preliminary gap closure

If the proposed P2.0A written design is approved and converted into a scoped shared-core companion contract, the four P2.0 blockers map as：

| Blocker | Proposed closure | Remaining ambiguity |
|---|---|---|
| SC01 ActorRef | ActorId + open ActorType + exact ActorRef | 0 blocking for P2 |
| SC02 TenantScope | TenantId + GLOBAL/TENANT + discriminator invariant | 0 blocking for P2 |
| SC03 Provenance | exact source_refs + external_source_refs | 0 blocking for P2 |
| SC04 ObjectRevision | integer >=1, ordering-only semantics | 0 blocking for P2 |

Preliminary result：

```text
SPEC_CONFLICT = 0
P2.0A blocking design ambiguity = 0 in written candidate
P2 still NOT AUTHORIZED
```
