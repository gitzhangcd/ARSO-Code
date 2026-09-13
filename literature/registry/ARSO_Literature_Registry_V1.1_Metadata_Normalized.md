# ARSO Literature Registry V1.1｜Metadata-Normalized Edition

**Project:** Adaptive Reflective Semantic Optimizer (ARSO)  
**Registry version:** V1.1  
**Date:** 2026-09-13  
**Parent:** ARSO Literature Registry V1.0  

## 0. What changed from V1.0

V1.1 preserves all V1.0 registry IDs and ARSO disposition labels, while adding bibliographic-normalization fields:

`canonical_title`, `authors`, `publication_year`, `venue`, `identifier_type`, `identifier`, `doi`, `canonical_url`, `first_seen_in_arso`, `last_verified_date`, `verification_status`, `resolution_notes`, `metadata_completeness`.

Important: metadata was not guessed. Where a short name or Daily Brief label could not be mapped safely to a unique primary source, the item remains `UNRESOLVED`. Where a likely mapping exists but a homonymous paper makes the mapping non-unique (e.g. CAPO), the item is marked `LIKELY_RESOLVED` with an explicit note.

## 1. Verification snapshot

- Total registry records: **122**
- Primary-source / high-confidence normalized: **77**
- Verified from PDF/secondary source but still missing at least one canonical bibliographic field: **5**
- Likely resolved but retained with ambiguity warning: **1**
- Unresolved / requires another source-recovery pass: **39**
- High-completeness metadata records: **78**

### Verification status counts

| Status | Count |
|---|---:|
| LIKELY_RESOLVED | 1 |
| UNRESOLVED | 39 |
| VERIFIED_PDF | 2 |
| VERIFIED_PRIMARY | 77 |
| VERIFIED_SECONDARY | 3 |

## 2. Normalized Registry

