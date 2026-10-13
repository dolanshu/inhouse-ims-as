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

"""Outbound URI for the translation use case."""

from __future__ import annotations

import pytest

from as_platform.decision import Decision, DecisionAction
from as_translation.outbound import route_target

pytestmark = pytest.mark.unit


def test_translate_rewrites_the_user_onto_the_next_hop(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_SIP_NEXT_HOP", "ssbc-south.example")
    monkeypatch.setenv("AS_SIP_NEXT_HOP_PORT", "5060")
    monkeypatch.setenv(
        "AS_TRANSLATION_RULES_JSON",
        '[{"rule_id":"t1-plus86","prefix":"+86138","strip_prefix":"+86","add_prefix":"0"}]',
    )
    decision = Decision(
        action=DecisionAction.TRANSLATE,
        target="sip:uas@south",
        reason_code="MATCH_TRANSLATE",
        matched_rule_id="t1-plus86",
    )
    uri = route_target(decision, "+8613800138000", "udp")
    assert uri == "sip:013800138000@ssbc-south.example:5060"


def test_forward_keeps_the_called_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_SIP_NEXT_HOP", "ssbc-south.example")
    monkeypatch.delenv("AS_TRANSLATION_RULES_JSON", raising=False)
    decision = Decision(
        action=DecisionAction.FORWARD,
        target="sip:uas@south",
        reason_code="MATCH_FORWARD",
        matched_rule_id="t5-forward",
    )
    uri = route_target(decision, "+155500010001", "tcp")
    assert uri == "sip:+155500010001@ssbc-south.example:5060"


def test_tls_uses_the_tls_port(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_SIP_NEXT_HOP", "ssbc-south.example")
    monkeypatch.setenv("AS_SIP_NEXT_HOP_TLS_PORT", "5061")
    decision = Decision(
        action=DecisionAction.FORWARD,
        target="sip:uas@south",
        reason_code="MATCH_FORWARD",
        matched_rule_id="f1-allow",
    )
    uri = route_target(decision, "+155500020002", "tls")
    assert uri == "sips:+155500020002@ssbc-south.example:5061"


def test_decline_is_not_rewritten(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_SIP_NEXT_HOP", "ssbc-south.example")
    decision = Decision(
        action=DecisionAction.DECLINE,
        target=None,
        reason_code="MATCH_BLOCK",
        matched_rule_id="f2-block",
    )
    assert route_target(decision, "+155500030003", "udp") is None
