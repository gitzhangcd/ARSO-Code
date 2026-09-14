# ARSO P0.1 I0 Verification Checkpoint

## Status

```text
I0 status: IMPLEMENTED / VERIFIED
Scientific experiment status: NOT STARTED
Batch-001 status: NOT EXECUTED
Real provider calls: NONE
Frozen DI Exact-V1 contract modifications: NONE
Next gate: I1 integrity enforcement + deterministic fake adapters + E2E synthetic matched block
```

This checkpoint verifies only the I0 implementation slice. It does not constitute evidence for the P0.1 Oracle Diagnosis Value scientific hypothesis.

## Scope verified

I0 now contains:

- strict `arso.p01` experimental contract models;
- the exact four-condition vocabulary `ORACLE | WRONG | NONE | IMPLICIT`;
- repair-visible contract boundaries that exclude raw condition type and sealed repair truth;
- D3 Protocol skeletons for fixture, diagnosis, repair, evaluation, and integrity boundaries;
- a deterministic harness-only `synthetic_001` fixture with public / sealed / qualification separation;
- four intentionally unimplemented I1 runtime integrity gates registered as strict `p01_red` xfails.

No production provider adapter, Batch-001 case, diagnosis engine, probe policy, adaptive search, database, queue, or deployment path was introduced.

## TDD evidence

### Port skeleton RED -> GREEN

The pre-implementation commit failed collection with:

```text
ModuleNotFoundError: No module named 'arso.p01.ports'
```

After the minimal Protocol implementation, both repository verification workflows passed at commit:

```text
de13ae6499b1f853ed0dd956d9ea1cf5ed01fb0c
```

### Synthetic fixture RED -> GREEN

The layout test was committed before fixture contents and failed because:

```text
experiments/p0_1_oracle_diagnosis/fixtures/synthetic_001/public/task.json
```

was absent. After adding the deterministic public / sealed / qualification fixture, both repository verification workflows passed at commit:

```text
e2ca21058bbdefeb1e2cf5724e67b81ba3aea729
```

### Intentionally red I1 gates

I0 registers four strict-xfail runtime enforcement tests for:

```text
TruthFirewall
MatchedControlChecker
EvaluatorBlindnessGuard
ScientificAdmissionGate
```

These APIs are intentionally absent in I0. The default suite therefore remains green with the tests reported as XFAIL. An isolated replay of the exact four test files with `--runxfail` produced four intended failures due to the missing `arso.p01.runtime` enforcement layer.

## Verification commands and observations

### Full repository regression

Command executed by GitHub Actions on the I0 branch:

```bash
PYTHONPATH=src python -m pytest -q
```

Observed at commit `861e6fa9583597ed4bc84093cea1e7f07cacccd0`:

```text
139 passed
4 xfailed (the intentional p01_red gates)
exit status: 0
```

The same run also verified:

```bash
PYTHONPATH=src python -m pytest \
  tests/unit/test_p1_refs.py \
  tests/schemas/test_p1_reference_schemas.py \
  tests/hashing \
  tests/cross_language \
  tests/registry \
  tests/repository/test_p1_scope.py -q
```

Observed:

```text
61 passed
exit status: 0
```

Candidate-baseline regression:

```bash
cd di_contracts_v1 && PYTHONPATH=. python -m pytest -q
```

Observed:

```text
46 passed
exit status: 0
```

The workflow also passed normative checksum verification, package compilation, whitespace checks, and frozen-source / candidate-baseline drift checks.

### Focused P0.1 green surface

The focused command specified by the I0 plan is:

```bash
pytest tests/p01/contracts tests/p01/fixtures -q
```

The current focused surface contains 12 green tests (3 base/enums + 6 I0 contract + 2 port-signature + 1 fixture-layout test). These 12 tests are included in the successful 139-pass repository run above. The connected execution environment did not provide a separate repository shell run for this focused command, so this checkpoint does not misrepresent it as a separately executed CI step.

### Forced-red gate

Plan command:

```bash
pytest -m p01_red --runxfail -q
```

Observed in an isolated replay using the exact four committed gate files:

```text
4 failed
failure cause: missing I1 runtime enforcement module / APIs
exit status: non-zero, as intended
```

The repository CI independently confirms the same files collect cleanly as four strict XFAIL entries in the normal run.

## Frozen-contract non-regression

`git diff origin/main...HEAD` contains no modifications beneath:

```text
src/design_intelligence/contracts/
di_contracts_v1/
```

The repository's frozen-source drift gate reported:

```text
Original frozen sources unchanged; scoped checksum-registered contracts are allowed.
```

Therefore I0 has not altered the previously frozen DI Exact-V1 contract surface.

## Scientific boundary

I0 establishes implementation scaffolding only. In particular:

```text
Synthetic fixture != Batch-001
Synthetic success != P0.1 evidence
XFAIL integrity gates != implemented enforcement
Contract skeleton != full ARSO runtime
```

No result in this checkpoint supports or rejects:

```text
Does perfect / oracle diagnosis improve validated repair?
```

That question remains experimentally open.

## I0 decision

```text
Repository bootstrap                 PASS
Strict experimental contracts       PASS
D3 port skeletons                    PASS
Public / sealed fixture split        PASS
Default regression suite             PASS
Frozen DI non-regression             PASS
Red I1 enforcement gates present     PASS
Batch-001 execution                  NOT STARTED
P0.1 empirical claim                 OPEN
```

I0 is ready to close after branch review. The next implementation slice is I1: implement the scientific-integrity enforcement layer, deterministic fake adapters, and the first end-to-end synthetic matched block while keeping all real provider calls disabled.
