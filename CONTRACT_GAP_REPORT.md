# Phase 0 Contract 差距报告

审计日期：2026-09-03  
审计范围：规范输入、现有 `di_contracts_v1` 基线、生成物、测试与仓库治理  
发布结论：**BLOCKED——Exact V1 继续保持 `FREEZE CANDIDATE`**

## 总体结论

现有 package 是一套有价值的 F6.1 可执行基线。当前 46 项测试全部通过，已经生成
JSON Schema，并且若干标准化不变量已经体现在代码中。但它还不是完整的 contract
repository，也无法满足优先级 1 规范定义的发布条件：

```text
CS-01..CS-32 AND AC-01..AC-18 = PASS
```

当前没有任何测试被命名或映射为完整的 CS/AC gate。因此，局部测试通过不能表述为
conformance freeze 已完成。

## 阻断性差距与实现偏离

| ID | 严重程度 | 发现 | 现场证据 | 必须采取的处理 |
|---|---|---|---|---|
| GAP-001 | Blocker | 完整 B01 exact schema 缺失。 | Registry 只有一个无法导入的 DesignSpec sentinel；7 个 B01 对象中有 6 个完全没有 entry/model。 | 获取或冻结 B01 owner contract；不得从叙述性规范推测字段。对应 AC-01。 |
| GAP-002 | Blocker | 完整 B02 exact schema 缺失。 | 4 个 B02 canonical object 均未出现在代码和 registry 中。 | 获取或冻结 B02 owner contract。对应 AC-02。 |
| GAP-003 | Blocker | 权威 ARSO type 尚未集成。 | 没有 `arso` package/import boundary；DI model 只使用通用 ref。 | 导入或适配权威 ARSO schema，禁止创建 DI shadow。对应 AC-03。 |
| GAP-004 | Blocker | Command inventory 不完整。 | 目前只有 4 个具体 command；优先级 1 的 N12 已明确现有基线不足。 | 新增代码前先冻结完整 command 清单及 exact field。对应 AC-04。 |
| GAP-005 | Blocker | Event inventory 不完整。 | 目前只有 `ReviewSessionClosedEvent`。 | 先冻结完整 event 清单及 exact metadata。对应 AC-05。 |
| GAP-006 | Blocker | Protocol 接口和 static typing 不完整。 | 只有 4 个 protocol；缺少 AssetStore、ArtifactRegistry、Executor / Model Gateway、ARSO boundary 和 static type gate。`CanonicalObjectStore` 还缺少 `resolve_logical_for_authoring`。 | 冻结 exact signature，并增加 static type fixture。对应 AC-06。 |
| GAP-007 | Blocker | Exact reference 的 semantic closure 未实现。 | `ExactObjectRef` 只验证字段形状；没有 resolver 验证 target 的 type、logical ID、version 和 hash。 | Contract 冻结后增加 resolver/store fixture。对应 AC-07。 |
| GAP-008 | Blocker | Revision-parent 行为未经证明。 | 只有 Protocol 声明；没有 CanonicalObjectStore implementation/fixture 验证 expected exact parent。 | 增加 expected-parent fixture 和冲突行为。对应 AC-08。 |
| GAP-009 | Blocker | CAS 行为未经证明。 | `DesignBranchRuntime` 只声明了方法；没有 atomic store double、`HEAD_CONFLICT` 行为或并发 fixture。 | 增加 CAS store fixture。对应 AC-09、CS-13。 |
| GAP-010 | Blocker | Snapshot negative firewall 缺失。 | ARSO SystemSnapshot 缺失；Knowledge/Review snapshot 没有基于 resolver 的 eligibility/materialization 测试。 | 增加 AC-10、AC-11、AC-12 fixture。 |
| GAP-011 | Blocker | 未实现 RFC 8785 canonicalization，也没有 cross-language test。 | `canonical_json_bytes` 使用 Python `json.dumps`；代码自身将其标记为 deterministic candidate。 | 使用 RFC 8785，并建立 byte-identical cross-language fixture。对应 AC-13。 |
| GAP-012 | Blocker | Registry 不完整。 | 目前有 44 个 entry；B01、B02、B07、Infrastructure、ARSO mandatory surface 均有缺失。 | 只能在 owner exact schema 就绪后补齐。对应 AC-14。 |
| GAP-013 | Blocker | B07 canonical surface 不完整。 | 20 个 B07 对象中缺少 8 个：DesignEdit、ForkRecord、MergeAnalysis、SemanticMergeConflict、MergeResolution、MergeRecord、DesignComment、DesignAnnotation。 | 冻结并实现 exact B07 model 及关联 command/event 接口。 |
| GAP-014 | High | Registry 中存在无法解析的 canonical type。 | `di.b01.design_spec` 指向 `external.B01.DesignSpec`，而 `external` 无法导入。 | B01 就绪前，将其保留为明确的非 canonical placeholder，或从 executable manifest 移除。 |
| GAP-015 | High | 3 个 B08 registry entry 违反优先级 1 的 Artifact eligibility 标准化规则。 | `BrandDNAProfile`、`RetentionPolicy`、`KnowledgeAccessPolicy` 设置了 `artifact_eligible=true`；N08 明确这些 Knowledge-domain object 默认不是直接的 System Artifact target。 | 在后续通过评审的实施阶段修正，并增加 invariant test。 |
| GAP-016 | High | CanonicalPayload 的字段包含策略缺少完整证据。 | Hash 代码除 N09 明确列出的字段外，还排除了 `id`、`logical_id`、`revision` 和 `parent_refs`。 | 在把 hash 视为 conformance 之前，先冻结每类对象的 CanonicalPayload 策略。 |
| GAP-017 | High | 没有全局强制拒绝未解析的 Logical authoring ref。 | 3 种 ref model 已区分，但没有 committed/runtime graph scan 或 resolver gate 拒绝未解析的 `LogicalObjectRef`。 | 增加递归 closure validation。 |
| GAP-018 | High | CS/AC 覆盖无法追踪。 | 已有 46 项测试，但测试源码中没有 CS/AC 编号，也没有生成 requirement-to-test 映射矩阵。 | 建立一套带明确 ID 和证据的可追踪 acceptance suite。 |
| GAP-019 | Medium | 生成的 conformance report 相对优先级 1 的标准化结论已经过时。 | 报告仍把 KnowledgeSnapshot validity 和 MemoryItem lifecycle overlap 视为未解决 candidate，而 N05/N07 已经给出冻结结论。 | 只在实施修正完成后重新生成；当前报告不得作为规范依据。 |
| GAP-020 | RESOLVED | 原审计发现 `/specs` 路径不存在。 | 规范现已统一迁移到 `specs/`。 | Phase 1 通过 checksum manifest 持续验证规范源内容。 |
| GAP-021 | Medium | 优先级 3 的规范身份存在歧义。 | `Cross-Spec-Consistency-Freeze.txt` 内部声明为 `DI-V5-ENG`，并非独立的 Cross-Spec 文档。 | 最终冻结前确认或补充正确的优先级 3 规范源。 |
| GAP-022 | Medium | 当前无法执行建议的 Git/PR freeze 节奏。 | 仓库根目录不是 Git repository。 | 确认此目录是否应成为 repository root，或是否应纳入其他 repository。 |
| GAP-023 | Medium | 当前扁平 package 结构没有隔离建议的 contract layer。 | 缺少 `src/`、`b01`、`b02`、`arso` 和 infrastructure contract package。 | 只能在 Phase 0 评审后处理；结构差异本身不构成重构授权。 |

