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

"""Unit tests for active-call counting and M5 simulation."""

from __future__ import annotations

import pytest

from as_platform.runtime.active_calls import ActiveCallSource

pytestmark = pytest.mark.unit


def test_manual_counter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AS_M5_SIMULATED_ACTIVE_CALLS", raising=False)
    terminating = False
    source = ActiveCallSource(is_terminating=lambda: terminating, now=lambda: 0.0)
    source.increment(2)
    assert source.count() == 2
    source.decrement(1)
    assert source.count() == 1


def test_simulated_calls_drain_after_terminate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_M5_SIMULATED_ACTIVE_CALLS", "3")
    terminating = False
    clock = 0.0

    def now() -> float:
        return clock

    source = ActiveCallSource(is_terminating=lambda: terminating, now=now)
    assert source.count() == 3
    terminating = True
    assert source.count() == 3
    clock = 1.5
    assert source.count() == 2
