from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from design_intelligence.contracts.core.hashing import canonical_json_bytes


ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests" / "cross_language" / "fixtures.json"
NODE_SOURCE = ROOT / "tests" / "cross_language" / "node"


def test_python_and_node_rfc8785_outputs_are_byte_identical(tmp_path: Path) -> None:
    assert shutil.which("node") is not None, "Node.js is required for the P1 cross-language gate"
    assert shutil.which("npm") is not None, "npm is required for the P1 cross-language gate"

    lock_file = NODE_SOURCE / "package-lock.json"
    assert lock_file.is_file(), "package-lock.json must be committed for the frozen Node oracle"

    node_dir = tmp_path / "node"
    shutil.copytree(NODE_SOURCE, node_dir)
    subprocess.run(
        ["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
        cwd=node_dir,
        check=True,
        capture_output=True,
        text=True,
    )

    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    for fixture in fixtures:
        payload = fixture["value"]
        input_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        completed = subprocess.run(
            ["node", "canonicalize.mjs"],
            cwd=node_dir,
            input=input_text,
            check=True,
            capture_output=True,
            text=True,
        )
        assert completed.stdout.encode("utf-8") == canonical_json_bytes(payload), fixture["name"]
