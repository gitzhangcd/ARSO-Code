# ARSO P0.1 I1 Implementation Design

## Status

`FREEZE CANDIDATE` for the I1 implementation slice only.

## Upstream checkpoint

I1 MUST branch from the verified I0 checkpoint:

```text
branch: arso-p0-1-i0
commit: cf7a974346ffe685f6c5ed809651690055eb3643
```

I0 remains immutable after this fork.

## Goal

Implement the smallest executable scientific-integrity layer that can turn the I0 contract skeleton into a deterministic synthetic matched-block run while preserving the P0.1 causal-comparison boundary.

I1 is intentionally narrower than the full D2/D3 runtime. It implements:

```text
Scientific integrity enforcement
+ deterministic fake adapters
+ one synthetic four-condition matched-block E2E
```

It does not execute Batch-001 and does not call a real model provider.

## Scientific boundary

The scientific question remains open:

```text
Does oracle diagnosis improve validated repair?
```

I1 does not answer that question. Its job is to establish that the implementation can represent and enforce the intended comparison without contamination.

These invariants remain normative:

```text
DiagnosisCondition = only intended treatment difference.
SealedTruth must not enter the non-Oracle repair-visible path.
Repair must not consume evaluator output.
Evaluator must be condition-blind.
Behavior-changing repair creates a new candidate snapshot.
Scientific admission requires integrity PASS.
Synthetic fixture != Batch-001.
Synthetic outcome != P0.1 empirical evidence.
```

## Chosen architecture

I1 adopts the approved **Thin Executable Scientific Harness** approach.

The alternatives are explicitly rejected for this slice:

```text
A. Integrity-gates-only implementation
   Rejected: insufficient because it does not prove that the gates compose in an actual trial pipeline.

C. Full D2/D3 runtime now
   Rejected: premature because retry, budget, resume, provider uncertainty, complete state-machine persistence, and production orchestration are not required to validate the first causal harness.
```

Therefore:

```text
I1 = minimal enforcement + deterministic E2E
I2+ = retry/budget/resume/full runtime hardening
```

## I1 pipeline

The one executable scientific path is:

```text
synthetic_001 manifest
        ↓
MatchedBlockPlanner
        ↓
4 P01TrialAssignments
        ↓
DiagnosisInjector
   ├── ORACLE
   ├── WRONG
   ├── NONE
   └── IMPLICIT
        ↓
RepairRequestBuilder
        ↓
DeterministicFakeRepairOperator
        ↓
CandidateMaterializer
        ↓
SyntheticExactEvaluator
        ↓
SyntheticValidator
        ↓
TrialIntegrityChecker
        ↓
ScientificAdmissionGate
        ↓
MatchedBlockIntegrityChecker
        ↓
SyntheticMatchedBlockResult
```

The four conditions MUST traverse the same orchestration path. Condition-specific behavior is represented only through `DiagnosisInjection.visible_payload` and the controlled Oracle sealed-access path.

## New runtime package

I1 adds:

```text
src/arso/p01/runtime/
├── __init__.py
├── truth_firewall.py
├── matched_control.py
├── evaluator_blindness.py
├── admission.py
├── diagnosis.py
├── repair_request.py
├── candidate.py
├── validation.py
├── integrity.py
└── matched_block.py

src/arso/p01/adapters/fake/
├── __init__.py
├── fixture.py
├── repair.py
└── evaluator.py
```

The exact file split may be reduced if implementation reveals unnecessary fragmentation, but the semantic boundaries MUST remain distinct.

## I1 contract additions

I1 may add only the minimal additional experimental records required for the synthetic E2E.

### CandidateChangeRecord

Represents a proposed behavior-changing repair materialized against an immutable base snapshot.

Required semantics:

```text
base snapshot remains unchanged
changed targets must be subset of allowed mutation targets
candidate has a distinct identity/hash from baseline
materialization failure is explicit
```

