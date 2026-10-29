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

"""Operations console (layer ③, control plane).

Read-write surface for the operator: rule editing through change orders, call
trace lookup by Call-ID, live statistics. It reaches an AS only through the
AS's internal API.
"""

from __future__ import annotations

from .access import (
    ROLE_PERMISSIONS,
    AuditOutcome,
    AuditRecord,
    Permission,
    Principal,
    Role,
    audit,
    authorize,
    authorize_and_audit,
    may_approve,
    permissions_for,
)

__all__: list[str] = [
    "ROLE_PERMISSIONS",
    "AuditOutcome",
    "AuditRecord",
    "Permission",
    "Principal",
    "Role",
    "audit",
    "authorize",
    "authorize_and_audit",
    "may_approve",
    "permissions_for",
]
