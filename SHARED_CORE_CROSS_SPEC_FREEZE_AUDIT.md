# Shared Canonical Shell Cross-Spec Freeze Audit

审计日期：2026-09-05  
阶段：P2.0A｜Shared Canonical Shell Support Contract Recovery  
审计对象：`DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT V1.0-FC1`  
当前结论：`PASS / FREEZE CANDIDATE / AWAITING CHECKSUM + INDEPENDENT REVIEW`

## 1. 审计问题

本审计独立回答：

1. shared-core companion contract 是否只补齐 global canonical shell 的 support-type exactness，而没有覆盖 P0/P1 frozen semantics？
2. `ActorRef / TenantScope / Provenance / ObjectRevision` 是否足以解除 P2.0-SC01–SC04？
3. 是否出现 candidate-only silent promotion、closed-enum over-freeze、跨 owner 版本策略污染或 Command/Event/Run canonical-ref 污染？
4. P2 若消费本合同与 B01 owner contract，是否仍需猜 shared shell 的字段/类型？

## 2. Authority relation audit

Proposed scoped authority：

```text
1A DI-V5-EXACT-CONTRACT
1B DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT
1C DI-B01-EXACT-CONTRACT
2+ existing chain
```

Interpretation：

- 1A remains global/cross-domain authority.
- 1B only owns shared support/nested type internals and structural bases.
- 1C owns B01 business/design field-level schemas and consumes 1B.
- 1B has no right to define B01/B02/ARSO primitive fields.

Verdict：`PASS`。

---

# 3. ActorRef audit｜SC01

## 3.1 Source evidence

Authority chain directly requires canonical attribution via：

```text
created_by
```

but does not provide an exact nested wire schema.

Candidate proposes：

```yaml
ActorRef:
  actor_type: ActorType
  actor_id: ActorId
```

with ActorType candidate enum：

```text
USER
SERVICE
AGENT
SYSTEM
EXTERNAL
```

## 3.2 Recovery evaluation

P2.0A preserves the two-field typed attribution structure but does NOT promote candidate exhaustiveness.

Exact decision：

```text
ActorId   = nominal strict non-empty string
ActorType = nominal strict non-empty open vocabulary
ActorRef  = actor_type + actor_id, both required
```

Five candidate codes are frozen only as standard recognized minimum vocabulary with explicit meanings.

## 3.3 Over-freeze check

Potential error：

```text
candidate StrEnum
=> exhaustive global actor taxonomy
```

P2.0A explicitly rejects that inference.

Potential error：import candidate opaque-ID regex into ActorId.

P2.0A explicitly rejects it to preserve P0's earlier lexical restraint.

Verdict：

```text
SC01 = CLOSED
candidate silent promotion = NO
closed-enum over-freeze = NO
P0 identity lexical drift = NO
```

---

# 4. TenantScope audit｜SC02

## 4.1 Source evidence

Global/cross-spec canonical metadata requires：

```text
tenant_scope
```

ARSO engineering retains tenant isolation and distinguishes tenant-specific evidence/artifacts/preferences from global knowledge.

Candidate proposes：

```yaml
TenantScope:
  scope_type: GLOBAL | TENANT
  tenant_id: TenantId | null
```

## 4.2 Scope-separation test

A key risk is conflating infrastructure isolation with semantic/domain scope.

P2.0A freezes：

```text
TenantScopeType = GLOBAL | TENANT
```

and explicitly rejects：

```text
BRAND
PROJECT
COLLECTION
CATEGORY
STYLE
USER
```

as tenant-isolation enum values.

Those may exist in B08/domain semantic scopes but do not replace tenant isolation.

## 4.3 GLOBAL semantics

P2.0A explicitly defines：

```text
GLOBAL = not bound to one tenant isolation domain
GLOBAL != public / anonymous / permissionless / cross-tenant-readable-by-default
```

Thus the shared shell does not become an authorization policy.

## 4.4 Discriminator invariant

```text
GLOBAL -> tenant_id null
TENANT -> tenant_id non-null
```

This is sufficient to prevent ambiguous isolation state.

Verdict：

```text
SC02 = CLOSED
semantic-scope pollution = NO
authorization-policy pollution = NO
```

---

# 5. Provenance audit｜SC03

## 5.1 Source evidence

`provenance` is globally required as stable canonical metadata where applicable, but authority documents do not freeze its internal fields.

Candidate proposes：

```text
source_refs
command_ref:ObjectRef
run_ref:ObjectRef
external_source_refs
```

## 5.2 Canonical-source ref decision

P2.0A freezes：

```text
source_refs: Tuple[CanonicalRef]
```

where：

```text
CanonicalRef = ExactObjectRef | ObjectRef
LogicalObjectRef forbidden at committed boundary
```

This is compatible with P1 exact reference semantics and introduces no implicit latest.

## 5.3 Command pollution test

Global Exact Contract explicitly states Commands and Events have their own identity/correlation metadata and MUST NOT become canonical domain primitives merely because persisted.

Therefore candidate：

```text
command_ref:ObjectRef
```

would imply a canonical persistent ObjectRef target without a frozen command canonical-object contract.

P2.0A verdict：`REJECTED`。

This is stricter than candidate and consistent with global semantics.

## 5.4 RunRecord owner test

`RunRecord` is ARSO-owned and authoritative production integration remains later.

P2.0A refuses to select：

```text
RunRecord object class
RunRecord persistent ref kind
run_ref:ObjectRef
```

Candidate `run_ref` is therefore `DEFERRED`.

