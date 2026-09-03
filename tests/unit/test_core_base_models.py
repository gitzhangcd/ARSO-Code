from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_core_base_module_exists() -> None:
    assert (ROOT / "src/design_intelligence/contracts/core/base.py").is_file()


def test_core_base_exports_expected_classes() -> None:
    from design_intelligence.contracts.core import base

    assert hasattr(base, "DIModel")
    assert hasattr(base, "FrozenDIModel")


def test_base_model_forbids_extra_fields() -> None:
    import pytest
    from pydantic import ValidationError
    from design_intelligence.contracts.core.base import DIModel

    class StrictProbe(DIModel):
        count: int

    with pytest.raises(ValidationError):
        StrictProbe(count=1, extra_field=True)


def test_base_model_uses_strict_validation() -> None:
    import pytest
    from pydantic import ValidationError
    from design_intelligence.contracts.core.base import DIModel

    class StrictProbe(DIModel):
        count: int

    with pytest.raises(ValidationError):
        StrictProbe(count="1")


def test_frozen_model_rejects_mutation() -> None:
    import pytest
    from pydantic import ValidationError
    from design_intelligence.contracts.core.base import FrozenDIModel

    class CanonicalProbe(FrozenDIModel):
        name: str

    probe = CanonicalProbe(name="alpha")
    with pytest.raises(ValidationError):
        probe.name = "beta"


def test_base_model_validates_default_values_strictly() -> None:
    import pytest
    from pydantic import ValidationError
    from design_intelligence.contracts.core.base import DIModel

    class DefaultProbe(DIModel):
        count: int = "1"

    with pytest.raises(ValidationError):
        DefaultProbe()
