# P2.0A｜Shared Canonical Shell Support Contract Recovery 独立 Freeze Review

Review 日期：2026-09-05  
Review 对象：PR #5 `p2-0a-shared-core-contract-recovery`  
Base：`p2-0-b01-contract-recovery@27e4607098daf543bd12aec9e0fdd7bf43e699d4`  
Review head：`7df4c0f61191ed5929d41019b5cf2fe6b200cc0a`  
Review 模式：独立于 source recovery / field-ledger / preliminary audit 的第二遍 criteria-based review  
结论：`PASS / READY FOR P2.0 RE-REVIEW / NOT FROZEN`

---

# 1. Independent criteria

本 Review 不以“candidate 能运行”为通过标准，而重新检查：

1. `ActorRef` 是否因 candidate enum/regex 被静默过度冻结；
2. `TenantScope` 是否把 tenant isolation 与 Brand/Project/User 等 semantic scope 混为一体；
3. `Provenance` 是否把 Command/Event/RunRecord 偷偷变成 canonical `ObjectRef` target；
4. `ObjectRevision` 是否与 identity/schema/concurrency/lineage 混淆；
5. structural bases 是否被错误注册为 canonical domain primitives；
6. P2.0A 是否重新打开 P0/P1 frozen semantics；
7. 最终 CI 是否对应 exact review head；
8. P2 是否能在消费 shared shell 时避免复制 `di_contracts_v1` support structures。

---

# 2. Automated evidence

Exact review head：

```text
7df4c0f61191ed5929d41019b5cf2fe6b200cc0a
```

Fresh GitHub Actions：

```text
P1 contract verification
run 33898485666
SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33898485725
SUCCESS
```

P2.0/P2.0A scoped gate passed all of：

```text
9 / 9 normative source checksums
registered shared-core digest equality
B01 7 / 7 canonical surface
shared-core required section coverage
no production B01 Python leakage
no production core Python leakage
P0/P1 regression
candidate baseline regression through P0/P1 regression step
compile frozen production package
placeholder scan
non-Markdown whitespace check
Markdown whitespace policy
authority-source scope gate
```

Verdict：`AUTOMATED VERIFICATION PASS`。

---

# 3. SC01｜ActorRef review

## 3.1 Candidate promotion test

Candidate proposes：

```text
ActorId opaque regex
ActorType closed USER/SERVICE/AGENT/SYSTEM/EXTERNAL enum
ActorRef(actor_type, actor_id)
```

P2.0A adopts only the two-field attribution structure and rejects the two candidate-specific over-freezes：

```text
candidate ActorId regex -> NOT ADOPTED
closed ActorType exhaustiveness -> NOT ADOPTED
```

Exact P2.0A result：

```text
ActorId = strict non-empty nominal string
ActorType = strict non-empty open typed vocabulary
standard recognized codes = USER/SERVICE/AGENT/SYSTEM/EXTERNAL
ActorRef = actor_type + actor_id
```

Standard-code meanings are explicit, so open vocabulary does not make the known codes ambiguous.

Verdict：

```text
SC01 CLOSED
candidate silent promotion = 0
P0 lexical backdoor change = 0
```

---

# 4. SC02｜TenantScope review

Exact P2.0A result：

```text
TenantId = strict non-empty nominal string
TenantScopeType = GLOBAL | TENANT
TenantScope = scope_type + tenant_id
```

Invariant：

```text
GLOBAL -> tenant_id null
TENANT -> tenant_id non-null
```

Domain semantic scopes are explicitly excluded from TenantScopeType.

The contract also prevents an authorization error：

```text
GLOBAL != public
GLOBAL != anonymous
GLOBAL != permissionless
GLOBAL != cross-tenant-readable-by-default
```

Verdict：

```text
SC02 CLOSED
tenant/domain scope conflation = 0
authorization-policy conflation = 0
```

---

# 5. SC03｜Provenance review

Exact P2.0A result：

```yaml
Provenance:
  source_refs: Tuple[CanonicalRef]
  external_source_refs: Tuple[str]
```

Both fields required, may be empty; committed `LogicalObjectRef` is forbidden.

Candidate fields reviewed independently：

