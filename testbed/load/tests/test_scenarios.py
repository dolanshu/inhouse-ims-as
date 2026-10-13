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

"""Call-type selection for the load harness."""

from __future__ import annotations

import pytest

from as_load.scenarios import FIRST_EDITION, scenario_by_id, scenario_for_attempt

pytestmark = pytest.mark.unit


def test_first_edition_is_the_approved_set() -> None:
    """T1, T4, T5, F1 and F2 are the first edition. T2 and T3 stay out."""
    assert tuple(item.scenario_id for item in FIRST_EDITION) == ("T1", "T4", "T5", "F1", "F2")


def test_attempts_rotate_through_enabled_scenarios() -> None:
    """Each scheduled attempt takes the next enabled scenario."""
    enabled = ("T5", "T4")
    assert scenario_for_attempt(enabled, 0).scenario_id == "T5"  # type: ignore[union-attr]
    assert scenario_for_attempt(enabled, 1).scenario_id == "T4"  # type: ignore[union-attr]
    assert scenario_for_attempt(enabled, 2).scenario_id == "T5"  # type: ignore[union-attr]


def test_empty_selection_keeps_the_legacy_uri() -> None:
    """No scenario means the harness still sends its original load URI."""
    assert scenario_for_attempt((), 0) is None


def test_unknown_scenario_is_rejected() -> None:
    """A typo must not silently become a call."""
    with pytest.raises(ValueError, match="unknown call scenario"):
        scenario_by_id("T2")
