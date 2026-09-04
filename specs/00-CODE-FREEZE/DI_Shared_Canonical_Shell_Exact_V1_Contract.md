# Design Intelligence Shared Canonical Shell Exact V1 Contract

## Shared Support Types + Structural Canonical Bases

**Document ID:** `DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT`  
**Version:** `V1.0-FC1`  
**Date:** `2026-09-05`  
**Document Type:** Scoped Shared-Core Schema / Structural Contract  
**Status:** `FREEZE CANDIDATE`  
**Parent Authority:** `DI-V5-EXACT-CONTRACT V1.0-FC1`  
**Normative Scope:** global canonical-shell support/nested types and structural bases only

---

# 0. Authority and Scope

This document closes the shared canonical-shell exactness gap discovered by the independent P2.0 Freeze Review.

Authority relation:

```text
1A  DI-V5-EXACT-CONTRACT
    global / cross-domain / release authority

1B  DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT
    shared support/nested types and structural canonical bases

1C  DI-B01-EXACT-CONTRACT
    B01 field-level scoped authority

2+  existing authority chain
```

Rules:

```text
1B MUST NOT override 1A.
1C MUST consume 1B and MUST NOT redefine shared-shell support internals.
1B MUST NOT absorb B01/B02/ARSO primitive-owner fields.
1B support/nested types are NOT independent canonical domain primitives.
```

This contract exists so owner-specific canonical schemas can use an exact common shell without copying `di_contracts_v1` candidate structures.

---

# 1. Frozen Global Distinctions

The following inherited distinctions remain unchanged:

```text
ID != LogicalID != Revision != SchemaVersion
HistoricalTruthImmutable
OperationalPointersMayMutate
LogicalObjectRef = authoring only
ExactObjectRef / ObjectRef = persistent exact refs
parentage = parent_refs
Command/Event identity != canonical domain primitive identity
OneCanonicalObject => OnePrimitiveOwner
```

P2.0A does not reopen P0/P1.

---

# 2. Support-Type Status

The following are exact shared support/nested types or structural bases, not canonical domain primitives:

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

Therefore they MUST NOT receive Object Registry manifest entries merely because canonical objects contain or inherit them.

---

# 3. ActorId

## 3.1 Exact wire

```text
JSON string
strict
non-empty
immutable nominal identity
```

Nominal distinction:

```text
ActorId != ObjectId
ActorId != LogicalId
ActorId != TenantId
```

No additional lexical grammar is frozen in V1.

In particular, the candidate opaque-ID regex:

```text
^[A-Za-z0-9][A-Za-z0-9._:-]{15,127}$
```

is NOT part of this contract.

---

# 4. ActorType

## 4.1 Exact wire

```text
JSON string
strict
non-empty
open typed vocabulary
```

Exact V1 standard recognized codes:

```text
USER
SERVICE
AGENT
SYSTEM
EXTERNAL
```

These codes are normative minimum vocabulary, not an exhaustive closed enum.

Additional non-empty ActorType values MAY be introduced by integrations without changing this shared schema, but MUST NOT redefine the standard-code meanings.

## 4.2 Standard-code meanings

```text
USER
= end-user / human-user attribution

SERVICE
= non-agent software or service principal acting through a service boundary

AGENT
= autonomous or semi-autonomous software actor represented as agent behavior

SYSTEM
= internal platform/system mechanism used when no narrower USER/SERVICE/AGENT principal is the intended attribution

EXTERNAL
= principal outside the local identity taxonomy/system boundary
```

`ActorType` classifies attribution. It is not an IAM role, permission set, organization membership, or authentication-provider taxonomy.

---

# 5. ActorRef

Exact wire:

```yaml
ActorRef:
  actor_type: ActorType
  actor_id: ActorId
```

Both fields are required.

Forbidden fields in shared ActorRef:

```text
display_name
email
roles
permissions
organization
authentication_provider
session/token state
```

`ActorRef` answers “who/what is attributed as the actor?” only.

P2.0 blocker closure:

```text
SC01 ActorRef = CLOSED BY THIS CONTRACT
```

---

# 6. TenantId

## 6.1 Exact wire

```text
JSON string
strict
non-empty
immutable nominal tenant identity
```

Nominal distinction:

```text
TenantId != ActorId
TenantId != ObjectId
TenantId != LogicalId
```

No candidate opaque-ID regex is imported.

---

# 7. TenantScopeType

Exact closed wire values:

```text
GLOBAL
TENANT
```

This enum represents infrastructure-level tenant isolation only.

The following concepts MUST NOT be added as TenantScopeType values:

```text
BRAND
PROJECT
COLLECTION
CATEGORY
STYLE
USER
```

Those are owner/domain semantic scopes inside an isolation domain, not alternatives to tenant isolation.

---

# 8. TenantScope

Exact wire:

```yaml
TenantScope:
  scope_type: TenantScopeType
  tenant_id: TenantId | null
```

Both fields are required in the exact wire shape.

Validation:

