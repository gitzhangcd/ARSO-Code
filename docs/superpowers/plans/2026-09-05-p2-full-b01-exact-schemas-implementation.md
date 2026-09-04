# P2 Full B01 Exact Schemas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the frozen P2 B01 Exact V1 Pydantic contract for the seven B01 canonical objects, the already-frozen shared canonical-shell support types required by them, B01 owner-specific canonical payload hashing, and the exact B01 registry surface needed to close AC-01.

**Architecture:** Preserve P0/P1 as immutable foundations. Add shared support/nested types and structural canonical bases under `contracts/core`, then build B01-owned nested values and seven domain models under `contracts/b01`. Owner-specific semantic hashing stays in B01 rather than becoming a generic blacklist extractor. Registry metadata is a derived manifest over the seven frozen B01 entries; no B02+, ARSO, Command/Event/Protocol, resolver/store/CAS, snapshot, UI, executor, or optimizer behavior is introduced.

**Tech Stack:** Python 3.12+, Pydantic 2.12+, RFC 8785 helper already frozen in P1, pytest 8+, GitHub Actions PR verification.

**Spec:** `specs/00-CODE-FREEZE/DI_B01_Exact_V1_Owner_Contract.md`, consuming `specs/00-CODE-FREEZE/DI_Shared_Canonical_Shell_Exact_V1_Contract.md` under `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`.

## Global Constraints

- Work only on branch `p2-b01-exact-schemas`; do not modify `main` during implementation.
- `di_contracts_v1/` is read-only candidate evidence and MUST NOT be edited or copied wholesale.
- P0/P1 contracts remain frozen: `ObjectId`, `LogicalId`, `SchemaVersion`, `ObjectType`, `CanonicalObjectClass`, `DIModel`, `FrozenDIModel`, `ContentHash`, exact refs, RFC8785 hashing, and registry foundation semantics.
- `ActorType` is a strict non-empty open typed vocabulary recognizing at least `USER`, `SERVICE`, `AGENT`, `SYSTEM`, `EXTERNAL`; it is not a closed enum.
- `TenantScopeType` is exactly `GLOBAL | TENANT`; `GLOBAL` does not imply public or permissionless access.
- `Provenance.source_refs` accepts only persistent `CanonicalRef = ExactObjectRef | ObjectRef`; `LogicalObjectRef`, shared `command_ref`, and shared `run_ref` are absent.
- `ObjectRevision` is a strict integer `>= 1` and is ordering metadata only; parentage is `parent_refs`.
- All canonical `created_at` values reject naive datetimes and normalize aware datetimes to UTC.
- Shared support/nested/structural types receive no registry entries.
- All B01 owner fields in the exact wire shape are required; nullable fields may be `None`; tuple fields may be empty except the explicitly non-empty owner rules below.
- `ReferenceIntentBinding.intent_codes`, `DesignRoute.mechanisms`, and `DesignSpec.assignments` MUST be non-empty.
- B01 committed references never accept `LogicalObjectRef`.
- B01 CanonicalPayload includes `schema_version`, `object_type`, all B01 owner semantic/binding fields, and `extensions`; it excludes `id`, `logical_id`, `revision`, `parent_refs`, `created_at`, `created_by`, `tenant_scope`, `provenance`, and `content_hash`.
- Exactly seven B01 registry entries are added, all with `primitive_owner=DI_B01`, `capability_owners=(DI_B01,)`, `state_domain=TASK`, `canonical=true`, `historical_ssot=true`, and the exact eligibility matrix in the owner contract.
- If an implementation decision requires an unfrozen field/type/behavior, stop that affected path as `SPEC_GAP`; if frozen requirements conflict, stop it as `SPEC_CONFLICT`.

---

### Task 1: Shared canonical-shell RED tests

**Files:**
- Create: `tests/unit/test_p2_shared_canonical_shell.py`

**Interfaces:**
- Consumes: frozen P0/P1 nominal types, refs, `FrozenDIModel`.
- Produces test contract for: `ActorId`, `ActorType`, `ActorRef`, `TenantId`, `TenantScopeType`, `TenantScope`, `Provenance`, `ObjectRevision`, `CanonicalObject`, `CanonicalRevision`, `ImmutableFact`.

- [ ] **Step 1: Write the failing tests**

Cover exact strict/non-empty nominal values, open `ActorType`, closed tenant scope values, GLOBAL/TENANT coupling, provenance exact-reference-only shape, ObjectRevision lower bound, structural field sets, and timezone normalization:

