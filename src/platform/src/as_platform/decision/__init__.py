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

"""The decision package: the pure routing policy of the kernel.

See ADR-0002 (one process per use case, kernel stays pure) and lld.md §2, §3.
"""

from __future__ import annotations

from .decide import (
    REASON_MATCH_BLOCK,
    REASON_MATCH_FORWARD,
    REASON_MATCH_TRANSLATE,
    REASON_NO_MATCH,
    Decision,
    DecisionAction,
    DecisionRequest,
    decide,
)
from .rules import Action, Rule, RuleSet, normalize_number

__all__: list[str] = [
    "REASON_MATCH_BLOCK",
    "REASON_MATCH_FORWARD",
    "REASON_MATCH_TRANSLATE",
    "REASON_NO_MATCH",
    "Action",
    "Decision",
    "DecisionAction",
    "DecisionRequest",
    "Rule",
    "RuleSet",
    "decide",
    "normalize_number",
]
