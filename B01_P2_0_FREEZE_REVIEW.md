# P2.0｜B01 Owner Contract Recovery 独立 Freeze Review

初次 Review：2026-09-04  
Remediation Re-review：2026-09-05  
Review 对象：P2.0 B01 owner contract + stacked P2.0A shared canonical-shell remediation  
原始基线：`main@7102c7e264784bd18bf0b423c2f4b12065a17ab9`  
Remediation content head：`7df4c0f61191ed5929d41019b5cf2fe6b200cc0a`  
当前结论：`PASS / READY FOR USER FREEZE DECISION / NOT FROZEN`

> 历史说明：2026-09-04 初次独立 Review 判定 B01 owner fields 本身已完整，但因 shared canonical shell 的 `ActorRef / TenantScope / Provenance / ObjectRevision` exact contract 缺失而阻断 P2.0 Freeze。P2.0A 随后被授权并生成 scoped shared-core contract。本文保留原 blocker IDs，并记录其 closure；不抹除原始发现。

---

# 1. B01 owner-layer result

`DI-V5-EXACT-CONTRACT` N11 要求 exactly seven B01 canonical objects：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

`DI-B01-EXACT-CONTRACT` 覆盖：

```text
7 / 7
```

Field ledger 已明确：

```text
wire type
cardinality
requiredness
semantic owner
reference kind
recovery decision
CanonicalPayload policy
```

B01 result：

```text
B01 owner-field SPEC_GAP = 0
B01 SPEC_CONFLICT = 0
```

Verdict：`PASS`。

---

# 2. B01 architecture-boundary recheck

## 2.1 StyleBrief boundary

```text
StyleBrief != prompt
StyleBrief != ReferenceTaskSpec
```

ARSO task semantics remain referenced rather than copied.

Verdict：`PASS`。

## 2.2 DesignDecision / DesignSpec boundary

```text
DesignDecision = strategy/allocation
DesignDecision != DesignSpec
DesignSpec = AuthoritativeStructuredIntent
DesignSpec != Prompt
DesignSpec != GenerationPackage
DesignSpec != ordinary SystemArtifact
```

Verdict：`PASS`。

## 2.3 Reference separation

```text
ReferenceAsset != ReferenceIntentBinding != CompiledReferenceBinding
```

ReferenceIntentBinding contains semantic intent only; B03 compiled/executor fields remain excluded.

Verdict：`PASS`。

## 2.4 Runtime/mutable-state leakage

DesignRoute contains no mutable selected/status field.  
DesignSpec contains no prompt/model/executor/runtime status fields.  
Committed B01 refs contain no `LogicalObjectRef`.

Verdict：`PASS`。

---

# 3. Original blocker history

The 2026-09-04 review found four Important shared-core gaps：

```text
P2.0-SC01 ActorRef exact wire contract missing
P2.0-SC02 TenantScope exact wire contract missing
P2.0-SC03 Provenance exact wire contract missing
P2.0-SC04 ObjectRevision exact wire contract missing
```

At that time：

```text
B01 owner fields complete
+
shared canonical shell incomplete
=
P2 full canonical models still required guessing
```

Therefore the original `BLOCKED` decision was correct and remains part of audit history.

---

# 4. P2.0A remediation authority

P2.0A adds the scoped candidate：

```text
specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md
```

Authority relation：

```text
1A DI-V5-EXACT-CONTRACT
1B DI-SHARED-CANONICAL-SHELL-EXACT-CONTRACT
1C DI-B01-EXACT-CONTRACT
```

Rules：

```text
1B MUST NOT override 1A
1C consumes 1B and MUST NOT redefine shared support internals
shared support types are not independent canonical domain primitives
```

Verdict：`PASS`。

---

# 5. SC01 remediation｜ActorRef

P2.0A exact contract：

```text
ActorId = strict non-empty nominal string
ActorType = strict non-empty open typed vocabulary
standard codes = USER/SERVICE/AGENT/SYSTEM/EXTERNAL
ActorRef = actor_type + actor_id
```

Candidate-specific over-freezes are explicitly rejected：

```text
candidate ActorId opaque regex -> not imported
candidate ActorType closed exhaustiveness -> not imported
```

B01 `created_by: ActorRef` can now be implemented without copying candidate internals.

Status：

```text
P2.0-SC01 = CLOSED
```

---

# 6. SC02 remediation｜TenantScope

P2.0A exact contract：

```yaml
TenantScope:
  scope_type: GLOBAL | TENANT
  tenant_id: TenantId | null
```

Invariant：

```text
GLOBAL -> tenant_id null
TENANT -> tenant_id non-null
```

And：

```text
GLOBAL != public / anonymous / permissionless
```

