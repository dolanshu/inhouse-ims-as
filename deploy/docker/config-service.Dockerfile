# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder

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

RUN uv sync --frozen --no-dev --package as-config-service --no-install-workspace

COPY src/platform/src src/platform/src
COPY src/services/config-service/src src/services/config-service/src
COPY src/services/console/src src/services/console/src
COPY src/services/console/web src/services/console/web
RUN uv sync --frozen --no-dev --package as-config-service --no-editable

FROM python:3.10-slim AS runtime

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN groupadd --gid 10001 as-runtime \
    && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /nonexistent \
        --shell /usr/sbin/nologin as-runtime

COPY --from=builder --chown=10001:10001 /app/.venv /app/.venv

EXPOSE 8000/tcp

USER 10001:10001
ENTRYPOINT ["as-config-service"]