```python
from datetime import datetime, timedelta, timezone
import pytest
from pydantic import ValidationError

from design_intelligence.contracts.core import (
    ActorId, ActorRef, ActorType, CanonicalObject, CanonicalRevision,
    ImmutableFact, ObjectRevision, Provenance, TenantId, TenantScope,
    TenantScopeType,
)


def test_actor_type_is_open_but_non_empty() -> None:
    assert ActorType("USER").root == "USER"
    assert ActorType("CUSTOM_INTEGRATION").root == "CUSTOM_INTEGRATION"
    with pytest.raises(ValidationError):
        ActorType("")


def test_tenant_scope_enforces_discriminator() -> None:
    assert TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id=None).tenant_id is None
    with pytest.raises(ValidationError):
        TenantScope(scope_type=TenantScopeType.GLOBAL, tenant_id=TenantId("tenant-a"))
    with pytest.raises(ValidationError):
        TenantScope(scope_type=TenantScopeType.TENANT, tenant_id=None)


def test_created_at_rejects_naive_and_normalizes_to_utc() -> None:
    # construct a minimal concrete CanonicalObject using exact nested shell values
    ...
```

The committed test must replace the illustrative final ellipsis with complete executable setup and assertions.

- [ ] **Step 2: Commit tests before production code**

```bash
git add tests/unit/test_p2_shared_canonical_shell.py
git commit -m "test: define P2 shared canonical shell contract"
```

- [ ] **Step 3: Run/observe RED**

Run locally when available:

```bash
PYTHONPATH=src python -m pytest tests/unit/test_p2_shared_canonical_shell.py -q
```

Expected before implementation: FAIL during import because the P2 shared-shell types do not yet exist. In the remote execution path, open/update the P2 PR and require the PR workflow to show the same failure before writing production code.

---

### Task 2: Implement shared canonical-shell support and structural bases

**Files:**
- Modify: `src/design_intelligence/contracts/core/types.py`
- Create: `src/design_intelligence/contracts/core/shell.py`
- Modify: `src/design_intelligence/contracts/core/__init__.py`
- Modify: `src/design_intelligence/contracts/__init__.py`
- Test: `tests/unit/test_p2_shared_canonical_shell.py`

**Interfaces:**
- Consumes: `FrozenDIModel`, `ObjectId`, `LogicalId`, `SchemaVersion`, `ObjectType`, `ExactObjectRef`, `CanonicalRef`.
- Produces: exact shared support/nested values and structural bases used by every B01 model.

- [ ] **Step 1: Add exact nominal support types**

Add strict frozen RootModels in `core/types.py` using `Annotated[..., Field(...)]`:

```python
class ActorId(RootModel[Annotated[str, Field(min_length=1)]]): ...
class ActorType(RootModel[Annotated[str, Field(min_length=1)]]): ...
class TenantId(RootModel[Annotated[str, Field(min_length=1)]]): ...
class ObjectRevision(RootModel[Annotated[int, Field(ge=1)]]): ...

class TenantScopeType(StrEnum):
    GLOBAL = "GLOBAL"
    TENANT = "TENANT"
```

Do not add opaque-ID regexes and do not close `ActorType`.

- [ ] **Step 2: Add exact nested support models**

Create `core/shell.py` with:

```python
class ActorRef(FrozenDIModel):
    actor_type: ActorType
    actor_id: ActorId

class TenantScope(FrozenDIModel):
    scope_type: TenantScopeType
    tenant_id: TenantId | None

class Provenance(FrozenDIModel):
    source_refs: tuple[CanonicalRef, ...]
    external_source_refs: tuple[Annotated[str, Field(min_length=1)], ...]
```

Use a model validator on `TenantScope` to enforce GLOBAL→null and TENANT→non-null. Do not add `command_ref` or `run_ref`.

- [ ] **Step 3: Add structural canonical bases**

In the same module:

```python
class CanonicalObject(FrozenDIModel):
    schema_version: SchemaVersion
    id: ObjectId
    object_type: ObjectType
    created_at: datetime
    created_by: ActorRef
    tenant_scope: TenantScope
    provenance: Provenance
    extensions: dict[str, JsonValue]

class CanonicalRevision(CanonicalObject):
    logical_id: LogicalId
    revision: ObjectRevision
    parent_refs: tuple[ExactObjectRef, ...]

class ImmutableFact(CanonicalObject):
    pass
```

Validate `created_at`: reject naive values and normalize aware values with `value.astimezone(timezone.utc)`. Use a recursive JSON-native type whose float branch forbids NaN/Infinity; do not invent owner semantic constraints.

- [ ] **Step 4: Export the frozen P2 shared API**

