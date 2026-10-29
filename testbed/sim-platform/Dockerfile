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

FROM python:3.10-slim-bookworm

ARG DEBIAN_MIRROR=deb.debian.org
RUN sed -i "s|deb.debian.org|${DEBIAN_MIRROR}|g" /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends openssl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --create-home --shell /usr/sbin/nologin sim

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /bin/uv

WORKDIR /src
COPY pyproject.toml uv.lock ./
COPY src/platform src/platform
COPY src/apps/translation src/apps/translation
COPY src/apps/anti-fraud src/apps/anti-fraud
COPY src/services/config-service src/services/config-service
COPY src/services/console src/services/console
COPY testbed/simulators/pyproject.toml testbed/simulators/pyproject.toml
COPY testbed/simulators/src testbed/simulators/src
COPY testbed/simulators/README.md testbed/simulators/README.md
COPY testbed/load/pyproject.toml testbed/load/pyproject.toml
COPY testbed/load/src testbed/load/src
COPY testbed/load/README.md testbed/load/README.md

RUN uv sync --frozen --no-dev --package as-simulators \
    && /src/.venv/bin/python -c "from pathlib import Path; import as_simulators; assert (Path(as_simulators.__file__).parent / 'static' / 'index.html').is_file()"

ENV PATH="/src/.venv/bin:${PATH}"
USER 10001
EXPOSE 8088 5060/tcp 5060/udp 5061/tcp
ENTRYPOINT ["as-simulators"]
CMD ["serve", "--host", "0.0.0.0", "--ui-host", "0.0.0.0"]