```text
scope_type = GLOBAL
=> tenant_id MUST be null

scope_type = TENANT
=> tenant_id MUST be non-null
```

Semantic guard:

```text
GLOBAL
=
not bound to one tenant isolation domain

GLOBAL
!= public
!= anonymous
!= permissionless
!= cross-tenant-readable-by-default
```

Access, promotion, and cross-tenant use remain explicit owner/governance policy.

Forbidden shared fields:

```text
tenant_ids
project_id
brand_id
user_id
knowledge_scope
cross_tenant_use
```

P2.0 blocker closure:

```text
SC02 TenantScope = CLOSED BY THIS CONTRACT
```

---

# 9. Provenance

## 9.1 Purpose

`Provenance` records the immutable source basis of canonical content.

It answers:

```text
which exact canonical objects contributed to this content?
which external non-canonical sources contributed to this content?
```

It does NOT answer:

```text
who created it              -> created_by
when it was created         -> created_at
which command requested it  -> Command/Event correlation/causation contract
which runtime run produced it -> ARSO RunRecord / runtime integration
who approved it             -> Review/Governance records
```

## 9.2 Exact wire

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  external_source_refs: Tuple[str]
```

Both fields are required and each tuple may be empty.

Rules:

```text
source_refs element type
= ExactObjectRef | ObjectRef

LogicalObjectRef
= forbidden in committed provenance

external_source_refs element
= strict non-empty JSON string

ordering
= preserved in wire serialization
```

No universal semantic meaning is assigned to tuple order unless an owner-specific contract explicitly adds one.

## 9.3 Candidate command_ref decision

Candidate field:

```text
command_ref: ObjectRef | None
```

Exact V1 decision:

```text
REJECTED FROM SHARED PROVENANCE
```

Reason:

Global Exact V1 states that Commands and Events have their own identity/correlation metadata and MUST NOT be registered as canonical domain primitives merely because they are persisted. `ObjectRef` is a canonical-object persistent reference. Therefore `command_ref:ObjectRef` would silently alter Command ontology.

Future command causality MUST use the frozen Command/Event identity/correlation design when that inventory is completed.

## 9.4 Candidate run_ref decision

Candidate field:

```text
run_ref: ObjectRef | None
```

Exact V1 decision:

```text
DEFERRED / NOT PRESENT IN SHARED PROVENANCE V1
```

Reason:

`RunRecord` is ARSO-owned. Its production type import and exact ref policy remain a later ARSO integration gate. P2.0A MUST NOT choose that owner’s object class or persistent ref kind.

If a future authoritative RunRecord qualifies as a canonical provenance source, its owner-approved persistent exact ref MAY enter `source_refs` without changing Provenance shape.

## 9.5 External source identifiers

`external_source_refs` remains intentionally opaque in V1:

```text
strict non-empty string
```

This contract does not freeze URI scheme, checksum syntax, DOI/document ontology, storage locator format, or an ExternalSourceRef canonical object.

P2.0 blocker closure:

```text
SC03 Provenance = CLOSED BY THIS CONTRACT
```

---

# 10. ObjectRevision

## 10.1 Exact wire

```text
JSON integer >= 1
```

## 10.2 Frozen semantics

```text
server-assigned ordering metadata only
not ObjectId
not LogicalId
not SchemaVersion
not ConcurrencyVersion
not parentage
not client authority
```

Parentage remains:

```text
parent_refs
```

## 10.3 Non-guarantees

The following are NOT frozen by P2.0A:

```text
revision == previous_revision + 1
contiguous allocation
revision arithmetic to infer lineage
global uniqueness across logical objects
allocation algorithm
CAS behavior
```

Branching is legal. Revision numbers need not encode graph topology.

P2.0 blocker closure:

```text
SC04 ObjectRevision = CLOSED BY THIS CONTRACT
```

---

# 11. JSONValue / Extensions Dependency

Canonical extensions use JSON-native values:

```text
null
bool
integer
finite number
string
list[JSONValue]
map[string, JSONValue]
```

P2.0A consumes this shared JSON-native value concept for `extensions`. It is not a new canonical primitive and receives no registry entry.

Namespaced extension policy from the global Exact Contract remains unchanged.

---

# 12. UTC Canonical Timestamp Rule

Global Exact V1 requires ISO-8601 UTC timestamps.

P2.0A runtime normalization for canonical-shell timestamps:

```text
naive datetime
-> reject

aware datetime
-> normalize to UTC

runtime canonical value
-> UTC-aware datetime

