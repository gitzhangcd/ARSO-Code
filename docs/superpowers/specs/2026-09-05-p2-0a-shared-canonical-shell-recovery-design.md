# P2.0A Shared Canonical Shell Support Contract Recovery Design

日期：2026-09-05  
阶段：P2.0A｜Shared Canonical Shell Support Contract Recovery  
状态：`WRITTEN SPEC / AWAITING USER APPROVAL`  
目标：解除 P2.0 独立 Freeze Review 发现的 SC01–SC04 shared-core blockers，使 P2 能在不复制 candidate、不猜 contract 的前提下实现完整 B01 canonical models。

---

# 1. Problem Statement

P2.0 已经完成 B01 owner-field recovery：

```text
7 / 7 B01 objects covered
B01 owner-field SPEC_GAP = 0
B01 SPEC_CONFLICT = 0
```

但 B01 canonical models 共同依赖 global canonical shell：

```text
created_by
tenant_scope
provenance
revision   [for versioned objects]
```

独立 Freeze Review 发现 authority chain 只冻结了这些字段的角色/语义，没有冻结 support types 的 exact wire contract：

```text
SC01 ActorRef
SC02 TenantScope
SC03 Provenance
SC04 ObjectRevision
```

Candidate baseline 提供了一套可运行结构，但：

```text
di_contracts_v1 != normative authority
```

因此不能直接 copy。

---

# 2. Design Classification

这是一个 **global structural contract recovery**，不是 B01 owner extension。

P2.0A 不增加新的 canonical domain primitive；它冻结的是多个 owner 共享的 support/nested types 与 structural bases。

Authority relation proposal：

```text
1A  DI-V5-EXACT-CONTRACT
1B  Shared Canonical Shell Support Contract [P2.0A candidate]
1C  DI-B01-EXACT-CONTRACT
2+  existing authority chain
```

Rules：

```text
1B MUST NOT override 1A.
1C MUST consume 1B but MUST NOT redefine shared support internals.
1B MUST NOT absorb B01/B02/ARSO primitive owner fields.
```

The final priority labels may be normalized during Recovery Implementation; the semantic requirement is that global shared-shell contract outranks owner-specific field contracts but remains subordinate to the global Exact Contract.

---

# 3. Scope

## 3.1 In scope

```text
ActorId
ActorType
ActorRef

TenantId
TenantScopeType
TenantScope

Provenance
ObjectRevision

CanonicalObject shared structural base
CanonicalRevision shared structural base
ImmutableFact structural base dependency
UTC canonical timestamp normalization rule
```

## 3.2 Out of scope

```text
ObjectId / LogicalId regex changes
SchemaVersion regex changes
ObjectType namespace regex changes
ConcurrencyVersion
OperationalControlState full schema
Command/Event full identity metadata
ARSO RunRecord exact integration
IAM/authentication/permission models
ExternalSourceRef URI/digest ontology
B01 production Pydantic models
B02+ owner schemas
canonical store implementation
CAS / resolver implementation
revision-allocation uniqueness policy
```

---

# 4. Considered Approaches

## 4.1 Approach A｜Clone candidate shell

Adopt candidate unchanged：

```text
ActorType = closed USER/SERVICE/AGENT/SYSTEM/EXTERNAL
TenantScopeType = GLOBAL/TENANT
Provenance = source_refs + command_ref + run_ref + external_source_refs
ObjectRevision = int>=1
```

### Rejected because

1. No authority proves ActorType taxonomy exhaustive.
2. `command_ref: ObjectRef` risks violating the global rule that Commands/Events are not canonical domain primitives merely because persisted.
3. `run_ref: ObjectRef` prematurely chooses ARSO `RunRecord` classification/ref semantics before AC-03/P4 integration.
4. Candidate convenience would become global contract without independent reasoning.

Verdict：`REJECTED`。

## 4.2 Approach B｜Minimal normalized shell

