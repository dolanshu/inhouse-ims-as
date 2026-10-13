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

"""Product decisions used by the first-edition scenarios."""

from __future__ import annotations

import pytest

from as_load.scenarios import scenario_by_id
from as_platform.decision.decide import DecisionAction, DecisionRequest, decide
from as_simulators.demo_rules import demo_rules
from as_translation.decision import translate_number

pytestmark = pytest.mark.unit


def test_demo_rules_match_the_first_edition_outcomes() -> None:
    """T1 rewrites, T4 is 404, T5 and F1 forward, F2 declines as 603."""
    rules, translations = demo_rules()
    cases = {
        "T1": DecisionAction.TRANSLATE,
        "T4": DecisionAction.NOT_FOUND,
        "T5": DecisionAction.FORWARD,
        "F1": DecisionAction.FORWARD,
        "F2": DecisionAction.DECLINE,
    }
    for scenario_id, action in cases.items():
        scenario = scenario_by_id(scenario_id)
        verdict = decide(
            DecisionRequest(
                call_id=scenario_id,
                calling_number=scenario.calling_user,
                called_number=scenario.called_user,
                received_at=0,
            ),
            rules,
        )
        assert verdict.action is action
    rewritten = translate_number("+8613800138000", translations[0])
    assert rewritten == "013800138000"
