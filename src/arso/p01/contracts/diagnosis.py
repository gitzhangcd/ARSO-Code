"""Diagnosis-treatment contracts for ARSO P0.1."""

from design_intelligence.contracts.core import ContentHash

from .base import FrozenP01Model
from .enums import DiagnosisConditionType


class DiagnosisConditionSpec(FrozenP01Model):
    condition_id: str
    condition_type: DiagnosisConditionType
    template_ref: str
    materialization_policy_ref: str
    source_policy: str
    visibility_policy: str
    frozen_before_run: bool
    content_hash: ContentHash


class DiagnosisInjection(FrozenP01Model):
    injection_id: str
    trial_id: str
    condition: DiagnosisConditionType
    visible_payload: str | None
    visible_payload_hash: ContentHash | None
    materialization_method: str
    source_visibility: str
