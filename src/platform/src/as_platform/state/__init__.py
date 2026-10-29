# Inhouse-IMS-AS — Copyright 2026 Dolan Shu <dolan.d.shu@gmail.com>, Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

"""The state package: the StateStore seam and its implementations.

Runtime state (sessions, dialogs, rate windows) lives outside the process, so
the process itself stays stateless and restartable. See ADR-0002 and ADR-0007.
"""

from __future__ import annotations

from .call_checkpoint import (
    CallStateCheckpoint,
    CallStateCheckpointRepository,
    CheckpointHeaderExtension,
    DialogLegCheckpoint,
)
from .in_memory import InMemoryStateStore
from .store import StateStore, build_key

__all__: list[str] = [
    "CallStateCheckpoint",
    "CallStateCheckpointRepository",
    "CheckpointHeaderExtension",
    "DialogLegCheckpoint",
    "InMemoryStateStore",
    "StateStore",
    "build_key",
]
