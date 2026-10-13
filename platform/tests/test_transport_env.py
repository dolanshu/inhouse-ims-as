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

"""Unit tests for runtime transport env loading."""

from __future__ import annotations

import pytest

from as_platform.runtime.transport_env import (
    load_sip_listen_config_from_env,
    load_transport_seam_from_env,
)

pytestmark = pytest.mark.unit


def test_listen_config_defaults_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AS_SIP_BIND_ADDRESS", raising=False)
    monkeypatch.delenv("AS_SIP_ADVERTISED_ADDRESS", raising=False)
    cfg = load_sip_listen_config_from_env()
    assert cfg.bind_address == "127.0.0.1"
    assert cfg.advertised_address == "127.0.0.1"


def test_bind_all_requires_advertised(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_SIP_BIND_ADDRESS", "0.0.0.0")
    monkeypatch.delenv("AS_SIP_ADVERTISED_ADDRESS", raising=False)
    with pytest.raises(ValueError, match="AS_SIP_ADVERTISED_ADDRESS"):
        load_sip_listen_config_from_env()


def test_tls_enable_requires_cert_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AS_TLS_ENABLE", "1")
    monkeypatch.delenv("AS_TLS_CERT_PATH", raising=False)
    monkeypatch.delenv("AS_TLS_KEY_PATH", raising=False)
    with pytest.raises(ValueError, match="AS_TLS_CERT_PATH"):
        load_transport_seam_from_env()
