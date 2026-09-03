# Phase 1 Contract Repository Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不实现 P0 contract type 的前提下，建立可验证、可提交、以 `specs/` 为唯一规范路径的 Contract Repository Skeleton。

**Architecture:** 保留现有 `di_contracts_v1` 作为只读 candidate baseline，新建标准 `src/design_intelligence` package、分层测试目录和生成物目录。通过 repository-level test 固化规范文件、目录结构、规范 checksum、旧路径清理以及“Phase 1 不得提前实现 P0”的边界。

**Tech Stack:** Python 3.12+、Pydantic v2（仅声明后续 contract runtime）、pytest、uv、Git、Markdown。

---

### Task 1：建立 Phase 1 repository contract 测试

**Files:**
- Create: `tests/repository/test_phase1_skeleton.py`

- [ ] **Step 1：先写会失败的 repository contract 测试**

```python
from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_SPECS = (
    "specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md",
    "specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt",
    "specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt",
    "specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt",
    "specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt",
    "specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt",
    "specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt",
)

REQUIRED_PACKAGES = (
    "src/design_intelligence/contracts/core/__init__.py",
    "src/design_intelligence/contracts/arso/__init__.py",
    "src/design_intelligence/contracts/infrastructure/__init__.py",
    "src/design_intelligence/contracts/b01/__init__.py",
    "src/design_intelligence/contracts/b02/__init__.py",
    "src/design_intelligence/contracts/b03/__init__.py",
    "src/design_intelligence/contracts/b04/__init__.py",
    "src/design_intelligence/contracts/b05/__init__.py",
    "src/design_intelligence/contracts/b06/__init__.py",
    "src/design_intelligence/contracts/b07/__init__.py",
    "src/design_intelligence/contracts/b08/__init__.py",
    "src/design_intelligence/registry/__init__.py",
    "src/design_intelligence/commands/__init__.py",
    "src/design_intelligence/events/__init__.py",
    "src/design_intelligence/protocols/__init__.py",
    "src/design_intelligence/resolution/__init__.py",
    "src/design_intelligence/errors/__init__.py",
)

AUDIT_DOCS = (
    "AGENTS.md",
    "SPEC_AUTHORITY.md",
    "IMPLEMENTATION_MANIFEST.md",
    "CONTRACT_GAP_REPORT.md",
    "SPEC_CONFLICTS.md",
)


def test_authoritative_specs_exist() -> None:
    assert all((ROOT / path).is_file() for path in REQUIRED_SPECS)


def test_target_package_skeleton_exists() -> None:
    assert all((ROOT / path).is_file() for path in REQUIRED_PACKAGES)


def test_audit_docs_use_specs_as_only_normative_path() -> None:
    for path in AUDIT_DOCS:
        text = (ROOT / path).read_text(encoding="utf-8")
        assert "reference_Pack" not in text


def test_phase1_does_not_implement_contract_types() -> None:
    source_root = ROOT / "src" / "design_intelligence"
    for path in source_root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "class " not in text
        assert "BaseModel" not in text


def test_spec_checksums_match_manifest() -> None:
    checksum_file = ROOT / "specs" / "SPEC_SOURCE_CHECKSUMS.sha256"
    rows = [line.split(maxsplit=1) for line in checksum_file.read_text(encoding="utf-8").splitlines() if line]
    for expected, relative_path in rows:
        payload = (ROOT / relative_path).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected


def test_candidate_baseline_is_preserved() -> None:
    assert (ROOT / "di_contracts_v1" / "pyproject.toml").is_file()
    policy = (ROOT / "BASELINE_POLICY.md").read_text(encoding="utf-8")
    assert "FREEZE CANDIDATE" in policy
    assert "不得作为规范权威" in policy
```

- [ ] **Step 2：运行测试并确认骨架相关测试失败**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with 'pytest>=8,<9' \
  python -m pytest -p no:cacheprovider tests/repository/test_phase1_skeleton.py -q
```

Expected: `test_authoritative_specs_exist` 通过；package skeleton、旧路径清理、checksum manifest、baseline policy 测试失败。

### Task 2：建立根级工程与 Git 治理文件

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `pyproject.toml`

- [ ] **Step 1：创建只包含必要规则的 `.gitignore`**

```gitignore
.DS_Store
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
dist/
build/
*.egg-info/
```

- [ ] **Step 2：创建根级 `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "design-intelligence-contracts"
version = "0.0.0"
description = "Design Intelligence V5.0 Exact V1 contract repository"
requires-python = ">=3.12"
dependencies = ["pydantic>=2.12,<3"]