serialization
-> ISO-8601 representation of the same UTC instant
```

This section applies to shared canonical-shell fields such as `created_at`.

It does NOT freeze the full time inventory for Commands, Events, Runs, or operational state.

---

# 13. CanonicalObject Structural Base

`CanonicalObject` is a structural base, not a registered canonical primitive.

Exact common wire:

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

All fields are required in the canonical wire shape.

The global Exact Contract remains authority for the semantic role of these fields; this companion contract supplies exact shared support-type internals.

---

# 14. CanonicalRevision Structural Base

`CanonicalRevision` extends CanonicalObject with:

```yaml
logical_id: LogicalId
revision: ObjectRevision
parent_refs: Tuple[ExactObjectRef]
```

All fields are required.

`parent_refs` may be empty only where owner/store semantics permit an initial/root revision.

Frozen rules:

```text
revision arithmetic MUST NOT infer parentage
parentage = parent_refs
ExactObjectRef remains the persistent ref for CANONICAL_REVISION objects
```

---

# 15. ImmutableFact Structural Base

`ImmutableFact` adds no shared wire field beyond CanonicalObject.

A concrete ImmutableFact’s object type, owner, state domain, historical role, eligibility flags, and persistent ObjectRef policy are supplied by that object’s owner/registry contract.

The structural base itself receives no Object Registry entry.

---

# 16. Registry Exclusion

The following MUST NOT be entered into Object Registry as independent domain objects:

```text
ActorId
ActorType
ActorRef
TenantId
TenantScopeType
TenantScope
Provenance
ObjectRevision
CanonicalObject
CanonicalRevision
ImmutableFact structural base
```

Rationale:

```text
support/nested/structural type
!= canonical domain primitive
```

This preserves `OneCanonicalObject => OnePrimitiveOwner` without inventing primitive owners for implementation support types.

---

# 17. CanonicalPayload Boundary

P2.0A freezes field types and structural bases. It does NOT define one universal semantic CanonicalPayload selector for every owner.

Inherited global N09 rules remain:

```text
content_hash itself excluded
transport-only metadata excluded
mutable operational fields excluded
created_at/created_by excluded from semantic revision hashes unless explicit owner identity policy says otherwise
```

B01 owner contract already freezes its own payload selection, including exclusion of:

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

P2.0A validates the field contracts but does not override B01’s owner-specific payload decision and does not decide B02+ payload policies.

---

# 18. P0 / P1 Compatibility

P2.0A MUST NOT change the frozen contracts for:

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

Explicitly forbidden compatibility backdoors:

```text
adding candidate opaque-ID regex to ObjectId/LogicalId
closing ActorType solely because candidate used StrEnum
encoding Command/Event as canonical ObjectRef targets
choosing ARSO RunRecord object class/ref kind
registering shared support types as domain primitives
```

---

# 19. Out of Scope / Deferred

This contract does not freeze:

```text
ObjectId lexical grammar
LogicalId lexical grammar
SchemaVersion lexical grammar
ObjectType namespace grammar
ConcurrencyVersion
OperationalControlState full schema
Command/Event complete identity/correlation inventory
CommandRef/EventRef
ARSO RunRecord exact production integration
IAM/authentication/permission models
ExternalSourceRef URI/digest ontology
store revision allocator
store uniqueness rules
CAS/resolver implementation
B01/B02 production Pydantic models
```

Those remain governed by their own future stages.

---

# 20. Recovery Decision Register

## 20.1 Strongly recovered / normalized

```text
created_by role -> ActorRef
ActorRef two-part typed attribution
TenantScope discriminator structure
GLOBAL/TENANT isolation distinction
revision as server ordering metadata
parentage = parent_refs
canonical metadata shell field presence
ISO-8601 UTC requirement
```

## 20.2 NEW_FREEZE_DECISION surface

```text
ActorId strict non-empty open lexical contract
ActorType open vocabulary instead of closed candidate enum
standard ActorType minimum meanings
TenantId strict non-empty open lexical contract
TenantScope GLOBAL semantic guard
Provenance exact two-field shape
Provenance canonical-ref-only source_refs
external_source_refs strict non-empty strings
ObjectRevision lower bound >=1
CanonicalObject/CanonicalRevision exact requiredness
support-type registry exclusion
```

## 20.3 REJECTED candidate surface

```text
common candidate opaque-ID regex for ActorId/TenantId
closed ActorType exhaustiveness
Provenance.command_ref:ObjectRef
support-type registry entries
```

## 20.4 DEFERRED candidate surface

```text
Provenance.run_ref:ObjectRef
```

---

# 21. P2.0A Freeze Conditions

This contract may move from `FREEZE CANDIDATE` toward a frozen checkpoint only when:

```text
SC01-SC04 exact support contracts covered
field-decision ledger complete
cross-spec audit PASS
no candidate-only field silently promoted
no P0/P1 semantic drift
no Command/Event/Run owner leakage
no production core/B01 implementation added
normative checksum registered and passing
independent P2.0A Freeze Review PASS
P2.0 B01 re-review PASS
user explicitly approves the combined P2.0 Freeze checkpoint
```

Current status:

```text
DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT: FREEZE CANDIDATE
P2.0A: RECOVERY IMPLEMENTATION IN PROGRESS
P2.0: B01 OWNER-FIELD RECOVERY PASS / REMEDIATION IN PROGRESS
P2: NOT AUTHORIZED
Exact V1 global: FREEZE CANDIDATE
```