Freeze only the structural data required for exact canonical models：

```text
ActorRef = typed actor identity, open actor vocabulary
TenantScope = binary isolation boundary GLOBAL/TENANT
Provenance = canonical sources + external sources
ObjectRevision = positive integer ordering metadata
```

No Command/Event/Run coupling.

Verdict：`RECOMMENDED`。

## 4.3 Approach C｜Generic JSON envelopes

```text
created_by: str
tenant_scope: dict
provenance: dict
revision: int
```

Rejected because it defeats strict validation, tenant invariants, semantic auditability, and static conformance.

Verdict：`REJECTED`。

---

# 5. Actor Contract

## 5.1 ActorId

Exact V1 semantics：

```text
ActorId = opaque nominal actor identity
```

Requirements：

```text
strict string
immutable
non-empty
no business-readable semantics required
no candidate opaque-ID regex imported
```

Distinctness：

```text
ActorId != ObjectId
ActorId != LogicalId
ActorId != TenantId
```

Rationale：P0 already refused to freeze candidate lexical regex for ObjectId/LogicalId. P2.0A should not reintroduce that regex indirectly for new IDs.

## 5.2 ActorType

Exact V1 semantics：

```text
ActorType = open typed vocabulary
```

Standard recognized codes：

```text
USER
SERVICE
AGENT
SYSTEM
EXTERNAL
```

Standard semantic boundaries：

| Code | Exact V1 meaning |
|---|---|
| `USER` | 由可识别的人类用户/操作员发起并归因到该交互用户身份的动作。 |
| `SERVICE` | 由非 Agent 的软件服务、后台进程或集成服务身份执行的动作；该值本身不声称具有自主决策语义。 |
| `AGENT` | 由在委托权限下进行自主或半自主决策的软件 Agent 身份执行的动作。 |
| `SYSTEM` | 由平台/系统自身生成、且没有更具体独立 `SERVICE` 或 `AGENT` 身份可归因时使用的系统级动作。 |
| `EXTERNAL` | 由本系统管理 actor namespace 之外的主体执行或导入、但仍具有稳定外部 actor identity 的动作。 |

Rules：

```text
standard codes retain exact spelling and meanings above
additional non-empty values allowed
additional values MUST NOT redefine a standard code
no closed-enum exhaustiveness claim
```

Rationale：creator categories can expand; authority does not prove the candidate five-value set exhaustive.

## 5.3 ActorRef

Exact wire：

```yaml
ActorRef:
  actor_type: ActorType
  actor_id: ActorId
```

Both fields required.

Forbidden fields：

```text
display_name
email
roles
permissions
organization
authentication provider
session
```

`ActorRef` is identity attribution, not IAM/profile state.

---

# 6. Tenant Isolation Contract

## 6.1 TenantId

Exact V1 semantics：

```text
TenantId = opaque nominal tenant identity
```

Requirements：

```text
strict string
immutable
non-empty
no candidate regex imported
TenantId != ActorId/ObjectId/LogicalId
```

## 6.2 TenantScopeType

Exact closed values：

```text
GLOBAL
TENANT
```

Exact meanings：

| Value | Exact V1 meaning |
|---|---|
| `GLOBAL` | 该对象不归属于某一个特定 tenant isolation boundary。是否允许跨 tenant 使用仍由 owner/governance policy 决定；`GLOBAL` **不等于 public / anonymous access**。 |
| `TENANT` | 该对象被隔离并归属于恰好一个 `tenant_id`；不得在未经过明确 governance/promotion 的情况下跨 tenant 使用。 |

Why closed here：

- global/tenant is an infrastructure isolation boundary;
- Brand/Project/Collection/User are semantic/domain scopes inside a tenant, not alternatives to tenant isolation;
- ARSO tenant-isolation text distinguishes tenant-specific material from global knowledge.

## 6.3 TenantScope

Exact wire：

