# Shared Canonical Shell Field Decision Ledger

日期：2026-09-05  
阶段：P2.0A｜Shared Canonical Shell Support Contract Recovery  
状态：`RECOVERY DECISIONS COMPLETE / NORMATIVE CONTRACT PENDING`

## 1. Decision vocabulary

每个 decision 必须属于：

```text
DIRECT_FROZEN
NORMALIZED_RECOVERY
NEW_FREEZE_DECISION
DEFERRED
REJECTED
```

`di_contracts_v1` 仅作为 executable/structural evidence；不能单独支撑 `DIRECT_FROZEN`。

## 2. Ownership boundary

P2.0A 冻结的是全局 canonical shell 的 **support/nested types 与 structural bases**，不是新的 canonical domain primitive。

因此以下类型：

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
ImmutableFact structural base
```

均：

```text
Object Registry entry = NONE
primitive owner entry = NONE
historical_ssot entry = N/A
persistent_ref_kind entry = N/A
```

它们被 canonical objects 嵌套/继承，但自身不是独立 canonical object。

---

# 3. Actor identity

## 3.1 ActorId

| Property | Exact decision | Source status | Decision |
|---|---|---|---|
| semantic role | creator/actor opaque identity | `created_by` globally required; candidate suggests distinct ActorId | NORMALIZED_RECOVERY |
| wire | strict non-empty JSON string | no authoritative lexical grammar | NEW_FREEZE_DECISION |
| nominal distinction | `ActorId != ObjectId != LogicalId != TenantId` | P0 identity separation principle + auditability | NEW_FREEZE_DECISION |
| candidate opaque regex | `^[A-Za-z0-9][A-Za-z0-9._:-]{15,127}$` | candidate only | REJECTED |
| business-readable semantics | not required and not prohibited by wire grammar beyond non-empty | no authority | NEW_FREEZE_DECISION |

Rationale：P0 deliberately declined to freeze candidate lexical regex for ObjectId/LogicalId. P2.0A must not reintroduce that same regex indirectly for ActorId.

## 3.2 ActorType

Candidate evidence:

```text
USER
SERVICE
AGENT
SYSTEM
EXTERNAL
```

Decision：

```text
ActorType = strict non-empty JSON string with open vocabulary
```

Standard recognized codes and frozen minimum meanings：

| Code | Minimum semantic meaning | Decision |
|---|---|---|
| `USER` | attribution to an end-user/human user identity | NORMALIZED_RECOVERY |
| `SERVICE` | attribution to a non-agent software/service principal acting through a service boundary | NORMALIZED_RECOVERY |
| `AGENT` | attribution to an autonomous or semi-autonomous software actor whose action is represented as agent behavior rather than an undifferentiated backend service | NORMALIZED_RECOVERY |
| `SYSTEM` | attribution to an internal platform/system mechanism when no narrower user/service/agent principal is the intended actor | NORMALIZED_RECOVERY |
| `EXTERNAL` | attribution to a principal outside the local identity taxonomy/system boundary | NORMALIZED_RECOVERY |

Closed-enum exhaustiveness：`REJECTED`。

Additional codes：allowed if strict non-empty strings; they MUST NOT redefine the standard codes.

Why open：authority proves creator attribution but not an exhaustive actor taxonomy. Future integrations may need actor classes such as organization-owned automation, federated principal families, or hardware/executor identities without revising every canonical schema.

## 3.3 ActorRef

Exact wire：

```yaml
ActorRef:
  actor_type: ActorType
  actor_id: ActorId
```

| Field | Type | Cardinality | Required | Decision |
|---|---|---:|---:|---|
| `actor_type` | ActorType | scalar | yes | NORMALIZED_RECOVERY |
| `actor_id` | ActorId | scalar | yes | NORMALIZED_RECOVERY |

Forbidden fields in Exact V1 shared attribution：

```text
display_name
email
roles
permissions
organization
auth_provider
session/token data
```

Those belong to identity/IAM/profile systems, not immutable canonical attribution.

SC01 closure candidate：`COMPLETE`。

---

# 4. Tenant isolation

## 4.1 TenantId

| Property | Exact decision | Decision |
|---|---|---|
| semantic role | opaque identity of one tenant isolation domain | NORMALIZED_RECOVERY |
| wire | strict non-empty JSON string | NEW_FREEZE_DECISION |
| nominal distinction | `TenantId != ActorId/ObjectId/LogicalId` | NEW_FREEZE_DECISION |
| candidate opaque regex | not imported | REJECTED |

## 4.2 TenantScopeType

Exact closed values：

```text
GLOBAL
TENANT
```

Decision：`NORMALIZED_RECOVERY / CLOSED ENUM`。

Why closed here：this enum models infrastructure tenant isolation only. Domain/semantic scopes such as Brand, Project, Collection, Category, User, Style, etc. are separate owner-level scope concepts inside an isolation domain and MUST NOT be added to `TenantScopeType`.

## 4.3 TenantScope

Exact wire：

```yaml
TenantScope:
  scope_type: TenantScopeType
  tenant_id: TenantId | null
