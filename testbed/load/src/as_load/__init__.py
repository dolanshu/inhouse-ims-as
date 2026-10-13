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

"""Capacity harness (layer ⑥, performance).

Drives the AS over real sockets, never by calling callbacks directly: a harness
that bypasses the socket and the event loop measures business logic, not system
capacity. The numbers it produces are evidence for ADR-0011, not marketing.
"""

__all__: list[str] = []
