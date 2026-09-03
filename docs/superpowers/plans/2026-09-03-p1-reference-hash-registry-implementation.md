# P1 Exact References + Canonical Hash + Registry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the approved P1 foundation for exact references, RFC 8785 content hashing, and the minimum executable Object Registry contract without entering P2 or inventing downstream owner schemas.

**Architecture:** Exact reference DTOs and `ContentHash` live in the core contract layer. Canonical payload selection stays outside P1; the P1 hashing module accepts only already-prepared JSON-native values and applies RFC 8785 + SHA-256. Registry entry/manifest contracts implement the full minimum field surface required by Exact Contract §20, while a separate validation/index layer enforces generic class/reference/eligibility rules without pretending the complete B01–B08 inventory exists.

**Tech Stack:** Python >=3.12, Pydantic >=2.12,<3, `rfc8785==0.1.4`, pytest >=8,<9, Node.js test oracle with `canonicalize@4.0.0` locked under `tests/cross_language/node/`.

**Spec:** `docs/superpowers/specs/2026-09-03-p1-reference-hash-registry-design.md`

## Global Constraints

- Work only on branch `p1-refs-hash-registry`; never implement on `main`.
- Highest authority: `specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md`.
- P0 public contracts remain backward compatible.
- P2 is not authorized. Do not add B01–B08 production models, ARSO shadow models, resolver/store/CAS, commands/events/protocols, or complete registry inventory.
- `di_contracts_v1/` is read-only candidate evidence; never copy it wholesale or edit it.
- `CanonicalPayload` composition is owner-specific and deferred. P1 must not implement a generic model-to-payload blacklist extractor.
- `ContentHash` exact wire form is `^sha256:[0-9a-f]{64}$`.
- Canonical JSON is RFC 8785 bytes, not `json.dumps(sort_keys=True)`.
- Registry entry field surface must include every minimum field required by Exact Contract §20.
- Every production behavior follows RED -> verify RED -> GREEN -> verify GREEN.
- GitHub CI remains `NOT CONFIGURED` unless status checks actually appear.

---

## File Structure

### Core contracts
- Create `src/design_intelligence/contracts/core/refs.py` — `ContentHash`, `ExactObjectRef`, `ObjectRef`, `LogicalObjectRef`, `CanonicalRef`.
- Create `src/design_intelligence/contracts/core/hashing.py` — `JsonValue`, `canonical_json_bytes`, `compute_content_hash` only.
- Modify `src/design_intelligence/contracts/core/types.py` — add `PrimitiveOwner` and `StateDomain` nominal string shells only if not kept in registry models.
- Modify `src/design_intelligence/contracts/core/__init__.py` and `src/design_intelligence/contracts/__init__.py` — export P1 public core surface.

### Registry
- Create `src/design_intelligence/registry/models.py` — `ReferenceKind`, `ObjectRegistryEntry`, `ObjectRegistryManifest`.
- Create `src/design_intelligence/registry/validation.py` — generic invariant validator helpers.
- Create `src/design_intelligence/registry/index.py` — `RegistryIndex` derived lookup and policy checks.
- Modify `src/design_intelligence/registry/__init__.py` — export P1 registry surface.

### Tests
- Create `tests/unit/test_p1_refs.py`.
- Create `tests/schemas/test_p1_reference_schemas.py`.
- Create `tests/hashing/test_p1_hashing.py`.
- Create `tests/cross_language/fixtures.json`.
- Create `tests/cross_language/node/package.json`.
- Create `tests/cross_language/node/package-lock.json`.
- Create `tests/cross_language/node/canonicalize.mjs`.
- Create `tests/cross_language/test_p1_cross_language_jcs.py`.
- Create `tests/registry/test_p1_registry_models.py`.
- Create `tests/registry/test_p1_registry_index.py`.
- Replace the P0-only repository scope guard with a P1-aware guard in `tests/repository/test_p0_scope.py` or a new `tests/repository/test_p1_scope.py` while preserving P0 regression intent.

### Packaging / audit
- Modify `pyproject.toml` to add exact runtime dependency `rfc8785==0.1.4`.
- Create `P1_REFERENCE_HASH_REGISTRY_AUDIT.md` only after implementation verification.
- Update current-state governance docs only after P1 implementation completes; do not declare P1 frozen before user review.

---

### Task 1: Exact reference contracts and ContentHash