## 可以保留的现有证据

以下内容可作为后续工作的 candidate-level asset，但不能作为发布结论：

- 严格且 frozen 的 Pydantic base，以及 nominal ID/ref type；
- Registry 中 object class 与 reference kind 的校验；
- DesignSpec sentinel entry 的 negative registry flag；
- GenerationCompiler 的 artifact/intervention flag；
- 不可变 DesignState 的 semantic-prefix validation；
- Review root 与 closure event 分离的方向；
- ProbeRecommendation 在结构上不包含 execution-authority field；
- MemoryMaturity 与 KnowledgeMaturity 使用不同 enum；
- MemoryItem 没有第二个通用 lifecycle field；
- KnowledgeSnapshot 的 validity ref 是 optional，而不是 mandatory；
- 当前 registry 子集不包含已知 forbidden shadow name；
- 隔离 Python 环境中，现有 46 项 unit test 全部通过。

## CS 覆盖审计

`STRUCTURAL` 表示本地 model/test 只支持要求的一部分，尚无 resolver、store 或 runtime
conformance 证明整个 gate。`BLOCKED` 表示 mandatory contract 或 integration boundary 缺失。

| Gate | 当前证据 | 状态 |
|---|---|---|
| CS-01、CS-02 | 44 个 registry entry 各有一个 enum owner，并包含 capability-owner field；但 registry 不完整。 | STRUCTURAL |
| CS-03、CS-04、CS-05 | B01 以及 ARSO ReferenceTaskSpec、SystemSnapshot、Run contract 缺失。 | BLOCKED |
| CS-06、CS-07 | DesignSpec sentinel 具有 negative flag，GenerationCompiler 具有 positive flag；但 resolver/intervention boundary 缺失。 | STRUCTURAL |
| CS-08、CS-09 | B03 nested value 已存在，但 DesignEdit、ReferenceAsset、ReferenceIntentBinding 和 execution behavior 不完整。 | BLOCKED |
| CS-10、CS-11、CS-12 | 3 种 lineage root model 和 operational pointer/transaction class 已存在；缺少完整 registry/runtime scan。 | STRUCTURAL |
| CS-13 | 只有 CAS Protocol 声明。 | BLOCKED |
| CS-14、CS-15、CS-16 | 已有 frozen state/root model 和 closure event 方向；projection/history behavior 未通过 end-to-end test。 | STRUCTURAL |
| CS-17、CS-18、CS-19、CS-20 | 已有 Review snapshot 和 HumanDecision ref；缺少 materialization、reconstruction、resolver、ARSO evaluation 和 executor provenance fixture。 | BLOCKED |
| CS-21 | ProbeRecommendation 没有明显的 execution-authority field，并有直接 unit test。 | STRUCTURAL；属于当前最强证据之一 |
| CS-22、CS-23 | ARSO ActionDecision、ProbePlan、ProbeResult、Evidence integration 缺失。 | BLOCKED |
| CS-24 | PromotionEvidencePack 使用 ObjectRef，但缺少 ARSO type resolution。 | STRUCTURAL |
| CS-25、CS-26 | B08 model 已区分 content/snapshot 概念，但 activation/retrieval protocol 和 negative firewall 缺失。 | BLOCKED |
| CS-27 | 使用不同 maturity enum，并有直接 unit test。 | STRUCTURAL；属于当前最强证据之一 |
| CS-28 | 已有 owner-targeted command，但 B02 owner schema/commit boundary 缺失。 | BLOCKED |
| CS-29、CS-30、CS-31 | ARSO integration、SystemSnapshot firewall、controlled learning/intervention flow 缺失。 | BLOCKED |
| CS-32 | Model 为 immutable，但没有覆盖完整长期 loop 的 acceptance fixture。 | STRUCTURAL |

