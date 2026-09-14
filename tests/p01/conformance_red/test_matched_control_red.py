import pytest

pytestmark = [
    pytest.mark.p01_red,
    pytest.mark.xfail(strict=True, reason="I1 scientific-integrity enforcement gate"),
]


def test_matched_control_mismatch_invalidates_block() -> None:
    from arso.p01.runtime.integrity import MatchedControlChecker

    checker = MatchedControlChecker()
    result = checker.check(("fingerprint-a", "fingerprint-b"))
    assert result.valid is False