Export the new symbols from `contracts/core/__init__.py` and `contracts/__init__.py`. Do not register support types.

- [ ] **Step 5: Verify GREEN and P0/P1 regression**

```bash
PYTHONPATH=src python -m pytest tests/unit/test_p2_shared_canonical_shell.py -q
PYTHONPATH=src python -m pytest tests/unit tests/schemas/test_p0_core_schemas.py tests/schemas/test_p1_reference_schemas.py tests/hashing tests/cross_language tests/registry -q
```

Expected: shared-shell test PASS; all P0/P1 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/design_intelligence/contracts/core src/design_intelligence/contracts/__init__.py tests/unit/test_p2_shared_canonical_shell.py
git commit -m "feat: implement frozen shared canonical shell"
```

---

### Task 3: B01 exact-model RED tests

**Files:**
- Create: `tests/schemas/test_p2_b01_schemas.py`

**Interfaces:**
- Consumes: Task 2 shared shell and P1 persistent refs.
- Produces executable contract for B01 nested values and seven owner models.

- [ ] **Step 1: Write exact field/classification tests**

Tests must assert:

```text
RequirementStrength == MUST/PREFER/EXPLORE/AVOID/FORBID
BriefRequirement fields == statement,strength,dimension
ContextRefBinding fields == context_ref,role
DesignSpecAssignment fields == parameter_key,value,strength
StyleBrief owner fields == contract section 6.2
ReferenceIntentBinding owner fields == contract section 7.2
DesignContextBinding owner fields == contract section 8.2
DesignDecision owner fields == contract section 9.2
DesignRoute owner fields == contract section 10.2
DesignSpec owner fields == contract section 11.2
DesignTaskBinding owner fields == contract section 12.2
```

Also assert six authored objects subclass `CanonicalRevision`, `DesignTaskBinding` subclasses `ImmutableFact`, fixed `object_type` values reject mismatches, extra fields are forbidden, all owner fields are required, and forbidden B03/runtime fields cannot be supplied.

- [ ] **Step 2: Write owner validation tests**

```python
with pytest.raises(ValidationError):
    ReferenceIntentBinding(..., intent_codes=(), ...)
with pytest.raises(ValidationError):
    DesignRoute(..., mechanisms=(), ...)
with pytest.raises(ValidationError):
    DesignSpec(..., assignments=(), ...)
```

Also confirm an unknown non-empty reference intent code is accepted so the code vocabulary remains open.

- [ ] **Step 3: Commit tests and observe RED**

```bash
git add tests/schemas/test_p2_b01_schemas.py
git commit -m "test: define P2 B01 exact schema contract"
PYTHONPATH=src python -m pytest tests/schemas/test_p2_b01_schemas.py -q
```

Expected before B01 production implementation: FAIL because B01 model exports do not yet exist.

---

### Task 4: Implement B01 nested values and seven exact schemas

**Files:**
- Create: `src/design_intelligence/contracts/b01/models.py`
- Modify: `src/design_intelligence/contracts/b01/__init__.py`
- Test: `tests/schemas/test_p2_b01_schemas.py`

**Interfaces:**
- Consumes: `CanonicalRevision`, `ImmutableFact`, `ExactObjectRef`, `ObjectRef`, `CanonicalRef`, JSON-native value type.
- Produces: `RequirementStrength`, `BriefRequirement`, `ContextRefBinding`, `DesignSpecAssignment`, `StyleBrief`, `ReferenceIntentBinding`, `DesignContextBinding`, `DesignDecision`, `DesignRoute`, `DesignSpec`, `DesignTaskBinding`.

- [ ] **Step 1: Implement B01 nested values**

Use `StrEnum` only for the frozen closed `RequirementStrength`; use strings for open intent codes. All nested models inherit `FrozenDIModel`.

- [ ] **Step 2: Implement six CanonicalRevision owner objects**

Define all frozen fields exactly and make `object_type` a required fixed literal per owner, e.g.:

```python
class DesignRoute(CanonicalRevision):
    object_type: Literal["di.b01.design_route"]
    decision_ref: ExactObjectRef
    route_name: str
    mechanisms: tuple[str, ...]
    constraints: tuple[BriefRequirement, ...]
    rationale: str | None