**Files:**
- Create: `tests/unit/test_p1_refs.py`
- Create: `tests/schemas/test_p1_reference_schemas.py`
- Create: `src/design_intelligence/contracts/core/refs.py`
- Modify: `src/design_intelligence/contracts/core/__init__.py`
- Modify: `src/design_intelligence/contracts/__init__.py`

**Interfaces:**
- Consumes: P0 `ObjectId`, `LogicalId`, `ObjectType`, `FrozenDIModel`.
- Produces: `ContentHash`, `ExactObjectRef`, `ObjectRef`, `LogicalObjectRef`, `CanonicalRef`.

- [ ] **Step 1: Write RED tests for ContentHash**

```python
import pytest
from pydantic import ValidationError

from design_intelligence.contracts.core import ContentHash


def test_content_hash_accepts_exact_sha256_wire_form() -> None:
    value = "sha256:" + "a" * 64
    assert ContentHash(value).root == value


@pytest.mark.parametrize(
    "value",
    [
        "a" * 64,
        "sha256:" + "A" * 64,
        "sha256:" + "a" * 63,
        "md5:" + "a" * 64,
    ],
)
def test_content_hash_rejects_noncanonical_wire_forms(value: str) -> None:
    with pytest.raises(ValidationError):
        ContentHash(value)
```

- [ ] **Step 2: Run RED**

Run: `PYTHONPATH=src python -m pytest tests/unit/test_p1_refs.py -q`
Expected: FAIL because `ContentHash` does not exist.

- [ ] **Step 3: Add RED tests for exact ref fields, strictness, immutability and extra rejection**

```python
from design_intelligence.contracts.core import ExactObjectRef, LogicalObjectRef, ObjectRef


def test_exact_object_ref_has_only_frozen_fields() -> None:
    ref = ExactObjectRef(
        object_type="di.test.object",
        logical_id="logical-id",
        version_id="version-id",
        content_hash="sha256:" + "1" * 64,
    )
    assert ref.model_dump().keys() == {"object_type", "logical_id", "version_id", "content_hash"}
```

Add equivalent tests for `ObjectRef`, `LogicalObjectRef`, mutation rejection, extra field rejection, and cross-nominal misuse.

- [ ] **Step 4: Implement minimal refs module**

```python
class ContentHash(RootModel[str]):
    model_config = ConfigDict(strict=True, frozen=True)

    @field_validator("root")
    @classmethod
    def validate_hash(cls, value: str) -> str:
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", value):
            raise ValueError("content hash must be sha256:<64 lowercase hex>")
        return value


class ExactObjectRef(FrozenDIModel):
    object_type: ObjectType
    logical_id: LogicalId
    version_id: ObjectId
    content_hash: ContentHash
```

Implement `ObjectRef`, `LogicalObjectRef`, and `CanonicalRef = ExactObjectRef | ObjectRef` analogously.

- [ ] **Step 5: Verify GREEN**

Run: `PYTHONPATH=src python -m pytest tests/unit/test_p1_refs.py tests/schemas/test_p1_reference_schemas.py -q`
Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `feat: add P1 exact reference contracts`

---

### Task 2: RFC 8785 canonicalization and SHA-256 hashing

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/hashing/test_p1_hashing.py`
- Create: `src/design_intelligence/contracts/core/hashing.py`
- Modify: core public `__init__.py` files.

**Interfaces:**
- Consumes: `ContentHash` from Task 1.
- Produces: `JsonValue`, `canonical_json_bytes(payload) -> bytes`, `compute_content_hash(payload) -> ContentHash`.

- [ ] **Step 1: Write RED tests proving deterministic JCS behavior**

```python
from design_intelligence.contracts.core.hashing import canonical_json_bytes


def test_canonical_json_orders_object_properties() -> None:
    assert canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'
```

Add tests for Unicode preservation, nested arrays/objects, booleans/null, and representative numeric serialization.

- [ ] **Step 2: Write RED rejection tests**

Use payloads containing `float("nan")`, positive/negative infinity, and non-string mapping keys. Each must raise rather than silently coerce.

- [ ] **Step 3: Verify RED**

Run: `PYTHONPATH=src python -m pytest tests/hashing/test_p1_hashing.py -q`
Expected: FAIL because hashing module/API does not exist.

- [ ] **Step 4: Add exact dependency**

Change project dependencies to include:

```toml
dependencies = ["pydantic>=2.12,<3", "rfc8785==0.1.4"]
```

- [ ] **Step 5: Implement minimal canonicalizer**

```python
import hashlib
import rfc8785

