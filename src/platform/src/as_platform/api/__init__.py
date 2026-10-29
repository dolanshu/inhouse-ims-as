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

"""The internal API package: the contract between the kernel and a use case.

The models here are the wire shape of the internal API. The implementation of
that API belongs to M4. See ADR-0002 and lld.md §1.
"""

from __future__ import annotations

from .contract import (
    AppliedVersionReport,
    ConfigBundle,
    RuleDTO,
    ToggleDTO,
    toggle_deployment,
)

__all__: list[str] = [
    "AppliedVersionReport",
    "ConfigBundle",
    "RuleDTO",
    "ToggleDTO",
    "toggle_deployment",
]
