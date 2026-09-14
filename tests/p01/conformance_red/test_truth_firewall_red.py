import pytest

pytestmark = [
    pytest.mark.p01_red,
    pytest.mark.xfail(strict=True, reason="I1 scientific-integrity enforcement gate"),
]


def test_non_oracle_sealed_access_is_blocked() -> None:
    from arso.p01.runtime.integrity import TruthFirewall

    firewall = TruthFirewall()
    assert firewall.authorize(condition="NONE", purpose="SCIENTIFIC_AUDIT") is False
