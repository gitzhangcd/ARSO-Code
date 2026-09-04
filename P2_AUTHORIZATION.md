# P2 Authorization

## 决策

```text
P2: AUTHORIZED
Scope: Full B01 Exact Schemas
```

用户于 2026-09-05 明确批准：

```text
P2.0 Freeze
→ merge PR #5 into PR #4
→ verify combined PR #4 head
→ record P2_0_FREEZE_DECISION
→ merge PR #4 to main
→ verify published main checkpoint
→ authorize P2｜Full B01 Exact Schemas
```

## 生效依据

P2.0/P2.0A frozen checkpoint 已发布到：

```text
main@8beef2baa733a346e0aa81ac5ffd652f926be84b
```

该 merge commit 的 tree：

```text
c2993995da42ebc6bd7ab8b847e4fcf1041161f8
```

与 freeze-decision head：

```text
d77243d0c129d505ae0f735c58f30a50c8426cab
```

的 tree SHA 完全一致：

```text
c2993995da42ebc6bd7ab8b847e4fcf1041161f8
```

因此 `main` published checkpoint 与已经执行 fresh CI 的 freeze-decision tree byte-for-byte identical。

Freeze-decision exact-head verification：

```text
P1 contract verification
run 33900622143 = SUCCESS

P2.0 B01 + Shared-Core contract verification
run 33900622142 = SUCCESS
```

P2.0 Freeze record：

```text
P2_0_FREEZE_DECISION.md
```

## P2 implementation scope

P2 只授权实现 frozen B01 Exact V1 contracts：

```text
StyleBrief
DesignContextBinding
DesignDecision
DesignRoute
DesignSpec
ReferenceIntentBinding
DesignTaskBinding
```

并实现这些 models 所需要、已经在 P2.0A 冻结的 shared canonical-shell support types / structural bases。

允许进入：

```text
P2 written implementation design / plan
TDD RED tests
minimal production schemas
B01 registry entries required by frozen owner contract
owner-specific validation needed by frozen P2.0 contract
P0/P1/P2 regression gates
AC-01 conformance evidence
```

## 明确未授权

```text
P3 / Full B02 Exact Schemas
P4 ARSO exact primitive imports beyond unavoidable frozen P2 dependency boundaries
B03-B08 production models
Command/Event/Protocol completion
semantic resolver/store/CAS beyond P2 schema-local validation
snapshot firewalls
UI / LLM / image-generation integration
optimizer / deployment / DEFERRED capabilities
```

如果 P2 implementation 遇到 owner contract 中没有冻结的 exact field/type/behavior：

```text
SPEC_GAP
→ stop affected path
→ do not guess
```

如果发现无法同时满足的 frozen contract：

```text
SPEC_CONFLICT
→ stop affected path
```

## Branch governance

P2 在独立 branch 上执行：

```text
p2-b01-exact-schemas
```

该 branch 从 verified frozen checkpoint：

```text
main@8beef2baa733a346e0aa81ac5ffd652f926be84b
```

创建。

`main` 继续代表最近的人类批准 frozen checkpoint。

当前状态：

```text
P0: FROZEN
P1: FROZEN
P2.0/P2.0A: FROZEN
P2: AUTHORIZED / IMPLEMENTATION NOT STARTED
P3+: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```
