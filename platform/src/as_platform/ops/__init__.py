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

"""Operations primitives: the verdicts that drive scaling, not the actuators.

This package decides **what may be done** to a running deployment; it never
does it. Nothing here talks to Kubernetes, to Helm or to a cluster API: the
modules are pure functions over the load a caller reports, and the caller —
the operations layer — carries the verdict out and acts on it. Keeping the
two apart is what makes the verdict testable without a cluster (AGENT.md §5:
decision modules are pure, no socket, no clock, no global state).

See ADR-0010.
"""
