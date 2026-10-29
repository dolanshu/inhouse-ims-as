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

"""Run the translation use case process shell with optional product SIP runtime."""

from __future__ import annotations

import os


def main() -> int:
    """Set ``AS_USE_CASE=translation`` and delegate to the platform process shell."""
    os.environ.setdefault("AS_USE_CASE", "translation")
    from as_platform.__main__ import main as platform_main

    return platform_main()


if __name__ == "__main__":
    raise SystemExit(main())