JsonScalar = None | bool | int | float | str
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


def canonical_json_bytes(payload: JsonValue) -> bytes:
    return rfc8785.dumps(payload)


def compute_content_hash(payload: JsonValue) -> ContentHash:
    digest = hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return ContentHash(f"sha256:{digest}")
```

Do not accept Pydantic models and do not add a model-to-payload converter.

- [ ] **Step 6: Verify GREEN**

Run: `PYTHONPATH=src python -m pytest tests/hashing/test_p1_hashing.py -q`
Expected: PASS with no warnings.

- [ ] **Step 7: Commit**

Commit message: `feat: add RFC8785 canonical hashing engine`

---

### Task 3: Cross-language RFC 8785 conformance fixture

**Files:**
- Create: `tests/cross_language/fixtures.json`
- Create: `tests/cross_language/node/package.json`
- Create: `tests/cross_language/node/package-lock.json`
- Create: `tests/cross_language/node/canonicalize.mjs`
- Create: `tests/cross_language/test_p1_cross_language_jcs.py`

**Interfaces:**
- Consumes: `canonical_json_bytes` from Task 2.
- Produces: executable cross-language byte equality gate; no production API.

- [ ] **Step 1: Define locked Node oracle**

`package.json` must contain only `canonicalize@4.0.0` as dev dependency and `package-lock.json` must lock that exact package version/integrity. `canonicalize.mjs` reads JSON from stdin and writes canonical JSON to stdout without additional whitespace.

- [ ] **Step 2: Write repository fixtures**

Include cases for Unicode keys/values, escaping, nested objects, arrays, boolean/null, and IEEE-754-safe numeric values. Do not include values JSON itself cannot represent such as NaN/Infinity.

- [ ] **Step 3: Write RED cross-language test**

The pytest test must:
1. verify Node is available;
2. verify `node_modules` can be prepared with `npm ci` in an isolated test setup;
3. run `canonicalize.mjs` for each fixture;
4. compare `stdout.encode("utf-8")` exactly with Python `canonical_json_bytes(payload)`.

- [ ] **Step 4: Verify RED or environment blocker correctly**

Run: `PYTHONPATH=src python -m pytest tests/cross_language/test_p1_cross_language_jcs.py -q`
Expected before Node fixture installation: FAIL for missing oracle dependency, not because production hashing is wrong.

- [ ] **Step 5: Prepare locked dependency and run GREEN**

Run `npm ci` under `tests/cross_language/node/`, then rerun pytest. Expected: all fixtures PASS byte-for-byte.

- [ ] **Step 6: Commit**

Commit message: `test: add cross-language RFC8785 conformance gate`

---

### Task 4: Registry entry and manifest schema

**Files:**
- Create: `tests/registry/test_p1_registry_models.py`
- Create: `src/design_intelligence/registry/models.py`
- Modify: `src/design_intelligence/registry/__init__.py`
- Modify: `src/design_intelligence/contracts/core/types.py` if `PrimitiveOwner`/`StateDomain` are placed there.

**Interfaces:**
- Consumes: `CanonicalObjectClass`, `SchemaVersion`, `ObjectType`, P1 refs.
- Produces: `PrimitiveOwner`, `StateDomain`, `ReferenceKind`, `ObjectRegistryEntry`, `ObjectRegistryManifest`.

- [ ] **Step 1: Write RED schema surface test**

Assert the exact field set required by §20:

```python
EXPECTED_FIELDS = {
    "object_type", "python_type", "schema_version", "canonical",
    "primitive_owner", "capability_owners", "object_class", "state_domain",
    "versioned", "persistent_ref_kind", "historical_ssot",
    "logical_authoring_ref_allowed", "system_snapshot_eligible",
    "knowledge_snapshot_eligible", "review_snapshot_eligible",
    "system_intervention_target_eligible", "artifact_eligible",
}
assert set(ObjectRegistryEntry.model_fields) == EXPECTED_FIELDS
```

Also assert every governance field is required; no hidden default may fill a mandatory declaration.

- [ ] **Step 2: Write RED type tests**

`PrimitiveOwner` and `StateDomain` accept strict strings but remain runtime-distinct nominal types. `ReferenceKind` is exactly `EXACT_OBJECT_REF`, `OBJECT_REF`, `NONE`.

- [ ] **Step 3: Write RED duplicate manifest test**

Two entries with the same `object_type` must make `ObjectRegistryManifest` fail validation.

- [ ] **Step 4: Verify RED**

Run: `PYTHONPATH=src python -m pytest tests/registry/test_p1_registry_models.py -q`
Expected: FAIL because registry production models do not exist.

- [ ] **Step 5: Implement minimal models**

Use `FrozenDIModel`, explicit required fields, tuple capability owners, and an `after` validator for unique `object_type` values in manifest. Do not add `manifest_id`, `generated_at`, or manifest `content_hash` because those metadata are not frozen by Exact Contract §20.

- [ ] **Step 6: Verify GREEN**

Run: `PYTHONPATH=src python -m pytest tests/registry/test_p1_registry_models.py -q`
Expected: PASS.

- [ ] **Step 7: Commit**

Commit message: `feat: add P1 registry contracts`

---

### Task 5: Generic registry invariants

**Files:**
- Create: `src/design_intelligence/registry/validation.py`
- Extend: `tests/registry/test_p1_registry_models.py`

**Interfaces:**
- Consumes: `ObjectRegistryEntry`, `ReferenceKind`, `CanonicalObjectClass`.
- Produces: validation of generic persistence/history invariants only.

- [ ] **Step 1: Write RED tests for each object class**

Test valid and invalid combinations for:
- `CANONICAL_REVISION`: historical SSOT true, versioned true, exact ref.
- immutable fact/root/graph/snapshot: historical SSOT true, versioned false, object ref.
- operational state: historical SSOT false, versioned false, no persistent ref.
- derived view: in P1 executable registry historical SSOT false, versioned false, no persistent ref.

- [ ] **Step 2: Verify RED**

Expected: invalid combinations currently validate successfully.

- [ ] **Step 3: Implement validator**

Prefer one focused `validate_registry_entry(entry)` function called from `ObjectRegistryEntry` model validation, or a single model validator delegating to `validation.py`. Do not encode object-specific B03/B05/B06/B08 policies here.

- [ ] **Step 4: Verify GREEN**

Run: `PYTHONPATH=src python -m pytest tests/registry/test_p1_registry_models.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: enforce registry persistence invariants`

---

### Task 6: RegistryIndex and reference/eligibility checks

**Files:**
- Create: `tests/registry/test_p1_registry_index.py`
- Create: `src/design_intelligence/registry/index.py`
- Modify: `src/design_intelligence/registry/__init__.py`

**Interfaces:**
- Consumes: `ObjectRegistryManifest`, `ExactObjectRef`, `ObjectRef`, `ReferenceKind`.
- Produces: `RegistryIndex.require`, `contains`, `validate_reference_kind`, and four eligibility guard methods.

- [ ] **Step 1: Write RED lookup tests**

`require(ObjectType(...))` returns the exact entry. Unknown type raises `KeyError` (or one local non-public lookup error if already frozen by repository error policy); no fallback or fuzzy lookup.

- [ ] **Step 2: Write RED reference-kind tests**

An exact ref is accepted only for entries whose `persistent_ref_kind` is `EXACT_OBJECT_REF`; an `ObjectRef` only for `OBJECT_REF`; entries with `NONE` reject either persistent ref.

- [ ] **Step 3: Write RED eligibility tests**

Each guard must reject entries whose corresponding flag is false:
- system snapshot
- knowledge snapshot
- review snapshot
- system intervention target

- [ ] **Step 4: Verify RED**

Run: `PYTHONPATH=src python -m pytest tests/registry/test_p1_registry_index.py -q`
Expected: FAIL because `RegistryIndex` does not exist.

- [ ] **Step 5: Implement minimal index**

Build an internal dict by `object_type.root`; rely on manifest uniqueness validation. Guard methods call `require()` and inspect only the frozen registry fields; they must not resolve target objects or hashes.

- [ ] **Step 6: Verify GREEN**

Run both registry test files; expected PASS.

- [ ] **Step 7: Commit**

Commit message: `feat: add registry lookup and policy guards`

---

### Task 7: P1 scope guard and public API freeze candidate

**Files:**
- Create or modify: `tests/repository/test_p1_scope.py`
- Modify: public `__init__.py` files as needed.

**Interfaces:**
- Consumes: all P0/P1 public types.
- Produces: repository stage boundary tests.

- [ ] **Step 1: Write RED stage-scope tests**

Assert P1 required symbols exist and P2+ namespaces remain class-free. Explicitly forbid early production definitions for B01/B02 and resolver/store/CAS/command/event/protocol classes. Preserve the AST-based non-core guard concept but permit registry classes introduced by P1.

- [ ] **Step 2: Write public API exact-set test**

Ensure core/registry exports include only approved P0+P1 public names; do not accidentally export third-party `rfc8785` symbols or local implementation helpers.

- [ ] **Step 3: Verify RED, then minimally update exports/guard**

Run P1 scope tests until GREEN.

- [ ] **Step 4: Run P0 regression tests**

Run: `PYTHONPATH=src python -m pytest tests/unit/test_core_base_models.py tests/unit/test_core_nominal_types.py tests/unit/test_core_object_class.py tests/schemas/test_p0_core_schemas.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `test: freeze P1 repository scope`

