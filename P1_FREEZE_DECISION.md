# P1 Freeze Decision

## 决策

```text
P1: FROZEN
```

用户于 2026-09-04 明确批准 P1 Freeze。

冻结范围：

```text
ExactObjectRef / ObjectRef / LogicalObjectRef
ContentHash wire normalization
RFC 8785 canonicalization + SHA-256 hashing engine
Python ↔ Node cross-language canonicalization gate
ObjectRegistryEntry / ObjectRegistryManifest
Generic registry persistence/history/reference invariants
RegistryIndex generic lookup/reference/eligibility guards
P1 repository scope boundary
```

冻结依据：

- `P1_REFERENCE_HASH_REGISTRY_AUDIT.md`
- `P1_REFERENCE_HASH_REGISTRY_FREEZE_REVIEW.md`
- GitHub Actions run `33749907003` on pre-decision head `b22a6a308f3ec65ebcff09de551e6780742c476c`: SUCCESS
- Independent Freeze Review: `Critical=0`, `Important=0`, `Minor=1 / NON-BLOCKING`

明确不包含：

```text
B01-B08 production models
complete Exact V1 registry inventory
owner-specific CanonicalPayload selection
semantic resolver/store/CAS
Command/Event/Protocol surfaces
ARSO shadow primitives
```

这些仍属于后续阶段与 Exact V1 release gates。

## 后续门禁

```text
P0: FROZEN
P1: FROZEN
P2: NOT AUTHORIZED
Exact V1: FREEZE CANDIDATE
```

本记录只确认 P1 Freeze；不自动授权 P2。P2 是否进入实现必须在 P1 merge 后独立检查 B01 owner exact contract 的可用性与完整性。
