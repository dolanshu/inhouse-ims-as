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

# ---- Stage 0: build reSIProcate shared libraries + Python native extensions ----
FROM python:3.10-bookworm AS resip-builder

WORKDIR /build

# Build-time dependencies: cmake, g++, libssl, libc-ares, popt, python3-dev, pkg-config
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cmake \
        build-essential \
        libssl-dev \
        libc-ares-dev \
        libpopt-dev \
        python3-dev \
        pkg-config \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy and verify the reSIProcate source tarball
COPY testbed/simulators/resip-probe/vendor/SHA256SUMS /build/vendor/SHA256SUMS
COPY testbed/simulators/resip-probe/vendor/resiprocate-1.14.0-632e215c-source.tar.gz /build/vendor/resiprocate-1.14.0-632e215c-source.tar.gz

RUN cd /build/vendor && sha256sum -c SHA256SUMS --ignore-missing

# Extract reSIProcate source
RUN mkdir -p /build/resip-source \
    && tar -xzf /build/vendor/resiprocate-1.14.0-632e215c-source.tar.gz \
        --strip-components=1 -C /build/resip-source

# Build reSIProcate (rutil, resip, dum) - minimal build, no extras
RUN mkdir -p /build/resip-build \
    && cmake -S /build/resip-source -B /build/resip-build \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/usr/local \
        -DUSE_CONTRIB=OFF \
        -DBUILD_PYTHON=OFF \
        -DUSE_MAXMIND_GEOIP=OFF \
        -DBUILD_TFM=OFF \
        -DBUILD_REPRO=OFF \
        -DBUILD_RETURN=OFF \
        -DBUILD_RECON=OFF \
        -DBUILD_REND=OFF \
        -DBUILD_MEDIA=OFF \
        -DBUILD_REFLOW=OFF \
        -DBUILD_TESTING=OFF \
        -DRESIP_HAVE_RADCLI=OFF \
        -DUSE_NETSNMP=OFF \
        -DUSE_GSTREAMER=OFF \
        -DBUILD_QPID_PROTON=OFF \
    && cmake --build /build/resip-build --parallel "$(nproc)"

# Install reSIProcate shared libraries to /usr/local/lib
# Use `libdum*` (not `libdum.so*`) to capture both versioned (libdum-1.14.so)
# and unversioned (libdum.so) names; native extensions NEEDED the versioned name.
RUN cd /build/resip-build \
    && cp rutil/librutil* /usr/local/lib/ \
    && cp resip/stack/libresip* /usr/local/lib/ \
    && cp resip/dum/libdum* /usr/local/lib/ \
    && ldconfig

# Copy platform native extension source trees
COPY src/platform/native/resip_runtime /build/native/resip_runtime
COPY src/platform/native/resip_two_leg /build/native/resip_two_leg
COPY src/platform/native/resip_recovery /build/native/resip_recovery

# Build _resip_runtime extension
RUN RESIP_RPATH="/build/resip-build/rutil:/build/resip-build/resip/stack:/build/resip-build/resip/dum" \
    && mkdir -p /build/native/resip_runtime/build \
    && cmake -S /build/native/resip_runtime -B /build/native/resip_runtime/build \
        -DRESIP_HOME=/build/resip-source \
        -DRESIP_BUILD=/build/resip-build \
        -DPython3_EXECUTABLE=$(which python3) \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_RPATH="${RESIP_RPATH}" \
        -DCMAKE_BUILD_RPATH="${RESIP_RPATH}" \
    && cmake --build /build/native/resip_runtime/build --parallel "$(nproc)"

# Build _resip_two_leg extension
RUN RESIP_RPATH="/build/resip-build/rutil:/build/resip-build/resip/stack:/build/resip-build/resip/dum" \
    && mkdir -p /build/native/resip_two_leg/build \
    && cmake -S /build/native/resip_two_leg -B /build/native/resip_two_leg/build \
        -DRESIP_HOME=/build/resip-source \
        -DRESIP_BUILD=/build/resip-build \
        -DPython3_EXECUTABLE=$(which python3) \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_RPATH="${RESIP_RPATH}" \
        -DCMAKE_BUILD_RPATH="${RESIP_RPATH}" \
    && cmake --build /build/native/resip_two_leg/build --parallel "$(nproc)"