| ID | Canonical title | Authors | Year | Venue | Identifier / DOI | ARSO disposition | Verification | Completeness |
|---|---|---|---:|---|---|---|---|---|
| ARSO-LIT-001 | Co-Evolving Harnesses and Models: On-Policy Correction Helps Weaker Models Catch Up Where Imitation Fails | Zhou Yu; Bin Bi; Shiva Kumar Pentyala; Shubham Mehrotra; Sougata Chaudhuri; Shilpa Bhagavath; Zeyuan Chen; Ran Xu; Phil Mui; James Zhu; Sitaram Asur | 2026 | arXiv | 2609.09134 | ADOPTED_NORMATIVE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-002 | COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization | Pingchen Lu; Xiangyi Wang; Xiang Li; Jie Mao; Zikun Qu; Junfeng Luo; Yao Shu; Bryan Kian Hsiang Low; Zhongxiang Dai | 2026 | arXiv | 2609.11682 | ADOPTED_NORMATIVE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-003 | Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents | Ruiqing Yue; Yu Cui; Zhuoyu Sun; Sicheng Pan; Xianhong Xue; Tingyu Li; Ting Li; Wenzhuo Zhu; Yi Chen; Yifei Liu; Baohan Huang; Zhe Cui; Haibin Zhang; Cong Zuo | 2026 | arXiv | 2609.11677 | ADOPTED_NORMATIVE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-004 | ExecCritic: Learn to Test, Test to Improve for Coding Agents | Leitian Tao; Baolin Peng; Haorui Wang; Hang Wang; Hao Cheng; Wenlin Yao; Qianhui Wu; Tao Ge; Sharon Li; Jianfeng Gao | 2026 | arXiv | 2609.09133 | ADOPTED_NORMATIVE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-005 | Accelerating Language Model Workflows with Prompt Choreography | TJ Bai; Jason Eisner | 2026 | Transactions of the Association for Computational Linguistics | 2026.tacl-1.13; DOI:10.1162/tacl.a.643 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-006 | Adaptive Influence Graphs for Failure Attribution in Multi-Agent Systems | Yarden Bakish; Amir Dudai; Roy Ganz; Oren Nuriel; Elad Ben Avraham; Mor Shpigel Nacson; Ron Litman | 2026 | arXiv | 2608.24361 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-007 | AgentAbstain: Do LLM Agents Know When Not to Act? | Xun Liu; Yi Evie Zhang; Vira Kasprova; Parisa Rabbani; Pardis Sadat Zahraei; Tianyu Zhang; Ali Ebrahimpour-Boroojeny; Varun Chandrasekaran | 2026 | arXiv | 2607.10059 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-008 | When Agentic Executions Fail: Detecting and Localizing Runtime Faults from Telemetry | Chenkai Zhang; Yiran Li; Yifang Tian; Michalis Bachras; Hans-Arno Jacobsen | 2026 | arXiv | 2608.14680 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-009 | AgentDebugX: An Open-Source Toolkit for Failure Observability, Attribution, and Recovery in LLM Agents | Kunlun Zhu; Xuyan Ye; Zhiguang Han; Yuchen Zhao; Bingxuan Li; Weijia Zhang; Muxin Tian; Xiangru Tang; Pan Lu; James Zou; Jiaxuan You; Heng Ji | 2026 | arXiv | 2607.18754 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-010 | AgentGrad: Intervention-guided Prompt Optimization for Multi Agent Systems | Jaewon Chu; Jinwoo Seo; Jaewon Cho; Jeehye Na; Yunyang Xiong; Youngdae Kim; Hyunwoo J. Kim | 2026 | arXiv | 2609.08572 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-011 | AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems? | Guibin Zhang; Junhao Wang; Junjie Chen; Wangchunshu Zhou; Kun Wang; Shuicheng Yan | 2026 | ICLR 2026 | 2509.03312 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-012 | ARISE-RL: Agentic Rubric-Grounded Iterative Self-Evolution with Reinforcement Learning | Fanrui Zhang; Ruixue Ding; Qiang Zhang; Xi Chen; Boli Chen; Shihang Wang; Qiuchen Wang; Hongmin Zhan; Jinxin Bian; Xingchao Li; Peijin Zheng; Hao Cheng; Pengjun Xie; Kaipeng Zhang; Jiawei Liu; Zheng-Jun Zha | 2026 | arXiv | 2609.01058 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-013 | At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent | David Dylan; Aoife Brennan; Cian Murphy; Niamh O'Sullivan; Conor Kelly; Saoirse Walsh | 2026 | arXiv | 2609.04217 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-014 | AutoTraceGT | — | — | — | — | ADOPTED_BENCHMARK | UNRESOLVED | LOW |
| ARSO-LIT-015 | Calibrate-Then-Act: Cost-Aware Exploration in LLM Agents | Wenxuan Ding; Nicholas Tomlin; Greg Durrett | 2026 | arXiv | 2602.16699 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-016 | CausalFlow: Causal Attribution and Counterfactual Repair for LLM Agent Failures | Akash Bonagiri; Devang Borkar; Gerard Janno Anderias; Setareh Rafatirad; Houman Homayoun | 2026 | arXiv | 2605.25338 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-017 | DCFA | — | — | — | — | ADOPTED_BENCHMARK | UNRESOLVED | LOW |
| ARSO-LIT-018 | Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows | Bochao Feng; Jianjiang Li; Haojie Wang; Lin Qiao; Yinghui Li; Yukun Yan; Jidong Zhai | 2026 | arXiv | 2609.10964 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-019 | Diagnosing with Insights: Structured Analysis of Agent Failures via Behavioral Abstractions | — | 2026 | Microsoft Research preprint | — | ADOPTED_BENCHMARK | VERIFIED_SECONDARY | MEDIUM |
| ARSO-LIT-020 | Do We Always Need Query-Level Workflows? Rethinking Agentic Workflow Generation for Multi-Agent Systems | Zixu Wang; Bingbing Xu; Yige Yuan; Huawei Shen; Xueqi Cheng | 2026 | Findings of ACL 2026 | 2026.findings-acl.254; DOI:10.18653/v1/2026.findings-acl.254 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-021 | Agent Memory Is a Surface for Endogenous Authorization Laundering | Tommaso Cerruti; Mika Okamoto; Ansel Kaplan Erol | 2026 | arXiv | 2609.01836 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-022 | EDGE: Error Dependency Graph-Guided Multi-Error Attribution in Multi-Agent LLM Systems | Jun Hou; Priya Pitre; Yi Fang; Xuan Wang | 2026 | arXiv | 2609.01360 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-023 | Towards Self-Improving Error Diagnosis in Multi-Agent Systems | Jiazheng Li; Emine Yilmaz; Bei Chen; Thu Le | 2026 | Findings of ACL 2026 | 2026.findings-acl.98; DOI:10.18653/v1/2026.findings-acl.98 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-024 | Escaping the Echo Trap: On Credit Assignment Failure in Multi-turn LLM Self-Reflection | Linxuan Du; Guangquan Xue; Xiaobo Liang; Qipeng Huang; Yuyang Ding; Xinyu Shi; Zhang Yijun; Ji Qi; Wenpeng Zhu; Juntao Li; Min Zhang | 2026 | ACL 2026 | 2026.acl-long.1636; DOI:10.18653/v1/2026.acl-long.1636 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-025 | F2R | — | — | — | — | ADOPTED_BENCHMARK | UNRESOLVED | LOW |
| ARSO-LIT-026 | From Rollouts to Recipes: Self-Contained Post-Training for LLMs | Yifei Li; Lingling Zhang; Muye Huang; Zihan Ma; Jiashuai Liu; Jun Liu | 2026 | arXiv | 2609.01422 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-027 | HarnessOpt-Bench | Varun Ursekar; Apaar Shanker; Yash Maurya; Shehab Yasser; Vijay S. Kalmath; Veronica Chatrath; Yuan Xue | 2026 | arXiv | 2608.06301 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-028 | How Fast Do Agents Rot? An Empirical Study of Long-Horizon Degradation in LLM Agents for Production Decision-Making | Shubhra Mittal; Gaurav Naresh Mittal | 2026 | Journal of Intelligent Decision Making and Information Science | — | ADOPTED_BENCHMARK | VERIFIED_SECONDARY | MEDIUM |
| ARSO-LIT-029 | Large-language-model-driven adaptive search space definition for autonomous closed-loop materials exploration | Yuma Iwasaki; Ryo Toyama; Ryo Tamura; Shoichi Matsuda; Yuya Sakuraba; Masato Kotsugi; Yasuhiko Igarashi; Keitaro Sodeyama | 2026 | Communications Materials 7, Article 202 | s43246-026-01304-9 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-030 | LLM-as-a-Judge Is Not an Oracle | — | — | — | — | ADOPTED_BENCHMARK | UNRESOLVED | LOW |
| ARSO-LIT-031 | LongRCA Bench: Diagnosing Responsible Roles and Root Causes in Long-Horizon Agent Failures | Yunfei Zhang; Boyu Feng; Changhua Pei; Zexin Wang; Zhihuang Peng; Xinlong Liu; Hengyue Jiang; Difeng Ma; Jiayi Zhang; Yongzhou Yao; Yanan Zhao; Fei Sun; Yintong Huo; Zhaoyang Liu; Jingjing Li; Gaogang Xie; Dan Pei | 2026 | arXiv | 2608.15242 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-032 | Monitoring Web Agents Without Internal Signals: Observable Trajectories and Key-Step Supervision | Sitong Pan; Yipeng Shen; Yilin Lu; Caiwen Ding; Lu Cheng; Qianwen Wang | 2026 | arXiv | 2609.02057 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-033 | Naive Prompt Optimization: Rethinking the Need for Complex Prompt Search | Yuan Chang; Xiaoqi Chen | 2026 | arXiv | 2608.27266 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-034 | OPT-BENCH: Evaluating the Iterative Self-Optimization of LLM Agents in Large-Scale Search Spaces | Xiaozhe Li; Jixuan Chen; Xinyu Fang; Shengyuan Ding; Haodong Duan; Qingwen Liu; Kai Chen | 2026 | Findings of ACL 2026 | 2026.findings-acl.1417; DOI:10.18653/v1/2026.findings-acl.1417 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-035 | PROTEA: Offline Evaluation and Iterative Refinement for Multi-Agent LLM Workflows | Kazuki Kawamura; Satoshi Waki; Kei Tateno | 2026 | ACL 2026 System Demonstrations | 2026.acl-demo.3; DOI:10.18653/v1/2026.acl-demo.3 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-036 | Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems | Mengzhuo Chen; Junjie Wang; Fangwen Mu; Yawen Wang; Zhe Liu; Huanxiang Feng; Qing Wang | 2026 | ACL 2026 | 2026.acl-long.912; DOI:10.18653/v1/2026.acl-long.912 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-037 | TRUCE | — | — | — | — | ADOPTED_BENCHMARK | UNRESOLVED | LOW |
| ARSO-LIT-038 | What LLM Trading Agents Actually Do in Production: A Six-Month, Population-Scale Record from Two Fleets | T. J. Barton; Chris Constantakis; Patti Hauseman; Annie Mous; Alaska Hoffman; Brian Bergeron; Hunter Goodreau | 2026 | arXiv | 2609.05663 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-039 | Where Does Harness-Optimization Value Live? Localized Gains and the Budget-Splitting Trap in Self-Evolving LLM Agents | Michael Nguyen; Wei Chen Tan; Nurul Aisyah Hassan; Arvind Raman; Li Hua Lim; Ahmad Faiz Razak | 2026 | arXiv | 2609.02889 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-040 | τ^τ-Bench: An Environment for End-To-End, Realistic Agent Construction | Quan Shi; Keshav Dhandhania; Karthik Narasimhan; Victor Barres | 2026 | arXiv | 2609.04611 | ADOPTED_BENCHMARK | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-041 | Natural-Language Workflows Are Not Software Yet: Artifact-Driven Compilation for Reliable Agent Execution | Xiangzhe Xu; Hanxi Guo; Guangyu Shen; Siyuan Cheng; Xiangyu Zhang | 2026 | arXiv | 2608.21341 | ENGINEERING_PROFILE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-042 | Control–Data Flow Separation: Stable Prompt Optimization in Multi-Agent LLMs | Wentao Zhang; Syed Shariyar Murtaza; Junaid Ahmad Bhatti; Utkarsh Soni; Yifan Nie; Eugene Wen; Yuntian Deng | 2026 | Findings of EMNLP 2026 | 2609.00621 | ENGINEERING_PROFILE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-043 | Automated Design of Agentic Systems | Shengran Hu; Cong Lu; Jeff Clune | 2025 | ICLR 2025 | 2408.08435 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-044 | AutoDSL: Automated Domain-Specific Language Design for Structural Representation of Procedures with Constraints | Yu-Zhe Shi; Haofei Hou; Zhangqian Bi; Fanxu Meng; Xiang Wei; Lecheng Ruan; Qining Wang | 2024 | ACL 2024 | 2024.acl-long.659; DOI:10.18653/v1/2024.acl-long.659 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-045 | Automatic Prompt Optimization with “Gradient Descent” and Beam Search | Reid Pryzant; Dan Iter; Jerry Li; Yin Lee; Chenguang Zhu; Michael Zeng | 2023 | EMNLP 2023 | 2023.emnlp-main.494; DOI:10.18653/v1/2023.emnlp-main.494 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-046 | AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces | Sungho Park; Wonjoong Kim; Rongyuan Tan; Jue Zhang; Wook-Shin Han; Pengfei Gao; Chanyoung Park; Yongqiang Yao; Rao Fu; Elsie Nallipogu; Qingwei Lin; Saravan Rajmohan; Dongmei Zhang | 2026 | arXiv / Microsoft Research | — | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-047 | CADET: Debugging and Fixing Misconfigurations using Counterfactual Reasoning | — | — | — | — | CORE_BASELINE | UNRESOLVED | LOW |
| ARSO-LIT-048 | Contrastive Reflection for Iterative Prompt Optimization | Derek Koh; Jinghui Mo; Benjamin H. Le; Jiening Zhan; Baofen Zheng; Kevin Bevis; Nathaniel C. Owen; Lauren Elizabeth Charney; Wenqiong Liu; Jingwei Wu | 2026 | arXiv | 2606.30840 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-049 | DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines | Omar Khattab; Arnav Singhvi; Paridhi Maheshwari; Zhiyuan Zhang; Keshav Santhanam; Sri Vardhamanan; Saiful Haq; Ashutosh Sharma; Thomas T. Joshi; Hanna Moazam; Heather Miller; Matei Zaharia; Christopher Potts | 2023 | arXiv | 2310.03714 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-050 | Connecting Large Language Models with Evolutionary Algorithms Yields Powerful Prompt Optimizers | Qingyan Guo; Rui Wang; Junliang Guo; Bei Li; Kaitao Song; Xu Tan; Guoqing Liu; Jiang Bian; Yujiu Yang | 2024 | ICLR 2024 | 2309.08532 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-051 | Expert-level Protocol Translation for Self-Driving Labs | Yu-Zhe Shi; Fanxu Meng; Haofei Hou; Zhangqian Bi; Qiao Xu; Lecheng Ruan; Qining Wang | 2024 | NeurIPS 2024 | 10.52202/079017-1506 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-052 | FLARE: Few-shot Learning-based Adaptive Reflective Engine | Dhanasekar Sundararaman; Bharat Gandhi; Aashna Garg; Minjie Li | 2026 | Microsoft Research / preprint | — | CORE_BASELINE | VERIFIED_PDF | MEDIUM |
| ARSO-LIT-053 | GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning | Lakshya A Agrawal; Shangyin Tan; Dilara Soylu; Noah Ziems; Rishi Khare; Krista Opsahl-Ong; Arnav Singhvi; Herumb Shandilya; Michael J Ryan; Meng Jiang; Christopher Potts; Koushik Sen; Alexandros G. Dimakis; Ion Stoica; Dan Klein; Matei Zaharia; Omar Khattab | 2026 | ICLR 2026 | 2507.19457 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-054 | GPTSwarm | — | — | — | — | CORE_BASELINE | UNRESOLVED | LOW |
| ARSO-LIT-055 | Large Language Models Are Human-Level Prompt Engineers | Yongchao Zhou; Andrei Ioan Muresanu; Ziwen Han; Keiran Paster; Silviu Pitis; Harris Chan; Jimmy Ba | 2022 | arXiv | 2211.01910 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-056 | Large Language Models as Optimizers | Chengrun Yang; Xuezhi Wang; Yifeng Lu; Hanxiao Liu; Quoc V. Le; Denny Zhou; Xinyun Chen | 2023 | arXiv | 2309.03409 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-057 | LLM-AutoDiff: Auto-Differentiate Any LLM Workflow | Li Yin; Zhangyang Wang | 2025 | arXiv | 2501.16673 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-058 | MLIR: Scaling Compiler Infrastructure for Domain Specific Computation | Chris Lattner; Mehdi Amini; Uday Bondhugula; Albert Cohen; Andy Davis; Jacques Arnaud Pienaar; River Riddle; Tatiana Shpeisman; Nicolas Vasilache; Oleksandr Zinenko | 2021 | CGO 2021 | 10.1109/CGO51591.2021.9370308 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-059 | Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs | Krista Opsahl-Ong; Michael J Ryan; Josh Purtell; David Broman; Christopher Potts; Matei Zaharia; Omar Khattab | 2024 | EMNLP 2024 | 2024.emnlp-main.525; DOI:10.18653/v1/2024.emnlp-main.525 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-060 | p1: Better Prompt Optimization with Fewer Prompts | Zhaolin Gao; Yu (Sid) Wang; Bo Liu; Thorsten Joachims; Kianté Brantley; Wen Sun | 2026 | arXiv | 2604.08801 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-061 | Prompt Engineering a Prompt Engineer | Qinyuan Ye; Mohamed Ahmed; Reid Pryzant; Fereshte Khani | 2024 | Findings of ACL 2024 | 2311.05661 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-062 | PromptAgent: Strategic Planning with Language Models Enables Expert-level Prompt Optimization | Xinyuan Wang; Chenxi Li; Zhen Wang; Fan Bai; Haotian Luo; Jiayou Zhang; Nebojsa Jojic; Eric P. Xing; Zhiting Hu | 2024 | ICLR 2024 | 2310.16427 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-063 | Promptbreeder: Self-Referential Self-Improvement via Prompt Evolution | Chrisantha Fernando; Dylan Sunil Banarse; Henryk Michalewski; Simon Osindero; Tim Rocktäschel | 2024 | ICML 2024 (PMLR 235) | — | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-064 | ReEvo: Large Language Models as Hyper-Heuristics with Reflective Evolution | Haoran Ye; Jiarui Wang; Zhiguang Cao; Federico Berto; Chuanbo Hua; Haeyeon Kim; Jinkyoo Park; Guojie Song | 2024 | arXiv | 2402.01145 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-065 | Reflection in the Dark: Exposing and Escaping the Black Box in Reflective Prompt Optimization | Shiyan Liu; Qifeng Xia; Qiyun Xia; Yisheng Liu; Xinyu Yu; Rui Qu | 2026 | arXiv | 2603.18388 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-066 | Reflective Prompt Tuning through Language Model Function-Calling | Farima Fatahi Bayat; Moin Aminnaseri; Pouya Pezeshkpour; Estevam Hruschka | 2026 | arXiv | 2605.21781 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-067 | Reflexion: Language Agents with Verbal Reinforcement Learning | Noah Shinn; Federico Cassano; Ashwin Gopinath; Karthik Narasimhan; Shunyu Yao | 2023 | NeurIPS 2023 | 2303.11366 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-068 | RIDER: Evolutionary Prompt Optimization with Adaptive Operator Selection for Software Engineering | Daglar Dragomirov; Nikita Kulin; Sergey Muravyov; Ilya Makarov; Daniil Sukhorukov; Mikhail Mozikov | 2026 | preprint | — | CORE_BASELINE | VERIFIED_PDF | MEDIUM |
| ARSO-LIT-069 | Self-Refine: Iterative Refinement with Self-Feedback | Aman Madaan; Niket Tandon; Prakhar Gupta; Skyler Hallinan; Luyu Gao; Sarah Wiegreffe; Uri Alon; Nouha Dziri; Shrimai Prabhumoye; Yiming Yang; Sean Welleck; Bodhisattwa Prasad Majumder; Shashank Gupta; Amir Yazdanbakhsh; Peter Clark | 2023 | NeurIPS 2023 | — | CORE_BASELINE | VERIFIED_SECONDARY | MEDIUM |
| ARSO-LIT-070 | TextGrad: Automatic “Differentiation” via Text | — | — | — | — | CORE_BASELINE | UNRESOLVED | LOW |
| ARSO-LIT-071 | Trace is the Next AutoDiff: Generative Optimization with Rich Feedback, Execution Traces, and LLMs | Ching-An Cheng; Allen Nie; Adith Swaminathan | 2024 | NeurIPS 2024 Expo / arXiv | 2406.16218 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-072 | Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems | Shaokun Zhang; Ming Yin; Jieyu Zhang; Jiale Liu; Zhiguang Han; Jingyang Zhang; Beibin Li; Chi Wang; Huazheng Wang; Yiran Chen; Qingyun Wu | 2025 | ICML 2025 (PMLR 267) | 2505.00212 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-073 | Why Do Multi-Agent LLM Systems Fail? | Mert Cemri; Melissa Z. Pan; Shuyi Yang; Lakshya A. Agrawal; Bhavya Chopra; Rishabh Tiwari; Kurt Keutzer; Aditya Parameswaran; Dan Klein; Kannan Ramchandran; Matei Zaharia; Joseph E. Gonzalez; Ion Stoica | 2025 | NeurIPS 2025 | 2503.13657 | CORE_BASELINE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-074 | Cross-Domain Transfer via Semantic Skill Imitation | Karl Pertsch; Ruta Desai; Vikash Kumar; Franziska Meier; Joseph J. Lim; Dhruv Batra; Akshara Rai | 2022 | CoRL 2022 | 2212.07407 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-075 | Does Your Agent’s Memory Survive a Model Upgrade? | — | — | — | — | POST_CORE | UNRESOLVED | LOW |
| ARSO-LIT-076 | Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory | Mirac Suzgun; Mert Yuksekgonul; Federico Bianchi; Dan Jurafsky; James Zou | 2026 | EACL 2026 | 2026.eacl-long.333; DOI:10.18653/v1/2026.eacl-long.333 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-077 | Forgetting Without Restarting: Execution-State Unlearning for Stateful LLM Agents | Chao Yao; Yangbo Wei; Zhen Huang; Junhong Qian; Chenle Chen; Shaoqiang Lu; Chen Wu; Lei He | 2026 | arXiv | 2609.04875 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-078 | Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents | Susheel Suresh; Hazel Mak; Sahil Bhatnagar; Chhaya Methani; Alejandro Gutierrez Munoz | 2026 | arXiv | 2609.11060 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-079 | MASkills: Continual Skills Optimization for Multi-Agent LLM Systems | Huaiyuan Yao; Xiaoou Liu; Charles Fleming; Tianlong Chen; Hua Wei | 2026 | Findings of EMNLP 2026 | 2609.02094 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-080 | MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging | Junxi Wang; Te Sun; Jiayi Zhu; Chen Zhang; Siyuan Li; Xuyang Liu; Zichen Wen; Xiaobing Tu; Jinkui Ren; Xiantao Zhang; Ziqi Yuan; Linfeng Zhang | 2026 | arXiv | 2609.08273 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-081 | Procedural Graphs: Self-Evolving Execution Structures for LLM Agents | Yuxing Lu; Yicheng Chen; Shanchan Wu; Sercan Ö. Arık | 2026 | arXiv | 2609.09153 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-082 | SE-GoS: Self-Evolving Graph-of-Skills for Skill Library at Scale | Dawei Fu; Cheng Jiang; Sitian Qian; Huainan Wang; Zhongkai Hao | 2026 | arXiv | 2609.08228 | POST_CORE | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-083 | Benchmarking Biomedical Foundation Models | — | — | — | — | EXTERNAL_VALIDATION | UNRESOLVED | LOW |
| ARSO-LIT-084 | Bioinfoysis | — | — | — | — | EXTERNAL_VALIDATION | UNRESOLVED | LOW |
| ARSO-LIT-085 | CRISPR RT–qPCR Artifact | — | — | — | — | EXTERNAL_VALIDATION | UNRESOLVED | LOW |
| ARSO-LIT-086 | Improving Portability of Knowledge-Based Planning Using an LLM-Driven Plan Refinement Framework in Lung Radiotherapy | — | — | — | — | EXTERNAL_VALIDATION | UNRESOLVED | LOW |
| ARSO-LIT-087 | MoChiAgent / Mother-Child AI Agent | — | — | — | — | EXTERNAL_VALIDATION | UNRESOLVED | LOW |
| ARSO-LIT-088 | PlanningCopilot: An Agentic Framework Integrating ESAPI Modules for Autonomous Treatment Planning in Lung Radiotherapy | — | — | — | — | EXTERNAL_VALIDATION | UNRESOLVED | LOW |
| ARSO-LIT-089 | AgentFactory | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-090 | ARCHITECT | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-091 | Aspire: Can Models Self-Evolve from Vague Goals? | Yuhao Wu; Jingyuan Zhang; Jiajun Shi; Yuxuan Zhang; Xinping Lei; Junting Zhou; Zexuan Wang; Yuchen Wu; Huan Zhou; Duo Wang; Yinzhu Piao; Yongchang Peng; Yunfeng Shi; Jin Chen; Zuo Wang; Jinkai Liu; Jiaheng Liu; Wenxuan Zhang; Shen Yan; Wenhao Huang; Ge Zhang | 2026 | arXiv | 2608.31111 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-092 | AutoSciRub — Learning to Evaluate Before Improving | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-093 | CAPO: Constraint-Aware Prompt Optimization for LLM Agents | Victor Ye Dong; Reid Pryzant; Yi Liu; Jian Jiao | 2026 | arXiv | 2608.16068 | REFERENCE_ONLY | LIKELY_RESOLVED | HIGH |
| ARSO-LIT-094 | CoolPrompt: Automatic Prompt Optimization Framework for Large Language Models | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-095 | DOCSCHISEL: Adaptive Tool Documentation Optimization Framework for LLM Agents | You Lu; Kun Zhang; Bihuan Chen; Xin Peng | 2026 | arXiv | 2608.10037 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-096 | Don’t Generate, Classify! | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-097 | Emergent Misalignment and Deception in Multi-Agent Research Swarms | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-098 | EvoX: Meta-Evolution for Automated Discovery | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-099 | ExTS | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-100 | FlowBot | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-101 | FlowScout: From Execution Feedback to Reliable Tool-Using Agent Workflows | Shuo Hao; You Lu; Bihuan Chen; Xin Peng | 2026 | arXiv | 2608.10039 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-102 | FusionFlow: Enabling Deep Structural Exploration for Automated Agentic Workflow Generation | Xiang Wang; Zongtao Yang; Zhuojian Hong; Shuhao Zhang; Wei Wei | 2026 | ACL 2026 | 2026.acl-long.1278; DOI:10.18653/v1/2026.acl-long.1278 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-103 | GOLLuM | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-104 | Harness-of-Harness: Multi-Day Autonomous Software Development with Continual Improvement | Haoyang Yan; Min-le Su; Hangfan Zhang; Zhanhao Li; Chen Zhang; Shao Zhang; Yang Chen; Lei Bai; Shuyue Hu | 2026 | arXiv | 2609.01481 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-105 | JIT-Agent | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-106 | JTPRO: A Joint Tool–Prompt Reflective Optimization Framework for Language Agents | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-107 | Learning from Contrastive Prompts: An Automated Prompt Optimization Framework | Mingqi Li; Karan Aggarwal; Yong Xie; Aitzaz Ahmad; Stephen Lau | 2026 | Findings of ACL 2026 | 2026.findings-acl.9; DOI:10.18653/v1/2026.findings-acl.9 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-108 | MAPRO | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-109 | On the Limit of Language Models as Planning Formalizers | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-110 | OPERA | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-111 | PlanFence | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-112 | PRompt Optimization in Multi-Step Tasks: Integrating Human Feedback and Heuristic-based Sampling | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-113 | PromptWizard: Optimizing Prompts via Task-Aware, Feedback-Driven Self-Evolution | Eshaan Agarwal; Raghav Magazine; Joykirat Singh; Vivek Dani; Tanuja Ganu; Akshay Nambi | 2025 | Findings of ACL 2025 | 2025.findings-acl.1025; DOI:10.18653/v1/2025.findings-acl.1025 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-114 | RE-GPS: Reflective Evolutionary Gradient Prompting System for Large Language Models | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-115 | ReASearch | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-116 | RLMOpt: Adaptive Prompt Optimization via Recursive Language Models | Subhash Bangalore Satheesha; Nirvik Pande; Deepthi Duddempudi; Bharath Dandala | 2026 | arXiv | 2608.10471 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-117 | Robust Prompt Optimization for Large Language Models Against Distribution Shifts | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-118 | Symbolic Prompt Program Search: A Structure-Aware Approach to Efficient Compile-Time Prompt Optimization | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-119 | TPGO | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-120 | TraceCompiler: Skill-Guided Mining and Compilation of LLM Agent Traces into Mostly Deterministic Workflows | Salma El Yadouni; Guanyi Li | 2026 | arXiv | 2608.02680 | REFERENCE_ONLY | VERIFIED_PRIMARY | HIGH |
| ARSO-LIT-121 | Unleashing the Potential of Large Language Models as Prompt Optimizers: Analogical Analysis with Gradient-based Model Optimizers | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |
| ARSO-LIT-122 | WHALE | — | — | — | — | REFERENCE_ONLY | UNRESOLVED | LOW |