---

### Task 8: Full verification, audit and PR review readiness

**Files:**
- Create: `P1_REFERENCE_HASH_REGISTRY_AUDIT.md`
- Modify: `README.md`, `AGENTS.md`, `SPEC_AUTHORITY.md` only to state `P1 COMPLETE / AUTOMATED CHECKS PASS / AWAITING USER FREEZE REVIEW`; never mark P1 FROZEN.

**Interfaces:**
- Produces: evidence package for independent P1 Freeze Review.

- [ ] **Step 1: Run targeted P1 suite**

```bash
PYTHONPATH=src python -m pytest \
  tests/unit/test_p1_refs.py \
  tests/schemas/test_p1_reference_schemas.py \
  tests/hashing \
  tests/cross_language \
  tests/registry \
  tests/repository/test_p1_scope.py -q
```

Expected: PASS.

- [ ] **Step 2: Run full root regression**

`PYTHONPATH=src python -m pytest -q`
Expected: PASS.

- [ ] **Step 3: Run candidate baseline regression**

`(cd di_contracts_v1 && PYTHONPATH=. python -m pytest -q)`
Expected: existing 46 tests PASS.

- [ ] **Step 4: Verify authoritative specs**

`sha256sum -c specs/SPEC_SOURCE_CHECKSUMS.sha256`
Expected: 7/7 OK.