```yaml
TenantScope:
  scope_type: TenantScopeType
  tenant_id: TenantId | null
```

Both fields required.

Validation：

```text
GLOBAL -> tenant_id MUST be null
TENANT -> tenant_id MUST be non-null
```

Forbidden：

```text
tenant_ids[]
project_id
brand_id
user_id
knowledge_scope
cross_tenant_use flag
```

A canonical object belongs to one tenant isolation scope. Cross-tenant/global promotion is a governance operation producing new canonical truth where owner policy permits; it is not represented by a multi-tenant scope envelope.

---

# 7. Provenance Contract

## 7.1 Role

Provenance answers：

> 这个 canonical object 的内容来自哪些 exact canonical sources，或哪些外部 non-canonical sources？

It does not answer：

```text
who created it        -> created_by
when created          -> created_at
which command mutated -> command/event history
which runtime status  -> Run/Event records
```

## 7.2 Exact wire

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  external_source_refs: Tuple[str]
```

Both fields required; each tuple may be empty.

Rules：

```text
source_refs only ExactObjectRef/ObjectRef
LogicalObjectRef forbidden
external_source_refs are non-empty opaque stable references, not free-form notes
ordering preserved
immutable
```

## 7.3 Candidate fields explicitly rejected/deferred

### `command_ref: ObjectRef`

`REJECTED`。

Reason：Global Exact Contract explicitly separates Command/Event identity from canonical domain primitives. P2.0A must not encode command persistence as ObjectRef semantics.

### `run_ref: ObjectRef`

`DEFERRED`。

Reason：`RunRecord` is ARSO-owned. Its exact production import/ref policy remains an AC-03/P4 issue. If a future RunRecord is a canonical provenance source, its owner-approved persistent ref can enter `source_refs` without changing Provenance shape.

## 7.4 Why not a generic map

A generic `dict[str, Any]` would allow hidden mutable status, logical refs, or duplicated owner fields. Exact V1 requires typed provenance, not free-form metadata.

---

# 8. ObjectRevision Contract

Exact wire：

```text
JSON integer >= 1
```

Semantics：

```text
server-assigned ordering metadata
not object identity
not SchemaVersion
not a concurrency token
not parentage
not client authority
```

Rules：

```text
revision arithmetic MUST NOT infer lineage
parentage is only parent_refs
branching remains legal
revision need not be contiguous
```

P2.0A deliberately does not freeze allocation algorithm or store uniqueness; those belong to store/concurrency conformance.

---

# 9. Shared Canonical Structural Bases

These are structural implementation contracts, not Object Registry primitives.

## 9.1 CanonicalObject

Exact common wire：

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

All fields required in the canonical wire shape.

## 9.2 CanonicalRevision

Adds：

```yaml
  logical_id: LogicalId
  revision: ObjectRevision
  parent_refs: Tuple[ExactObjectRef]