## 3. High-impact V2.2.5 traceability remains unchanged

The bibliographic normalization does **not** change the V2.2.5 scientific decisions. In particular:

- `Ecdysis` remains the strongest direct literature pressure behind **N25 — Instance Failure ≠ Systemic Defect**.
- `Co-Evolving Harnesses and Models` remains a direct pressure behind **N26 — Local Component Gain ≠ Whole-System Validated Gain**.
- `ExecCritic` remains a direct pressure behind **N27 — Optimization Feedback ≠ Claim-Supporting Validation Evidence** and anti-self-confirmation / ACG-1 hardening.
- `COBRA-Skills` remains a direct pressure behind **N28 — Candidate Generation ≠ Evaluation Allocation**.
- `AgentGrad`, `EDGE`, `NPO`, `MA-Evolve`, `SCALE`, `How Fast Do Agents Rot?`, and related works remain benchmark/scientific-hardening evidence rather than new Scientific Core claims.

## 4. Verification queue policy

Unresolved records are retained rather than deleted because they are part of ARSO's historical literature trail. They should be resolved by recovering the exact Daily Brief / Monthly Audit source entry, then checking the primary paper page (arXiv/OpenReview/ACL/PMLR/publisher).

Before public release or manuscript citation, records with `LOW` completeness or `UNRESOLVED` / `LIKELY_RESOLVED` status should not be cited from the registry as if their bibliographic identity were certain.

## 5. Change-control rule

Metadata normalization does not itself change a work's ARSO disposition. A literature item can only move between `REFERENCE_ONLY`, `CORE_BASELINE`, `ADOPTED_BENCHMARK`, `ADOPTED_NORMATIVE`, `ENGINEERING_PROFILE`, `POST_CORE`, or `EXTERNAL_VALIDATION` through an explicit ARSO literature/revision decision.

> **Registry principle:** Bibliographic certainty, scientific relevance, and normative adoption are three different dimensions.