```

Use `Annotated[tuple[T, ...], Field(min_length=1)]` only for the three owner-level non-empty rules explicitly frozen by the contract. Do not add mutable route selection/status, prompt, model, executor, seed, B02 definitions, or compiled-reference fields.

- [ ] **Step 3: Implement DesignTaskBinding as ImmutableFact**

Exact fields:

```python
design_state_ref: ObjectRef
style_brief_ref: ExactObjectRef
evaluation_contract_ref: CanonicalRef
enterprise_hard_policy_refs: tuple[CanonicalRef, ...]
risk_policy_ref: CanonicalRef | None
budget_policy_ref: CanonicalRef | None
intervention_policy_ref: CanonicalRef | None
reference_task_spec_ref: ExactObjectRef
```

Do not duplicate ARSO task content.

- [ ] **Step 4: Export B01 API and verify GREEN**

```bash
PYTHONPATH=src python -m pytest tests/schemas/test_p2_b01_schemas.py -q
PYTHONPATH=src python -m pytest tests/unit/test_p2_shared_canonical_shell.py tests/unit/test_p1_refs.py -q
```

- [ ] **Step 5: Commit**

```bash
git add src/design_intelligence/contracts/b01 tests/schemas/test_p2_b01_schemas.py
git commit -m "feat: implement frozen B01 exact schemas"
```

---

### Task 5: B01 CanonicalPayload/hash RED→GREEN

**Files:**
- Create: `src/design_intelligence/contracts/b01/hashing.py`
- Modify: `src/design_intelligence/contracts/b01/__init__.py`
- Create: `tests/hashing/test_p2_b01_payload_hashing.py`

**Interfaces:**
- Consumes: seven B01 canonical models, P1 `compute_content_hash`.
- Produces: `b01_canonical_payload()` and `compute_b01_content_hash()` implementing the frozen owner selector without changing generic P1 hashing.

- [ ] **Step 1: Write failing owner-payload tests**

For representative `StyleBrief`, `DesignSpec`, and `DesignTaskBinding`, assert payload keys contain exactly:

```text
schema_version
object_type
all concrete B01 owner fields
extensions
```

and exclude all shell identity/order/audit fields listed by the owner contract. Assert changing `created_at`, `created_by`, `tenant_scope`, `provenance`, `id`, `logical_id`, `revision`, or `parent_refs` does not change the B01 content hash, while changing an owner semantic field or `extensions` does.

- [ ] **Step 2: Observe RED**

```bash
PYTHONPATH=src python -m pytest tests/hashing/test_p2_b01_payload_hashing.py -q
```

Expected: FAIL because owner payload functions do not exist.

- [ ] **Step 3: Implement selector and hash helper**

Use an explicit allow-list derived from each concrete model's B01 owner fields; do not implement a generic blacklist over arbitrary canonical models. Convert through Pydantic JSON mode before calling P1 hashing so RootModels/enums/refs become JSON-native values.

```python
def b01_canonical_payload(obj: B01CanonicalObject) -> dict[str, JsonValue]: ...

def compute_b01_content_hash(obj: B01CanonicalObject) -> ContentHash:
    return compute_content_hash(b01_canonical_payload(obj))
