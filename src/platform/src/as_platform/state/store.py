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

"""The StateStore seam and the key namespace every implementation shares.

Runtime keys are namespaced ``as:{case}:{kind}:{id}`` and must carry a TTL; a
runtime key without a TTL is governance data by accident (ADR-0007). Both
``set`` and ``delete`` are idempotent so that a Redis split-brain window can
replay a write without changing the outcome (risk R5, open item D3).
"""

from __future__ import annotations

from typing import Protocol

# The single global prefix of the runtime namespace. See ADR-0007.
KEY_PREFIX = "as"


def build_key(case: str, kind: str, entity_id: str, namespace: str = KEY_PREFIX) -> str:
    """Build a runtime key.

    Args:
        case: The use case owning the key, for example ``translation``.
        kind: The kind of state, for example ``dialog``.
        entity_id: The identifier, typically a Call-ID.
        namespace: The global key prefix, ``as`` by default.

    Returns:
        The key ``as:{case}:{kind}:{id}``.
    """
    return f"{namespace}:{case}:{kind}:{entity_id}"  # See ADR-0007


class StateStore(Protocol):
    """Where the kernel keeps runtime state. Implementations must be swappable."""

    def get(self, key: str) -> bytes | None:
        """Read a key.

        Args:
            key: A key built by ``build_key``.

        Returns:
            The stored bytes, or ``None`` when the key is absent or expired.
        """
        ...

    def set(self, key: str, value: bytes, ttl_seconds: float | None = None) -> None:
        """Write a key, idempotently.

        Args:
            key: A key built by ``build_key``.
            value: The bytes to store; values are binary safe.
            ttl_seconds: The lifetime of the key. ``None`` means no expiry,
                which ADR-0007 reserves for non-runtime data.
        """
        ...

    def delete(self, key: str) -> None:
        """Remove a key; deleting an absent key is not an error.

        Args:
            key: A key built by ``build_key``.
        """
        ...

    def expire(self, key: str, ttl_seconds: float) -> None:
        """Re-arm the TTL of an existing key.

        Args:
            key: A key built by ``build_key``.
            ttl_seconds: The new lifetime, counted from the injected clock.
        """
        ...