### SyntheticEvaluationRecord

A harness-only deterministic evaluation record. It is not promoted to a universal ARSO `EvaluationRecord` implementation.

Required fields include:

```text
evaluation_id
trial_id
candidate_ref
passed
observations
condition_metadata_present = false
```

### SyntheticValidationResult

Harness-only validation output with:

```text
ACCEPTED | REJECTED | INCONCLUSIVE
```

### MatchedBlockIntegrityReport

Block-level report that checks cross-arm invariants that cannot be established from one trial alone.

At minimum:

```text
all_required_conditions_present
shared_fixture
shared_visible_evidence
shared_repair_operator
shared_mutation_policy
shared_evaluator
shared_budget_policy
shared_seed_policy
shared_pre_run_lock
shared_matched_control_fingerprint
condition_is_only_intended_difference
final_status
violations
```

### SyntheticMatchedBlockResult

An execution summary referencing four immutable trial outcomes plus the block integrity report. It MUST NOT contain a scientific interpretation of treatment effect.

## 1. Truth Firewall

The I0 red gate becomes real enforcement.

### Allowed sealed access purposes

The runtime uses the already frozen purpose vocabulary:

```text
ORACLE_DIAGNOSIS_MATERIALIZATION
EVALUATION
FIXTURE_QUALIFICATION
SCIENTIFIC_AUDIT
```

### Access rule

Ordinary repair execution receives no sealed-access capability.

Oracle materialization may read only the prequalified oracle-diagnosis payload. It MUST NOT expose:

```text
full causal truth
expected repair patch
evaluation answer
sealed scoring truth
```

to the repair request.

Non-Oracle conditions MUST be rejected if they request Oracle diagnosis materialization.

Evaluation may access sealed scoring truth through a separate evaluation capability, and that data MUST NOT flow back into repair input.

## 2. Diagnosis materialization

I1 implements a deterministic `SyntheticDiagnosisInjector` for all four conditions.

### ORACLE

Uses the sealed `oracle_diagnosis.json` through the Truth Firewall and materializes only its approved `visible_payload`.

### WRONG

Uses a pre-frozen wrong diagnosis defined in the synthetic manifest/condition data. It MUST NOT inspect the real planted fault at runtime to invent a wrong answer.

### NONE

Materializes a valid `DiagnosisInjection` with `visible_payload = null`.

### IMPLICIT

Uses a frozen harness-only implicit formulation that provides the same public evidence and repair objective but no explicit fault label, fault locus, causal mechanism, or oracle diagnosis.

All four outputs have the same contract shape.

## 3. Repair request boundary

The existing I0 `RepairRequest` remains the only repair-visible request shape.

The builder MUST NOT accept or embed:

```text
SealedFixtureTruth
condition_type
ground_truth_fault
causal_truth
expected_repair_target
evaluation_answer
```

The repair operator can infer differences only from the ordinary visible request content, including the materialized diagnosis payload.

## 4. Deterministic fake repair operator

`DeterministicFakeRepairOperator` exists only to test scientific plumbing.

It MUST NOT branch on hidden `condition_type`.

It receives only `RepairRequest` plus repair-visible fixture content resolved through normal refs.

Its deterministic policy is deliberately simple:

```text
if visible diagnosis identifies the reversed mapping mechanism:
    propose the allowed identity-mapping repair
else:
    emit a predefined alternative/no-op proposal according to the harness rule
```

The fake operator is not intended to simulate LLM intelligence. It is a deterministic instrument for verifying treatment isolation, candidate materialization, evaluation blindness, and block-level integrity.

## 5. Candidate materialization

I1 introduces the first behavior-changing materialization step.

Allowed mutation locus for `synthetic_001`:

```text
transformation_spec.mapping
```

Any attempt to modify task definition, evaluator, success criterion, sealed reference, budget, or another system field is rejected.

Materialization produces a new candidate representation and never mutates the baseline fixture.