本轮审计不把任何 CS gate 提升为最终 `PASS`，因为优先级 1 要求整套 suite 必须明确且完整。

## AC 覆盖审计

| Gate | 当前状态 | 原因 |
|---|---|---|
| AC-01 | FAIL | B01 exact schema 缺失。 |
| AC-02 | FAIL | B02 exact schema 缺失。 |
| AC-03 | FAIL | 权威 ARSO import 缺失。 |
| AC-04 | FAIL | Command inventory 不完整且未冻结。 |
| AC-05 | FAIL | Event inventory 不完整且未冻结。 |
| AC-06 | FAIL | Protocol capability、signature 和 static check 不完整。 |
| AC-07 | FAIL | Semantic resolver fixture 缺失。 |
| AC-08 | FAIL | Store revision-parent fixture 缺失。 |
| AC-09 | FAIL | CAS fixture 缺失。 |
| AC-10 | FAIL | SystemSnapshot firewall 缺失。 |
| AC-11 | FAIL | KnowledgeSnapshot resolver/firewall 缺失。 |
| AC-12 | FAIL | ReviewSnapshot provenance firewall 缺失。 |
| AC-13 | FAIL | RFC 8785 cross-language fixture 缺失。 |
| AC-14 | FAIL | Mandatory registry surface 不完整。 |
| AC-15 | PARTIAL | 当前 registry 子集具有 forbidden-name test，但没有扫描完整 source/schema/import surface。 |
| AC-16 | PARTIAL | 当前只检查少量 hard-coded name，没有完整的 ambiguous bare-name scan。 |
| AC-17 | SCHEMA SATISFIED / GATE UNPROVED | MemoryItem 没有重复 lifecycle field，但缺少明确的 AC-17 acceptance test。 |
| AC-18 | SCHEMA SATISFIED / GATE UNPROVED | `knowledge_validity_refs` 为 optional，并非 mandatory，但缺少明确的 AC-18 acceptance test。 |

## 阶段结论

Phase 0 已经完成并通过人工评审，Phase 1 Contract Repository Skeleton 已获授权。
本报告中的其他 `SPEC_GAP` 与 implementation drift 仍然有效；不得因此提前开始
Core、B01 或 B02 编码。
