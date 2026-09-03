from __future__ import annotations
from typing import Protocol
from di_contracts.core.models import ExactObjectRef, ObjectRef
from di_contracts.b07.models import BranchHeadPointer

class DesignBranchRuntime(Protocol):
    def get_head(self, branch_ref: ObjectRef) -> BranchHeadPointer: ...
    def compare_and_swap_head(self, *, branch_ref: ObjectRef, expected_head_ref: ObjectRef, expected_concurrency_version: int, new_head_ref: ObjectRef) -> BranchHeadPointer: ...

class KnowledgeSnapshotService(Protocol):
    def validate_snapshot(self, snapshot_ref: ObjectRef) -> None: ...