```

| Invariant | Exact decision |
|---|---|
| `GLOBAL` | `tenant_id MUST be null` |
| `TENANT` | `tenant_id MUST be non-null` |

Both fields are required in the wire shape.

Important semantic guard：

```text
GLOBAL
=
not bound to one tenant isolation domain

GLOBAL
!=
public
!= anonymous
!= permissionless
!= cross-tenant-readable-by-default
```

Authorization/access remains owner/governance policy.

Rejected shared fields：

```text
tenant_ids[]
project_id
brand_id
user_id
knowledge_scope
cross_tenant_use
```

SC02 closure candidate：`COMPLETE`。

---

# 5. Provenance

## 5.1 Role

Frozen purpose：trace immutable canonical content to exact canonical inputs and/or opaque external non-canonical source identifiers.

It does not own：

```text
creator attribution -> created_by
creation time       -> created_at
command correlation -> Command/Event metadata
runtime execution   -> RunRecord/Event
approval             -> Review/Governance records
```

## 5.2 Exact wire

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  external_source_refs: Tuple[str]
```

| Field | Type | Cardinality | Required | Rule | Decision |
|---|---|---:|---:|---|---|
| `source_refs` | `Tuple[CanonicalRef]` | ordered tuple, may empty | yes | `ExactObjectRef | ObjectRef` only; LogicalObjectRef forbidden | NEW_FREEZE_DECISION |
| `external_source_refs` | `Tuple[str]` | ordered tuple, may empty | yes | every value strict non-empty string | NEW_FREEZE_DECISION |

Ordering is preserved for deterministic wire serialization. The contract does not assert semantic significance of ordering unless an owner-specific contract says so.

## 5.3 Candidate field decisions

### `command_ref: ObjectRef | None`

Decision：`REJECTED`。

Reason：Global Exact Contract states Commands/Events have their own identity/correlation metadata and MUST NOT be registered as canonical domain primitives merely because persisted. `ObjectRef` is a persistent canonical-object reference; therefore encoding a command as `ObjectRef` would silently change command ontology.

Future command causality may be represented by Command/Event-owned correlation/causation identifiers or a dedicated typed reference after command inventory freeze, without changing Provenance's canonical-source list.

### `run_ref: ObjectRef | None`

Decision：`DEFERRED / NOT PRESENT IN V1 SHARED SHELL`。

Reason：`RunRecord` is ARSO-owned and exact production integration remains later. P2.0A cannot select its canonical object class or persistent ref kind. If an authoritative RunRecord later qualifies as a canonical provenance source, its owner-approved exact ref may be placed in `source_refs` without schema change.

## 5.4 External source semantics

`external_source_refs` is intentionally opaque in P2.0A：

```text
strict non-empty string
```

P2.0A does not freeze URI scheme, digest format, document identifier taxonomy, or ExternalSourceRef object model.

SC03 closure candidate：`COMPLETE`。

---

# 6. ObjectRevision

## 6.1 Exact wire

```text
JSON integer >= 1
```

Decision：`NORMALIZED_RECOVERY + NEW_FREEZE_DECISION on lower bound`。

Evidence：

```text
ID != LogicalID != Revision != SchemaVersion
revision = server-assigned ordering metadata only
parentage = parent_refs
```

Candidate uses `Annotated[int, Field(ge=1)]`; this agrees with the normalized interpretation but does not become authority by itself.

## 6.2 Frozen semantics

```text
server-assigned
ordering metadata only
not ObjectId
not LogicalId
not SchemaVersion
not ConcurrencyVersion
not a parent pointer
not a client-generated authority
```

## 6.3 Explicit non-guarantees

P2.0A does NOT require：