[project.optional-dependencies]
test = ["pytest>=8,<9"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"

[tool.setuptools.packages.find]
where = ["src"]
```

- [ ] **Step 3：创建中文根级 README**

README 必须说明当前为 Phase 1、`specs/` 是唯一规范入口、`di_contracts_v1` 只是 candidate baseline、P0 尚未开始，并给出 repository test 命令。

### Task 3：同步 `specs/` 路径与阶段状态

**Files:**
- Modify: `AGENTS.md`
- Modify: `SPEC_AUTHORITY.md`
- Modify: `IMPLEMENTATION_MANIFEST.md`
- Modify: `CONTRACT_GAP_REPORT.md`
- Modify: `SPEC_CONFLICTS.md`

- [ ] **Step 1：把所有规范路径从 `reference_Pack/` 更新为 `specs/`**

要求：5 份文档中不得残留 `reference_Pack`。

- [ ] **Step 2：更新阶段状态**

```text
Phase 0: COMPLETE / REVIEWED
Phase 1: AUTHORIZED / IN PROGRESS
P0: NOT STARTED
```

- [ ] **Step 3：关闭已解决的路径歧义**

将 A-01 和 GAP-020 标记为 `RESOLVED`；保留历史记录，但不得继续计入 active blocker。

### Task 4：创建 Contract Repository Skeleton

**Files:**
- Create: `src/design_intelligence/__init__.py`
- Create: `src/design_intelligence/contracts/**/__init__.py`
- Create: `src/design_intelligence/{registry,commands,events,protocols,resolution,errors}/__init__.py`
- Create: `tests/{unit,schemas,registry,references,immutability,commands,events,protocols,conformance}/.gitkeep`
- Create: `tests/conformance/{cs_01_08,cs_09_16,cs_17_24,cs_25_32,ac}/.gitkeep`
- Create: `generated/json_schema/.gitkeep`

- [ ] **Step 1：创建 package marker**

每个 `__init__.py` 只能包含说明该 namespace 尚未进入实现阶段的 module docstring，例如：

```python
"""B01 contract namespace；Phase 1 只建立骨架，不定义 schema。"""
```

- [ ] **Step 2：创建测试和生成物目录 marker**

只创建 `.gitkeep`，不得创建虚假测试、schema 或生成物。

- [ ] **Step 3：运行 repository contract 测试**

Expected: package skeleton 测试通过；checksum 和 baseline policy 测试仍失败。

### Task 5：冻结规范 checksum 与 candidate baseline 边界

**Files:**
- Create: `specs/SPEC_SOURCE_CHECKSUMS.sha256`
- Create: `BASELINE_POLICY.md`

- [ ] **Step 1：写入当前 7 份规范的 SHA-256**

```text
d914947fb29e3161156be382679b071ba6ba419e6c47972833bc6b6ed19dd7d3  specs/00-CODE-FREEZE/DI_V5_Exact_V1_Schema_API_Contract_Freeze_Specification.md
930c24f776ae7faf64630d3dc991f7da9b6b0dede5e6203fcea434e9ec89e9d2  specs/01-AUTHORITY/Cross-Spec-Consistency-Freeze.txt
7e21f6566554eab5ede129d4d7b8d3999b86e7ee8a17ab50dcecc7221503701d  specs/01-AUTHORITY/Design-Intelligence-V5.0-Engineering-Specification-V1.0.txt
830207e6d429811bde313c0926f5d882d1491b2a6201ec825f1a51171ea6e327  specs/02-UPSTREAM/ARSO-Engineering-Specification-V2.2.1.txt
093d693c3272f2cf655d4b7252e500d3ededa04ac76a72836e94d47d7c47215b  specs/02-UPSTREAM/Design-Intelligence-V5.0-Application-Specification.txt
ad71cd0ae66ac9c2c56a5b09d8e93acb9f45b7ab0d8254f215f050cf4eb97d1b  specs/02-UPSTREAM/Design-Intelligence-x-ARSO-V2.2.1-Implementation-Blueprint.txt
1ae273ff4ec3c9396c267600662ee6dfdb419fe07b64b1726893b17093d522f2  specs/03-RESEARCH/ARSO-Research-Specification-V2.2.1.txt
```

- [ ] **Step 2：建立 baseline policy**

`BASELINE_POLICY.md` 必须明确：

```text
di_contracts_v1 = 只读 candidate baseline
不得作为规范权威
不得直接复制缺失的 B01/B02/ARSO contract
迁移必须经过对应 P0-P15 阶段的 test-first conformance 审计
```

- [ ] **Step 3：运行 repository contract 测试并确认全部通过**

Expected: `6 passed`。

### Task 6：完成 Phase 1 验证、审计与本地 Git 基线

**Files:**
- Create: `PHASE_1_SKELETON_AUDIT.md`
- Modify: `AGENTS.md`

- [ ] **Step 1：运行新的 repository test**

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with 'pytest>=8,<9' \
  python -m pytest -p no:cacheprovider tests/repository/test_phase1_skeleton.py -q
```

Expected: `6 passed`。

- [ ] **Step 2：复跑现有 candidate baseline test**

```bash
cd di_contracts_v1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. uv run --no-project \
  --with 'pytest>=8,<9' --with 'pydantic>=2.12,<3' \
  python -m pytest -p no:cacheprovider -q
```

Expected: `46 passed`。

- [ ] **Step 3：验证新 package 可导入且没有 contract class**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -c 'import design_intelligence'
rg -n '^class |BaseModel' src/design_intelligence
```

Expected: import exit 0；`rg` 不返回匹配。

- [ ] **Step 4：写入中文 Phase 1 audit，并将阶段标记为完成**

Audit 必须记录：规范 checksum、目录结构、repository test、legacy baseline test、无 P0 contract implementation、仍未解决的 SPEC_GAP，以及 `P0: NOT AUTHORIZED`。

- [ ] **Step 5：初始化本地 Git 并创建 Phase 1 基线提交**

```bash
git init -b main
git add .
git status --short
git commit -m "chore: establish contract repository skeleton"
```

Expected: 创建本地 `main` 分支和一个初始 baseline commit；不配置 remote，不 push。