Negative tests MUST demonstrate that an out-of-policy patch is rejected.

## 6. Condition-blind evaluator

`SyntheticExactEvaluator` deterministically evaluates candidate behavior against the task's expected input/output rule.

The evaluator-facing API MUST NOT receive:

```text
condition
condition_type
diagnosis_injection
repair reasoning
matched arm label
```

The runtime applies an `EvaluatorBlindnessGuard` before evaluation.

If forbidden condition metadata is present, evaluation MUST be rejected and the trial cannot be scientifically admitted.

## 7. Synthetic validator

The validator is intentionally small in I1.

It checks:

```text
target behavior passes
hard constraints hold
baseline object was not mutated
candidate mutation stayed inside the allowed locus
```

Output vocabulary is:

```text
ACCEPTED
REJECTED
INCONCLUSIVE
```

Validation success does not itself imply scientific admission.

## 8. Matched control enforcement

I1 implements `MatchedControlChecker` at block scope.

For all four conditions in one synthetic matched block, the checker verifies equality of the frozen shared controls, at minimum:

```text
fixture/public fixture identity
reference task
base snapshot
visible evidence
repair operator identity
repair instruction
mutation policy
evaluator binding
validation plan
budget policy
retry policy identity, even though retry is not executed in I1
seed policy
pre-run-lock hash
runtime semantics version
```

The diagnosis treatment itself is excluded from the shared fingerprint.

Any mismatch makes the block scientifically invalid even if every individual trial executed successfully.

## 9. Scientific admission gate

A trial is admitted only if:

```text
execution completed
validation result exists
trial integrity report = PASS
no truth-firewall violation
no evaluator-blindness violation
no forbidden mutation
required records are complete
```

A matched block is admitted only if:

```text
all four required conditions are present
all admitted trials belong to the same matched block
block integrity report = PASS
shared fingerprint equality holds
```

`ValidationState.ACCEPTED` MUST NOT bypass this gate.

## 10. Synthetic matched-block runner

I1 adds a thin orchestration function/class that runs exactly one `synthetic_001` block.

The runner is not a general workflow engine.

It MUST:

```text
load the fixed harness manifest
construct the four assignments
materialize each diagnosis condition
build repair-visible requests
invoke deterministic fake repair
materialize candidates
run condition-blind evaluation
validate candidates
compute trial integrity
apply scientific admission
compute block integrity
return an immutable synthetic result summary
```

It MUST NOT implement:

```text
parallel workers
queues
database persistence
provider retry
budget exhaustion recovery
resume after crash
general task scheduling
adaptive search
```

## 11. Error handling

I1 uses explicit harness errors for scientific-boundary violations.

At minimum:

```text
SealedAccessDenied
RepairVisibilityViolation
MatchedControlViolation
EvaluatorBlindnessViolation
MutationPolicyViolation
ScientificAdmissionDenied
SyntheticFixtureError
```

Scientific-integrity errors are not retryable infrastructure errors.

I1 does not implement retry semantics beyond explicitly refusing to reinterpret scientific failure as a retry condition.

## 12. Test strategy

I1 follows strict TDD.

### Existing red gates to turn green

The four I0 xfail gates become normal passing tests only after their real enforcement exists:

```text
TruthFirewall
MatchedControlChecker
EvaluatorBlindnessGuard
ScientificAdmissionGate
```

The marker/xfailed status MUST be removed as each capability becomes implemented. I1 closes with no `p01_red` gate remaining for these four behaviors.

### New unit/contract tests

At minimum:

```text
Oracle-only sealed diagnosis access
non-Oracle sealed diagnosis access denied
None injection has null visible payload
Wrong diagnosis does not read sealed causal truth
RepairRequest contains no forbidden truth fields
out-of-policy candidate mutation rejected
evaluator input rejects condition metadata
validation does not imply admission
fingerprint mismatch invalidates block
baseline fixture remains unchanged after repair
```