```text
command_ref:ObjectRef -> REJECTED
run_ref:ObjectRef -> DEFERRED / ABSENT IN V1 SHARED SHAPE
```

The command decision is required by the global rule that persisted Commands/Events are not thereby canonical domain primitives.

The run decision preserves ARSO primitive ownership and leaves RunRecord exact integration to its scheduled gate.

No command/event/run lifecycle state appears in Provenance.

Verdict：

```text
SC03 CLOSED
Command/Event canonical-ref pollution = 0
ARSO RunRecord owner override = 0
LogicalObjectRef leakage = 0
```

---

# 6. SC04｜ObjectRevision review

Exact wire：

```text
JSON integer >= 1
```

Frozen semantics remain：

```text
server-assigned ordering metadata only
!= ObjectId
!= LogicalId
!= SchemaVersion
!= ConcurrencyVersion
!= parentage
```

The contract explicitly rejects：

```text
revision + 1 => child
revision arithmetic => lineage
contiguous allocation requirement
CAS semantics inside ObjectRevision
```

Parentage remains `parent_refs`.

Verdict：

```text
SC04 CLOSED
identity conflation = 0
lineage conflation = 0
concurrency conflation = 0
```

---

# 7. Structural-base review

P2.0A freezes exact support mapping for：

```text
CanonicalObject
CanonicalRevision
ImmutableFact structural base
UTC canonical timestamp normalization
```

It does NOT register any of these bases/support types as canonical domain primitives.

Therefore：

```text
support/nested/structural type
!= independent canonical object
```

and `OneCanonicalObject => OnePrimitiveOwner` remains intact.

Verdict：`PASS`。

---

# 8. P0/P1 compatibility review

PR #5 does not modify production contracts under：

```text
src/design_intelligence/contracts/core/
src/design_intelligence/contracts/b01/
```

P2.0A does not alter the frozen semantics of：

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

The open lexical choice for ActorId/TenantId avoids indirectly imposing the candidate opaque-ID regex rejected during P0.

Verdict：`PASS / P0-P1 NOT REOPENED`。

---

# 9. CanonicalPayload review

P2.0A defines support-field types and structural bases, not a universal owner hash selector.

P1 separation remains：

```text
owner contract selects CanonicalPayload
P1 canonicalizes + hashes it
```

B01 keeps its explicit owner payload policy; P2.0A does not override it.

Verdict：`PASS`。

---

# 10. External provenance limitation

`external_source_refs` intentionally remains an opaque non-empty string rather than freezing URL/digest/document ontology.

This means P2.0A does not itself prove immutability of an external resource's bytes. That concern belongs to a future ExternalSourceRef/content-digest contract if required by an owner.

For P2/B01 implementability this is non-blocking because：

```text
external_source_refs wire is exact
B01 provenance is immutable metadata
B01 semantic payload policy already excludes provenance
no B01 field requires an ExternalSourceRef canonical primitive
```

Classification：`DEFERRED SCOPE / NON-BLOCKING`, not a P2.0A defect.

---

# 11. Findings summary

```text
Critical:  0
Important: 0
Minor:     0
```

Shared-core contract result：

```text
SC01 ActorRef       CLOSED
SC02 TenantScope    CLOSED
SC03 Provenance     CLOSED
SC04 ObjectRevision CLOSED
SPEC_CONFLICT       0
blocking shared-core field SPEC_GAP 0
```

No candidate-only support structure was silently promoted as normative authority.

---

# 12. P2.0A decision

```text
P2.0A SOURCE RECOVERY: PASS
P2.0A FIELD DECISION LEDGER: PASS
P2.0A CROSS-SPEC AUDIT: PASS
P2.0A AUTOMATED VERIFICATION: PASS
P2.0A INDEPENDENT FREEZE REVIEW: PASS
SC01-SC04: CLOSED
```

Governance result：

```text
P2.0A = READY FOR P2.0 RE-REVIEW
P2.0A != FROZEN
P2 = NOT AUTHORIZED
```

P2.0A may become part of a frozen checkpoint only after the combined P2.0 re-review passes and the user explicitly approves P2.0 Freeze.