Domain scopes such as Brand/Project/Collection are not mixed into tenant isolation.

Status：

```text
P2.0-SC02 = CLOSED
```

---

# 7. SC03 remediation｜Provenance

P2.0A exact contract：

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  external_source_refs: Tuple[str]
```

Candidate-specific fields：

```text
command_ref:ObjectRef -> REJECTED
run_ref:ObjectRef -> DEFERRED
```

This avoids turning persisted Commands into canonical domain primitives and avoids choosing ARSO RunRecord ref policy before its owner integration.

B01 `provenance` now has an exact support schema without ARSO/Command shadowing.

Status：

```text
P2.0-SC03 = CLOSED
```

---

# 8. SC04 remediation｜ObjectRevision

P2.0A exact wire：

```text
JSON integer >= 1
```

Semantics：

```text
server-assigned ordering metadata only
not identity
not SchemaVersion
not ConcurrencyVersion
not parentage
parentage = parent_refs
```

No contiguous allocation or revision-arithmetic lineage rule is invented.

Status：

```text
P2.0-SC04 = CLOSED
```

---

# 9. Shared structural shell closure

P2.0A additionally freezes the exact shared structural mapping：

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

CanonicalRevision:
  + logical_id: LogicalId
  + revision: ObjectRevision
  + parent_refs: Tuple[ExactObjectRef]
```

`ImmutableFact` adds no extra common wire field beyond CanonicalObject.

Support types/bases receive no Object Registry entries.

Therefore the six B01 canonical revisions and one B01 immutable fact have a complete shared shell at contract level.

Verdict：`PASS`。

---

# 10. CanonicalPayload closure

P1 continues to provide hashing mechanics only.  
B01 owner contract continues to provide B01-specific payload selection.  
P2.0A only defines exact support-field types and does not override the B01 payload policy.

```text
owner selects CanonicalPayload
-> P1 RFC8785 canonicalization
-> SHA-256 ContentHash
```

Verdict：`PASS`。

---

# 11. Automated remediation evidence

Exact remediation content head：

```text
7df4c0f61191ed5929d41019b5cf2fe6b200cc0a
```

Fresh workflow evidence：

```text
P1 contract verification
run 33898485666
SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33898485725
SUCCESS
```

Scoped gate proves：

```text
9 / 9 normative checksums
registered shared-core digest equality
B01 7 / 7 surface
shared-core required surface
no production B01 Python leakage
no production core Python leakage
P0/P1 regression
candidate baseline regression
compile
placeholder / whitespace / authority-scope gates
```

Verdict：`PASS`。

---

# 12. P2 implementability recheck

Question：

> If P2 begins after an explicit Freeze decision, must the implementer still guess any B01 owner field or shared canonical-shell support type?

Result：

```text
B01 business/design fields -> exact owner contract available
B01 object classifications -> fixed
B01 registry policy -> fixed
B01 CanonicalPayload policy -> fixed
ActorRef -> exact shared contract available
TenantScope -> exact shared contract available
Provenance -> exact shared contract available
ObjectRevision -> exact shared contract available
CanonicalObject/Revision structural shell -> exact shared contract available
```

No `di_contracts_v1` support structure must be promoted silently to implement the seven B01 canonical models.

Verdict：

```text
P2 CONTRACT-LEVEL IMPLEMENTABILITY = PASS
```

---

# 13. Findings summary after remediation

```text
Critical:  0
Important: 0
Minor:     0
```

```text
B01 owner-field SPEC_GAP = 0
shared-core blocking SPEC_GAP = 0
SPEC_CONFLICT = 0
SC01-SC04 = CLOSED
```

Deferred global Exact V1 blockers outside P2 remain, including B02, ARSO imports, full Command/Event/Protocol, resolver/CAS/snapshot gates and remaining CS/AC release surface. They do not require B01 schema fabrication.

---

# 14. Re-review Decision

```text
P2.0 B01 OWNER-FIELD RECOVERY: PASS
P2.0A SHARED-CANONICAL-SHELL REMEDIATION: PASS
P2.0 AUTOMATED VERIFICATION: PASS
P2.0 INDEPENDENT RE-REVIEW: PASS
P2.0-SC01–SC04: CLOSED
P2.0: READY FOR USER FREEZE DECISION
```

Governance remains：

```text
P2.0 != FROZEN
P2 = NOT AUTHORIZED
```

Required sequence after explicit user approval：

```text
approve P2.0 Freeze
-> merge PR #5 into p2-0-b01-contract-recovery
-> run fresh PR #4 verification on the exact combined head
-> record P2.0 Freeze decision
-> merge PR #4 to main with expected-head protection
-> verify main checkpoint
-> only then authorize P2 Full B01 Exact Schemas
```