```

All fields required. `parent_refs` may be empty only where owner/store semantics permit an initial/root revision.

## 9.3 ImmutableFact

No additional common fields beyond CanonicalObject.

The concrete subclass/object registry determines：

```text
object_class
historical_ssot
persistent_ref_kind
state_domain
primitive owner
```

## 9.4 Registry exclusion

Support/nested types do not get manifest entries：

```text
ActorId
ActorType
ActorRef
TenantId
TenantScopeType
TenantScope
Provenance
ObjectRevision
CanonicalObject structural base
CanonicalRevision structural base
```

They are not independent canonical domain objects.

---

# 10. UTC Timestamp Rule

Global rule：

```text
ISO-8601 UTC timestamps
```

P2.0A exact runtime normalization：

```text
naive datetime -> reject
aware datetime -> normalize to UTC
canonical model stores UTC-aware datetime
JSON serialization represents UTC time
```

This rule applies to canonical shell timestamps such as `created_at`; it does not redefine Event/Command-specific time contracts.

---

# 11. CanonicalPayload Boundary

P2.0A defines field types, not one universal owner hash policy.

Inherited N09：

```text
content_hash excluded
transport-only metadata excluded
mutable operational fields excluded
created_at/created_by excluded for semantic revision hashes unless explicit owner policy overrides
```

B01 already freezes：

```text
created_at
created_by
tenant_scope
provenance
id
logical_id
revision
parent_refs
```

as excluded from B01 semantic content hash.

P2.0A does not override that choice and does not decide B02+ owner payload selections.

---

# 12. Exactness / Requiredness Table

| Type | Field / wire | Required | Cardinality | Exact decision |
|---|---|---:|---|---|
| ActorId | strict non-empty string | yes | scalar | nominal/open lexical |
| ActorType | strict non-empty string | yes | scalar | open vocabulary; 5 standard codes |
| ActorRef | actor_type | yes | scalar | ActorType |
| ActorRef | actor_id | yes | scalar | ActorId |
| TenantId | strict non-empty string | conditionally | scalar | nominal/open lexical |
| TenantScopeType | GLOBAL/TENANT | yes | scalar | closed enum |
| TenantScope | scope_type | yes | scalar | TenantScopeType |
| TenantScope | tenant_id | yes | scalar nullable | discriminator invariant |
| Provenance | source_refs | yes | tuple; may empty | CanonicalRef only |
| Provenance | external_source_refs | yes | tuple; may empty | non-empty stable string values |
| ObjectRevision | integer >=1 | yes on revisions | scalar | ordering metadata |
| CanonicalObject | canonical metadata shell | yes | structural | global field mapping |
| CanonicalRevision | logical_id/revision/parent_refs | yes | structural | versioned shell |

---

# 13. Compatibility with Frozen P0/P1

P2.0A MUST NOT change：

```text
ObjectId
LogicalId
SchemaVersion
ObjectType
CanonicalObjectClass
DIModel
FrozenDIModel
ContentHash
ExactObjectRef
ObjectRef
LogicalObjectRef
CanonicalRef
RFC8785 hash engine
registry foundation semantics
```

New types will eventually extend the existing core package rather than revise those contracts.

Candidate regexes for ActorId/TenantId are not imported because that would indirectly contradict P0's explicit decision not to freeze the common opaque-ID regex.

---

# 14. Expected P2 Unblock

After this written design is approved, Recovery Implementation should generate a scoped normative companion contract and re-run the P2.0 independent review.

Expected blocker closure：

```text
SC01 ActorRef       -> CLOSED
SC02 TenantScope    -> CLOSED
SC03 Provenance     -> CLOSED
SC04 ObjectRevision -> CLOSED
```

Then P2.0 can be re-evaluated as：

```text
B01 owner-field contract complete
+
shared canonical shell exact contract complete
+
P2.0 verification pass
=
P2.0 READY FOR USER FREEZE DECISION
```

This still does not automatically authorize P2; explicit user Freeze/authorization remains required.

---

# 15. Recovery Implementation Deliverables After Approval

If this written spec is approved, the next plan should create/update only contract/governance artifacts, not B01 production code：

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
SHARED_CORE_FIELD_DECISION_LEDGER.md
SHARED_CORE_CROSS_SPEC_FREEZE_AUDIT.md
P2_0A_FREEZE_REVIEW.md
SPEC_AUTHORITY.md
specs/SPEC_SOURCE_CHECKSUMS.sha256
README.md
AGENTS.md
P2.0A verification workflow/gates as needed
```

No production implementation：

```text
src/design_intelligence/contracts/core/* new implementation
src/design_intelligence/contracts/b01/*
```

until the relevant Freeze checkpoint is approved.

---

# 16. Written Spec Decision

Current candidate conclusion：

```text
Approach B = RECOMMENDED
SPEC_CONFLICT = 0
blocking written-design ambiguity = 0
P2.0A written design = READY FOR USER REVIEW
P2 = NOT AUTHORIZED
```
