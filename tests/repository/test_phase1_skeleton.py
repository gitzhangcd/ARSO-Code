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


def test_spec_checksums_match_manifest() -> None:
    checksum_file = ROOT / "specs" / "SPEC_SOURCE_CHECKSUMS.sha256"
    rows = [
        line.split(maxsplit=1)
        for line in checksum_file.read_text(encoding="utf-8").splitlines()
        if line
    ]
    for expected, relative_path in rows:
        payload = (ROOT / relative_path).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected


def test_candidate_baseline_is_preserved() -> None:
    assert (ROOT / "di_contracts_v1" / "pyproject.toml").is_file()
    policy = (ROOT / "BASELINE_POLICY.md").read_text(encoding="utf-8")
    assert "FREEZE CANDIDATE" in policy
    assert "不得作为规范权威" in policy
