from __future__ import annotations

from design_intelligence.contracts.core.hashing import canonical_json_bytes


def test_rfc8785_section_3_2_canonicalization_example() -> None:
    payload = {
        "numbers": [
            333333333.33333329,
            1e30,
            4.50,
            2e-3,
            0.000000000000000000000000001,
        ],
        "string": "\u20ac$\x0f\nA'B\"\\\\\"/",
        "literals": [None, True, False],
    }
    expected = '''{"literals":[null,true,false],"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],"string":"€$\\u000f\\nA'B\\"\\\\\\\\\\"/"}'''.encode(
        "utf-8"
    )
    assert canonical_json_bytes(payload) == expected
