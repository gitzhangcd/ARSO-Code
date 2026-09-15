# ARSO P0.1 I1 Verification Checkpoint

## Status

```text
I1 status: IMPLEMENTED / VERIFIED
Synthetic matched block: EXECUTED / DETERMINISTIC
Scientific-integrity enforcement: ACTIVE FOR SYNTHETIC HARNESS
Batch-001: NOT EXECUTED
Real provider calls: NONE
P0.1 empirical hypothesis: OPEN
```

## Verification subject

```text
branch: arso-p0-1-i1
verified implementation commit: 98b91f68c7626a55372c6103cd6c601c07605a47
draft PR: #9
base branch: main
```

The implementation commit above is the I1 runtime state that underwent repository-wide PR verification. This verification record is committed afterward and is itself re-verified by the same PR workflows.

## Focused I1 verification

Command:

```bash
pytest tests/p01/contracts tests/p01/runtime tests/p01/conformance tests/p01/e2e tests/p01/fixtures -q
```

Observed result:

```text
31 passed
0 failed
0 xfailed
```

The four former I0 scientific-integrity red gates are now ordinary green tests:

```text
TruthFirewall
MatchedControlChecker
EvaluatorBlindnessGuard
ScientificAdmissionGate
```

No `test_*.py` files remain under `tests/p01/conformance_red/`.

## Repository-wide GitHub Actions verification

### P1 contract verification

```text
workflow: P1 contract verification
run: #133
head commit: 98b91f68c7626a55372c6103cd6c601c07605a47
conclusion: success
```

Observed checks:

```text
P1 targeted tests: 61 passed
Root repository tests: 170 passed, 0 failed
Root warnings: 2 existing Pydantic deprecation warnings
DI candidate baseline regression: 46 passed
Specification checksums: PASS
Production package compile: PASS
Non-Markdown whitespace gate: PASS
Markdown whitespace gate: PASS
Frozen source and candidate-baseline drift gate: PASS
```

The frozen-source gate emitted:

```text
Original frozen sources unchanged; scoped checksum-registered contracts are allowed.
```

All nine registered specification checksum entries reported `OK`.

### P2.0 B01 + Shared-Core verification

```text
workflow: P2.0 B01 + Shared-Core contract verification
run: #66
head commit: 98b91f68c7626a55372c6103cd6c601c07605a47
conclusion: success
```

Observed checks included:

```text
Full normative source checksums: PASS
Shared-core registered digest: PASS
B01 canonical object coverage: 7/7
Shared-core required section coverage: 11/11
P0/P1 regression: PASS
Root repository tests: 170 passed
DI candidate baseline regression: 46 passed
Compile frozen production package: PASS
Placeholder scan: PASS
Patch whitespace checks: PASS
Authority-source scope gate: PASS
```

## Frozen-source non-regression

The I0-to-I1 comparison introduced I1 documents, synthetic condition artifacts, P0.1 runtime/adapters, and P0.1 tests only. It did not modify:

```text
src/design_intelligence/contracts/
di_contracts_v1/
```

The repository checksum gate independently confirmed all registered frozen authority files remain unchanged.

## Synthetic clean-block evidence

The deterministic synthetic matched-block E2E executes exactly the frozen four treatment conditions:

```text
ORACLE
WRONG
NONE
IMPLICIT
```

The clean harness asserts and passes the following properties:

```text
exactly four conditions execute
one shared matched-control fingerprint is used
shared non-treatment controls remain equal
non-Oracle repair paths do not read sealed oracle diagnosis
Evaluator remains condition-blind
baseline state remains immutable
required records are materialized
block integrity = PASS
all scientifically valid trials are admitted irrespective of repair success
scientific_interpretation = None
```

This is harness verification only.

## Contamination rejection evidence

The contaminated E2E intentionally changes `visible_evidence_ref` for one treatment arm before the block-level integrity check.

Observed expected behavior:

```text
shared_visible_evidence = false
condition_is_only_intended_difference = false
block integrity = FAIL
```

Thus the harness detects and rejects a cross-arm non-treatment mismatch rather than silently admitting the block.

## Provider and Batch-001 boundary

No real provider adapter or network model execution path was added in I1. The only executable adapters added under P0.1 are deterministic local fake adapters for fixture loading, repair, and evaluation.

Therefore:

```text
Real provider calls: NONE
Batch-001: NOT EXECUTED
```

## Scientific interpretation boundary

The synthetic harness is not empirical P0.1 evidence and cannot support a treatment-effect claim.

In particular, I1 does **not** establish:

```text
OracleDiagnosisHelpsRepair
OracleDiagnosisDoesNotHelpRepair
DiagnosisFirstIsValid
DiagnosisFirstIsInvalid
```

The scientific question remains open until the locked real pilot is executed under the upstream P0.1-A/P0.1-B manifest, fixture qualification, and pre-run lock.

## I1 exit state

```text
I1 status: IMPLEMENTED / VERIFIED
Synthetic matched block: EXECUTED / DETERMINISTIC
Scientific-integrity enforcement: ACTIVE FOR SYNTHETIC HARNESS
Batch-001: NOT EXECUTED
Real provider calls: NONE
P0.1 empirical hypothesis: OPEN
```