- [ ] **Step 5: Verify source quality**

Run `python -m compileall -q src/design_intelligence`, public imports, and `git diff --check`.
Expected: all clean.

- [ ] **Step 6: Verify no candidate/spec drift**

Confirm no changed files under `di_contracts_v1/` or `specs/` relative to P1 base `main`.

- [ ] **Step 7: Write audit**

Document:
- P1 Requirement Matrix;
- `P1-N01` ContentHash normalization;
- baseline reuse/adapt/reject decisions;
- cross-language byte proof and exact package versions;
- registry schema/invariant coverage;
- explicitly deferred gates;
- actual test counts;
- GitHub CI status as `NOT CONFIGURED` unless checks exist.

- [ ] **Step 8: Update current-state docs and commit**

Commit message: `docs: record P1 verification checkpoint`

- [ ] **Step 9: Independent PR review**

Review GitHub PR patch against exact spec. Any blocker is fixed on the same branch and all verification reruns. Final state before user approval:

```text
P0: FROZEN
P1: COMPLETE / AUTOMATED CHECKS PASS / INDEPENDENT REVIEW PASS / AWAITING USER FREEZE
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

---

## Plan Self-Review

### Spec coverage
- Exact ref wire fields: Task 1.
- ContentHash normalization: Task 1.
- RFC 8785 + SHA-256: Task 2.
- Cross-language gate: Task 3.
- Full §20 minimum registry field surface: Task 4.
- Generic persistence/history invariants: Task 5.
- Registry lookup/reference/eligibility policy: Task 6.
- P1/P2 scope boundary: Task 7.
- Full regression/audit/freeze evidence: Task 8.

### Explicit non-coverage by design
- Object-specific canonical payload selection: downstream owner contracts.
- Complete registry inventory: downstream + AC-14/P14.
- Semantic target resolution: P13.
- B01/B02 exact schemas: P2/P3 only after owner contracts are frozen.
- ARSO exact imports: P4.

### Placeholder scan
No `TBD`, `TODO`, `implement later`, or undefined neighboring interfaces are permitted in this plan.

### Type consistency
`ContentHash`, reference DTOs, registry fields, and `RegistryIndex` signatures match the approved written P1 design spec.