```text
revision == previous_revision + 1
contiguous allocation
revision arithmetic to infer parentage
global uniqueness across logical objects
allocation algorithm
CAS semantics
```

A store may use monotone ordering per logical object, but allocator/concurrency proof belongs to later store conformance. Parentage is always represented by `parent_refs`.

SC04 closure candidate：`COMPLETE`。

---

# 7. Shared canonical structural bases

## 7.1 JSONValue

P2.0A consumes the Pydantic/JSON-native concept already used by Exact V1 extensions and hashing. It does not create a new canonical primitive.

## 7.2 CanonicalObject

Exact common wire fields：

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

All fields required.

Decision provenance：

- field presence/role: `DIRECT_FROZEN` by global Exact Contract §6;
- exact `ActorRef/TenantScope/Provenance` internals: P2.0A normalized recovery;
- required empty-capable `extensions` map: normalized strict canonical wire choice consistent with namespaced extension policy.

## 7.3 CanonicalRevision

Adds：

```yaml
logical_id: LogicalId
revision: ObjectRevision
parent_refs: Tuple[ExactObjectRef]
```

All fields required. `parent_refs` may be empty for a root/initial revision where the owner/store permits it.

No arithmetic linkage between `revision` and `parent_refs` is valid.

## 7.4 ImmutableFact

Structural base adds no shared wire field beyond CanonicalObject.

Concrete canonical object registry entries determine `object_type`, owner, state domain and reference policy; structural bases/support types are not registered as domain primitives.

---

# 8. Timestamp normalization

Global rule：`ISO-8601 UTC timestamps`。

P2.0A runtime normalization for canonical-shell timestamps：

```text
naive datetime -> reject
aware datetime -> normalize to UTC
stored runtime value -> UTC-aware
serialized time -> ISO-8601 representation of the same UTC instant
```

This applies to canonical shell fields such as `created_at` only. Command/Event timestamp inventories remain out of scope.

Decision：`NORMALIZED_RECOVERY`。

---

# 9. CanonicalPayload boundary

P2.0A does not create one universal semantic content-hash policy.

Inherited global rule：

```text
content_hash itself excluded
transport-only metadata excluded
mutable operational fields excluded
created_at/created_by excluded for semantic revision hashes unless explicit owner policy overrides
```

B01 owner contract already explicitly excludes from B01 semantic content hash：

```text
id
logical_id
revision
parent_refs
created_at
created_by
tenant_scope
provenance
```

P2.0A validates those field types but does not override B01 payload selection and does not decide B02+ owner payload policy.

---

# 10. P0/P1 compatibility ledger

P2.0A MUST NOT alter：

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
RFC8785 canonicalization/hash engine
registry foundation semantics
```

Specific rejected backdoor changes：

```text
adding candidate opaque-ID regex to existing P0 nominal IDs
closing ActorType solely because candidate used StrEnum
adding canonical ObjectRef semantics to Command/Event
choosing ARSO RunRecord ref kind
adding registry entries for nested support types
```

---

# 11. Scope exclusions

Explicitly deferred/outside P2.0A：

```text
ConcurrencyVersion
OperationalControlState full exact schema
Command/Event full identity/correlation model
CommandRef/EventRef types
ARSO RunRecord integration
IAM/auth/permission models
external source URI/digest ontology
ObjectId/LogicalId/SchemaVersion/ObjectType lexical grammar
store revision allocator
CAS/resolver implementation
B01/B02 production models
```

---

# 12. Closure summary

| Blocker | Recovery candidate | Status |
|---|---|---|
| SC01 ActorRef | ActorId + open ActorType + 2-field ActorRef | CLOSED IN RECOVERY CANDIDATE |
| SC02 TenantScope | TenantId + closed GLOBAL/TENANT discriminator | CLOSED IN RECOVERY CANDIDATE |
| SC03 Provenance | canonical `source_refs` + opaque `external_source_refs`; command rejected, run deferred | CLOSED IN RECOVERY CANDIDATE |
| SC04 ObjectRevision | positive integer server ordering metadata | CLOSED IN RECOVERY CANDIDATE |

Current result：

```text
shared-core SPEC_CONFLICT discovered = 0
blocking shared-core field SPEC_GAP = 0 in recovery candidate
normative companion contract = PENDING
P2.0A = NOT YET FROZEN
P2 = NOT AUTHORIZED
```