### Negative contamination tests

At minimum deliberately inject:

```text
different model/repair-operator identity across arms
different evidence identity across arms
different evaluator identity across arms
condition metadata in evaluator input
sealed expected repair target in repair path
mutation outside allowed locus
missing required condition
```

Every contamination MUST cause trial/block non-admission.

### End-to-end test

A top-level test runs one synthetic matched block and asserts:

```text
exactly four conditions executed
all use one shared matched-control fingerprint
all non-treatment controls match
no non-Oracle sealed access occurred
evaluator remained condition-blind
baseline remained immutable
all required records exist
block integrity PASS for the clean fixture
synthetic result contains no scientific-effect claim
```

A companion contaminated-block E2E test MUST demonstrate automatic rejection.

## 13. Reproducibility scope

I1 is fully deterministic because every executable component is local and synthetic.

Therefore the synthetic harness may claim deterministic reproducibility for I1 only.

This MUST NOT be generalized to future real-provider P0.1 runs.

No API key, provider request, network call, or external model identity participates in I1.

## 14. Non-goals

I1 MUST NOT add:

```text
real OpenAI/Anthropic/other model adapter
Batch-001 fixture or scenario data
learned DiagnosisEngine
IdentifiabilityEngine
ProbePlan/ProbeOperator
adaptive SearchController
persistent memory
meta-optimizer
production Deployment
SQL/database layer
queue/workflow framework
retry engine
budget manager
crash resume
full D2 state-transition persistence
parallel execution
statistical treatment-effect analysis
```

These are deferred unless a later implementation gate explicitly requires them.

## 15. Repository protection

I1 MUST NOT modify frozen files under:

```text
src/design_intelligence/contracts/
di_contracts_v1/
```

Existing repository-level exact-ref/hash primitives may be reused, as in I0, without redefining ownership.

No I1 type is promoted to a universal ARSO canonical primitive merely because it is executable.

## 16. I1 acceptance gates

I1 is eligible for `IMPLEMENTED / VERIFIED` only if all of the following are true:

```text
I1-G01  TruthFirewall enforcement is executable and tested.
I1-G02  Non-Oracle repair flow cannot obtain sealed oracle truth.
I1-G03  Oracle flow exposes only approved oracle diagnosis payload.
I1-G04  All four conditions use one orchestration path.
I1-G05  Repair-visible request excludes condition metadata and sealed truth.
I1-G06  Fake repair operator does not branch on hidden condition type.
I1-G07  Candidate materialization creates a new state and preserves baseline immutability.
I1-G08  Mutation outside the frozen locus is rejected.
I1-G09  Evaluator is condition-blind by contract and runtime guard.
I1-G10  Validation and scientific admission remain separate.
I1-G11  Trial integrity PASS is required for admission.
I1-G12  Matched-block integrity checks shared-control equality.
I1-G13  Clean synthetic block completes with block integrity PASS.
I1-G14  Contaminated synthetic block is automatically rejected.
I1-G15  Existing four p01_red gates are converted to ordinary green tests.
I1-G16  Full repository regression remains green.
I1-G17  Frozen DI/source drift checks remain green.
I1-G18  No real provider call occurs.
I1-G19  Batch-001 remains unexecuted.
I1-G20  No empirical P0.1 claim is produced.
```

## 17. Exit state

Successful I1 closes at:

```text
I1 status: IMPLEMENTED / VERIFIED
Synthetic matched block: EXECUTED / DETERMINISTIC
Scientific-integrity enforcement: ACTIVE FOR SYNTHETIC HARNESS
Batch-001: NOT EXECUTED
Real provider calls: NONE
P0.1 empirical hypothesis: OPEN
```

The next slice after I1 is expected to harden runtime semantics needed before real pilot execution, especially retry/budget/attempt selection/state persistence and provider-facing reproducibility. Those features are intentionally not pulled into I1.
