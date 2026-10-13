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

"""Unit tests for decision → SIP metrics bridge."""

from __future__ import annotations

import pytest

from as_platform.decision.decide import DecisionAction
from as_platform.sip.metrics_bridge import record_terminal_decision_response
from as_platform.telemetry.metrics import SIP_RESPONSES_TOTAL, CallMetrics, MetricsRegistry

pytestmark = pytest.mark.unit


def test_records_terminal_codes_only() -> None:
    registry = MetricsRegistry()
    metrics = CallMetrics(registry)
    record_terminal_decision_response(metrics, "translation", DecisionAction.DECLINE)
    record_terminal_decision_response(metrics, "translation", DecisionAction.FORWARD)
    points = [p for p in registry.snapshot() if p.name == SIP_RESPONSES_TOTAL]
    assert len(points) == 1
    assert points[0].labels["status_code"] == "603"
