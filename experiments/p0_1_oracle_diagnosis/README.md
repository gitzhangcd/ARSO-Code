# ARSO P0.1 synthetic harness fixture

This directory contains the **harness-only** `synthetic_001` fixture used to verify the P0.1 implementation boundary. It is not Batch-001, is not empirical evidence for the P0.1 hypothesis, and makes no scientific claim about diagnosis value.

The fixture deliberately separates repair-visible public data from sealed experimental truth:

- `public/`: task, baseline behavior, and observed evidence available to the repair path.
- `sealed/`: planted fault, causal truth, oracle diagnosis, and expected repair target. These are never repair-visible except for the approved oracle-diagnosis payload materialization.
- `qualification/`: records that the fixture is synthetic and qualified only for harness testing.

No real model provider is called by I0.
