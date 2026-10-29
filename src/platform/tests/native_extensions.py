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

"""Helpers for optional cmake-built native extensions in tests."""

from __future__ import annotations

import os

import pytest

from as_platform.sip.resip_runtime import load_resip_runtime_extension


def require_resip_runtime_extension() -> object:
    """Return ``_resip_runtime`` or skip/fail per ``AS_REQUIRE_NATIVE_EXTENSIONS``."""
    extension = load_resip_runtime_extension()
    if extension is not None:
        return extension
    message = "platform _resip_runtime extension not built; run make m2-platform-resip-build"
    if os.environ.get("AS_REQUIRE_NATIVE_EXTENSIONS", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }:
        pytest.fail(message)
    pytest.skip(message)
