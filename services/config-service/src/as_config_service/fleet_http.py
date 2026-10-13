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

"""Small urllib helpers for fleet outbound HTTP."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener, urlopen

_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})


def urlopen_for_request(request: Request, *, timeout: float) -> Any:
    """Open ``request``, bypassing HTTP(S)_PROXY for loopback targets."""
    host = (urlparse(request.full_url).hostname or "").lower()
    if host in _LOOPBACK_HOSTS:
        return build_opener(ProxyHandler({})).open(request, timeout=timeout)
    return urlopen(request, timeout=timeout)
