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

"""Optional runtime probes for ops metrics (M5.1)."""

from __future__ import annotations


def probe_redis_available(url: str, *, timeout_seconds: float = 1.0) -> bool:
    """Return whether Redis answers ``PING`` within the timeout.

    Args:
        url: ``REDIS_URL`` from deployment configuration.
        timeout_seconds: Socket connect timeout for the probe.

    Returns:
        ``False`` when the URL is empty or the probe fails.
    """
    if not url.strip():
        return False
    try:
        import redis  # lazy: optional at import time

        client = redis.Redis.from_url(url, socket_connect_timeout=timeout_seconds)
        return client.ping() is True
    except Exception:
        return False
