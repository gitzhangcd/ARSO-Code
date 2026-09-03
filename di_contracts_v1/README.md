# Design Intelligence V5.0 — Exact V1 Contract Candidate

F6.1 implementation baseline for the ARSO V2.2.1 reference application.

## Implemented

- F0/F1 canonical base models: strict Pydantic v2, nominal IDs, exact/object/logical refs, immutable canonical classes, operational state, semantic hashing candidate.
- Machine-readable Object Registry with ownership, storage class, state domain, ref kind, snapshot eligibility, intervention eligibility and historical-SSOT metadata.
- Representative Exact V1 contracts for E03–E08, including GenerationPackage, DesignStateRevision, HumanDecision, ProbeRecommendation, SystemChangeCandidate, KnowledgePromotionDecision and KnowledgeSnapshot.
- Command/Event role separation and protocol surfaces.
- F6 normalization: no canonical ReviewSessionClosed object; InterventionTransaction is operational; no mutable candidate_status; MemoryMaturity follows final cross-spec vocabulary.
- Automated tests for core schema strictness, reference semantics, registry invariants, semantic prefix, review provenance, non-executable ProbeRecommendation, stable knowledge gates, and cross-contract meta rules.

## Intentionally not frozen yet

- Full B01/B02 exact semantic payload schemas.
- Full ARSO Core Pydantic models (this package references ARSO-owned primitives rather than shadowing them).
- RFC 8785 cross-language canonical-hash proof; current serializer is deterministic Python JSON and is marked candidate.
- Complete 240-gate test surface from F0–F6; this baseline executes a first concrete subset.
- Physical DB schema, REST/gRPC transport, algorithms, thresholds, production activation.

## Run

```bash
PYTHONPATH=. pytest -q
PYTHONPATH=. python tools/export_artifacts.py
python -m compileall -q di_contracts
```