```

Reject non-B01 inputs rather than guessing an owner policy.

- [ ] **Step 4: Verify GREEN and commit**

```bash
PYTHONPATH=src python -m pytest tests/hashing/test_p2_b01_payload_hashing.py tests/hashing/test_p1_hashing.py -q
git add src/design_intelligence/contracts/b01 tests/hashing/test_p2_b01_payload_hashing.py
git commit -m "feat: add B01 canonical payload hashing"
```

---

### Task 6: Exact B01 registry RED→GREEN

**Files:**
- Create: `src/design_intelligence/registry/b01.py`
- Modify: `src/design_intelligence/registry/__init__.py`
- Create: `tests/registry/test_p2_b01_registry.py`

**Interfaces:**
- Consumes: P1 registry models and seven B01 Python type paths.
- Produces: `B01_REGISTRY_MANIFEST` plus an indexable exact seven-entry registry surface.

- [ ] **Step 1: Write failing matrix tests**

Assert exact object types, Python paths, object classes, versioning/ref kinds, `logical_authoring_ref_allowed`, and `review_snapshot_eligible`. Assert all seven common values are exactly the owner contract values and that the manifest contains exactly seven unique entries.

- [ ] **Step 2: Observe RED**

```bash
PYTHONPATH=src python -m pytest tests/registry/test_p2_b01_registry.py -q
```

Expected: FAIL because B01 registry manifest is absent.

- [ ] **Step 3: Implement seven frozen entries**

Build `ObjectRegistryManifest(entries=(...))` using the exact matrix from owner contract §13. No shared support type and no B02+/ARSO primitive receives an entry.

- [ ] **Step 4: Verify GREEN and P1 registry regression**

```bash
PYTHONPATH=src python -m pytest tests/registry -q
```

- [ ] **Step 5: Commit**

```bash
git add src/design_intelligence/registry tests/registry/test_p2_b01_registry.py
git commit -m "feat: register frozen B01 object inventory"
```

---

### Task 7: AC-01 conformance and JSON Schema artifacts

**Files:**
- Create: `tests/conformance/ac/test_ac_01_b01_exact_schemas.py`
- Create: `tools/export_b01_json_schemas.py`
- Create: seven files under `generated/json_schema/` for the B01 canonical objects
- Create: `P2_B01_EXACT_SCHEMAS_AUDIT.md`

**Interfaces:**
- Consumes: P2 B01 models, owner payload helper, B01 registry manifest.
- Produces: executable AC-01 evidence and deterministic JSON Schema artifacts for the seven canonical B01 objects.

- [ ] **Step 1: Write AC-01 conformance tests**

Assert all seven canonical classes exist and generate JSON Schema; schema object-type constants, inheritance field presence, required owner fields, `additionalProperties=false`, and registry↔model path/object-type agreement. Assert `AC-01` covers exactly seven B01 canonical objects and no B02+ surface.

- [ ] **Step 2: Observe any RED before exporter/audit completion**

```bash
PYTHONPATH=src python -m pytest tests/conformance/ac/test_ac_01_b01_exact_schemas.py -q
```

- [ ] **Step 3: Add deterministic exporter**

The exporter imports exactly the seven canonical B01 classes, calls `model_json_schema()`, and writes UTF-8 JSON using sorted keys and a final newline. Generated files must be reproducible by rerunning the tool.

- [ ] **Step 4: Add audit record**

`P2_B01_EXACT_SCHEMAS_AUDIT.md` records authority inputs, implemented surface, TDD RED/GREEN evidence, AC-01 result, P0/P1 regression result, unchanged frozen checksums, and explicitly states that P3+ remains unauthorized and global Exact V1 remains `FREEZE CANDIDATE`.

- [ ] **Step 5: Run full verification**

```bash
python -m pip install -e '.[test]'
PYTHONPATH=src python -m pytest -q
cd di_contracts_v1 && PYTHONPATH=. python -m pytest -q
cd ..
sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256
python -m compileall -q src/design_intelligence
python tools/export_b01_json_schemas.py
git diff --exit-code -- generated/json_schema
```

Expected: all current root tests PASS; candidate baseline PASS; checksum verification PASS; compile PASS; exporter idempotence PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/conformance/ac tools/export_b01_json_schemas.py generated/json_schema P2_B01_EXACT_SCHEMAS_AUDIT.md
git commit -m "test: close AC-01 B01 exact schema gate"
```

---

### Task 8: PR checkpoint and freeze boundary

**Files:**
- No production file changes unless verification exposes a P2-scoped defect.

**Interfaces:**
- Consumes: complete P2 implementation branch and GitHub Actions.
- Produces: reviewable P2 PR checkpoint; does not merge to `main` without a separate human freeze/merge decision.

- [ ] **Step 1: Verify branch diff scope**

```bash
git diff --name-only main...HEAD
```

Expected changes only in P2 plan/tests/shared-shell+B01 implementation/registry/generated B01 schemas/audit. `di_contracts_v1/` and frozen source bytes must be unchanged.

- [ ] **Step 2: Require fresh exact-head CI**

The P2 PR must run the existing PR workflow against the exact head. Any failed root, baseline, checksum, compile, or whitespace gate blocks completion.

- [ ] **Step 3: Record status**

If all gates pass:

```text
P0 = FROZEN / regression PASS
P1 = FROZEN / regression PASS
P2.0/P2.0A = FROZEN / checksum unchanged
P2 implementation = COMPLETE / REVIEW CANDIDATE
AC-01 = PASS
P3+ = NOT AUTHORIZED
Exact V1 global = FREEZE CANDIDATE
```

Do not merge P2 to `main` solely because CI is green. A separate human review/freeze decision is required.

## Self-Review

- Spec coverage: all 7/7 B01 canonical objects, four B01 nested values/value sets, shared canonical shell dependencies, owner validation, payload policy, registry matrix, and AC-01 are mapped to implementation tasks.
- Boundary coverage: no B02, ARSO production imports, B03 runtime lowering, B07 resolver semantics, Command/Event/Protocol, CAS, snapshot, UI, executor, or optimizer work is included.
- TDD coverage: every new production surface has an explicit failing-test stage before implementation.
- Type consistency: B01 persistent refs use only P1 `ExactObjectRef | ObjectRef`; authored B01 objects inherit `CanonicalRevision`; `DesignTaskBinding` inherits `ImmutableFact`; registry persistent-ref kinds match those classifications.
