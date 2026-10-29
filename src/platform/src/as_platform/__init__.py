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

"""Kernel of the third-party IMS Application Server.

This package owns what every AS instance shares and nothing that belongs to a
specific use case: the process shell, the B2BUA state machine, the ``decide()``
decision seam, and the two pluggable seams (``Transport``, ``StateStore``).

It must never import an application, a service or the testbed. That one-way rule
is asserted by ``tests/test_library_independence.py`` in this directory.
"""

__all__: list[str] = []