# Build _resip_recovery extension
RUN RESIP_RPATH="/build/resip-build/rutil:/build/resip-build/resip/stack:/build/resip-build/resip/dum" \
    && mkdir -p /build/native/resip_recovery/build \
    && cmake -S /build/native/resip_recovery -B /build/native/resip_recovery/build \
        -DRESIP_HOME=/build/resip-source \
        -DRESIP_BUILD=/build/resip-build \
        -DPython3_EXECUTABLE=$(which python3) \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_RPATH="${RESIP_RPATH}" \
        -DCMAKE_BUILD_RPATH="${RESIP_RPATH}" \
    && cmake --build /build/native/resip_recovery/build --parallel "$(nproc)"

# Collect extension .so files into /build/native-dist/
RUN mkdir -p /build/native-dist \
    && EXT_SUFFIX=$(python3 -c 'import sysconfig; print(sysconfig.get_config_var("EXT_SUFFIX"))') \
    && for name in _resip_runtime _resip_two_leg _resip_recovery; do \
         src="/build/native/${name#_}/build/${name}${EXT_SUFFIX}"; \
         if [ -f "$src" ]; then \
           cp "$src" "/build/native-dist/${name}${EXT_SUFFIX}"; \
         else \
           cp "/build/native/${name#_}/build/${name}.so" "/build/native-dist/${name}.so" 2>/dev/null || true; \
         fi; \
       done

# ---- Stage 1: Python package build (uv workspace) ----
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS py-builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy
WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/platform/pyproject.toml src/platform/README.md src/platform/
COPY src/apps/translation/pyproject.toml src/apps/translation/README.md src/apps/translation/
COPY src/apps/anti-fraud/pyproject.toml src/apps/anti-fraud/README.md src/apps/anti-fraud/
COPY src/services/config-service/pyproject.toml src/services/config-service/README.md src/services/config-service/
COPY src/services/console/pyproject.toml src/services/console/README.md src/services/console/
COPY testbed/simulators/pyproject.toml testbed/simulators/README.md testbed/simulators/
COPY testbed/load/pyproject.toml testbed/load/README.md testbed/load/

RUN uv sync --frozen --no-dev --package as-platform --no-install-workspace

COPY src/platform/src src/platform/src
RUN uv sync --frozen --no-dev --package as-platform --no-editable

# ---- Stage 2: final runtime image ----
FROM python:3.10-slim AS runtime

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LD_LIBRARY_PATH="/app/lib" \
    AS_ENABLE_SIP_RUNTIME=1 \
    AS_RESIP_RUNTIME_BUILD="/app/native" \
    AS_RESIP_TWO_LEG_BUILD="/app/native" \
    AS_RESIP_RECOVERY_BUILD="/app/native"
WORKDIR /app

RUN groupadd --gid 10001 as-runtime \
    && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /nonexistent \
        --shell /usr/sbin/nologin as-runtime

# Runtime deps: libssl, libc-ares (needed by reSIProcate)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libssl3 \
        libc-ares2 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy reSIProcate shared libraries from resip-builder into /app/lib
# Match both versioned (libdum-1.14.so) and unversioned (libdum.so) names.
COPY --from=resip-builder /usr/local/lib/librutil* /app/lib/
COPY --from=resip-builder /usr/local/lib/libresip* /app/lib/
COPY --from=resip-builder /usr/local/lib/libdum* /app/lib/

# Copy Python venv from py-builder
COPY --from=py-builder --chown=10001:10001 /app/.venv /app/.venv

# Copy native extensions into /app/native (AS_RESIP_*_BUILD points here)
COPY --from=resip-builder --chown=10001:10001 /build/native-dist/ /app/native/

# SIP listening ports: 5060 UDP, 5060 TCP, 5061 TLS
EXPOSE 5060/udp 5060/tcp 5061/tcp

USER 10001:10001
ENTRYPOINT ["python", "-m", "as_platform"]