If ARSO later freezes RunRecord as an eligible canonical provenance source, its exact persistent ref can be included in `source_refs` without changing the shared Provenance shape.

## 5.5 External source decision

`external_source_refs: Tuple[str]` remains opaque, strict and non-empty per element. No URI/digest ontology is fabricated.

Verdict：

```text
SC03 = CLOSED
Command canonical-ref pollution = NO
ARSO owner override = NO
LogicalObjectRef leakage = NO
```

---

# 6. ObjectRevision audit｜SC04

## 6.1 Frozen global semantics

Global Exact Contract explicitly distinguishes：

```text
ObjectId != LogicalId != Revision != SchemaVersion
revision = server-assigned ordering metadata only
parentage = parent_refs
```

## 6.2 P2.0A exact wire

```text
JSON integer >= 1
```

This is an explicit normalization decision. Candidate uses the same lower-bound shape, but the decision is justified independently by the need for a positive server ordering sequence rather than by candidate authority.

## 6.3 Lineage/concurrency firewall

P2.0A explicitly rejects inference：

```text
revision + 1 = child
revision = concurrency token
revision arithmetic = lineage
```

It does not freeze allocator/contiguity/CAS semantics.

Verdict：

```text
SC04 = CLOSED
lineage conflation = NO
concurrency conflation = NO
```

---

# 7. Structural CanonicalObject audit

Global Exact Contract §6 requires, where applicable：

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

P2.0A maps these exact roles into：

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

No new canonical object identity is created for the base itself.

Verdict：`PASS`。

---

# 8. CanonicalRevision audit

Global Exact Contract requires versioned revisions to add：

```text
logical_id
revision
parent_refs
```

P2.0A maps：

```yaml
logical_id: LogicalId
revision: ObjectRevision
parent_refs: Tuple[ExactObjectRef]
```

ExactObjectRef matches P1 persistent-reference semantics for CANONICAL_REVISION targets.

`parent_refs` may be empty only when owner/store semantics allow an initial/root revision; P2.0A does not invent branch topology from revision arithmetic.

Verdict：`PASS`。

---

# 9. Registry / primitive ownership audit

Potential error：register structural/nested support types as canonical primitives.

P2.0A explicitly excludes all support types and structural bases from Object Registry.

```text
support/nested/structural type
!= canonical domain primitive
```

No `primitive_owner` is invented for ActorRef/TenantScope/Provenance/ObjectRevision.

Verdict：`PASS`。

---

# 10. P0/P1 compatibility audit

P2.0A changes none of the frozen contracts for：

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
registry foundation
```

It also does not import candidate regex constraints into existing P0 nominal IDs.

Verdict：`PASS / NO REOPEN OF P0 OR P1`。

---

# 11. CanonicalPayload audit

P2.0A freezes field types and structural bases only.

It does not reintroduce a generic payload extractor and does not override B01's owner-specific payload policy.

Therefore P1's deliberate separation remains：

```text
owner selects CanonicalPayload
P1 canonicalizes/hashes it
```

Verdict：`PASS`。

---

# 12. Candidate baseline audit

Candidate evidence is used only to identify plausible structures and drift risks.

Explicit candidate outcomes：

```text
ActorRef 2-field structure         NORMALIZED_RECOVERY
ActorType closed enum              REJECTED as exhaustive
ActorId/TenantId opaque regex      REJECTED
TenantScope 2-field discriminator  NORMALIZED_RECOVERY
Provenance source_refs             NORMALIZED_RECOVERY
Provenance external_source_refs    NORMALIZED_RECOVERY
Provenance command_ref:ObjectRef   REJECTED
Provenance run_ref:ObjectRef       DEFERRED
ObjectRevision int>=1              NORMALIZED independently
```

Verdict：`NO SILENT CANDIDATE PROMOTION`。

---

# 13. P2 implementability audit

Before P2.0A, a complete B01 canonical model could not be written without guessing：

```text
ActorRef internals
TenantScope internals
Provenance internals
ObjectRevision wire
```

With the shared-core candidate contract, B01's canonical shell resolves to exact support types and invariants.

No B01 business field is redefined by P2.0A.

Preliminary result：

```text
SC01-SC04 contract-level closure = PASS
B01 shared-shell consumption = IMPLEMENTABLE AT CONTRACT LEVEL
```

This remains a preliminary conclusion until checksum registration, automated gates, and independent review.

---

# 14. Gap / Conflict register

## SPEC_CONFLICT

```text
0 discovered
```

## Blocking shared-core field SPEC_GAP

```text
0 in the P2.0A recovery candidate
```

## Explicitly deferred non-P2 blockers

```text
ObjectId/LogicalId/SchemaVersion/ObjectType lexical grammar
ConcurrencyVersion
OperationalControlState full schema
Command/Event inventory and identity/correlation refs
ARSO RunRecord integration
ExternalSourceRef ontology
revision allocator/CAS/store semantics
B02+ owner schemas
```

These do not prevent B01 canonical shell construction under the approved P2.0A scope.

---

# 15. Preliminary recommendation

Subject to checksum registration, automated verification and independent Freeze Review：

```text
P2.0A RECOVERY CONTRACT: PASS
SC01-SC04: CLOSED IN CANDIDATE
SHARED-CORE SPEC_CONFLICT: 0
BLOCKING SHARED-CORE FIELD SPEC_GAP: 0
P0/P1 DRIFT: 0
CANDIDATE SILENT PROMOTION: 0
P2.0A: READY FOR CHECKSUM + INDEPENDENT REVIEW
```

This audit does not itself freeze P2.0A, does not merge PR #5, and does not authorize P2.
