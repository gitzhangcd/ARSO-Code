"""Fixture access port for ARSO P0.1."""

from typing import Protocol

from arso.p01.contracts.enums import SealedAccessPurpose
from arso.p01.contracts.fixture import PublicQualifiedFixture, SealedFixtureTruth


class FixtureProvider(Protocol):
    """Loads public fixture data and capability-gated sealed truth."""

    def load_public(self, fixture_ref: str) -> PublicQualifiedFixture:
        ...

    def load_sealed(
        self,
        fixture_ref: str,
        purpose: SealedAccessPurpose,
    ) -> SealedFixtureTruth:
        ...
