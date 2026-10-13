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

"""Executable entry point for the deployable AS process shell."""

from __future__ import annotations

import argparse
import logging
import os
import signal
import threading
import time
from collections.abc import Callable, Sequence
from types import FrameType

from as_platform.ops.downscale_config import (
    DownscaleGuardConfig,
    load_downscale_guard_config,
    pod_removable_under_guard,
)
from as_platform.runtime.active_calls import ActiveCallSource, resolve_instance_id
from as_platform.runtime.health import HealthServer, HealthServerConfig
from as_platform.runtime.sip_stack_service import SipStackService
from as_platform.runtime.state_probe import probe_redis_available
from as_platform.shell import ProcessShell, ShellConfig
from as_platform.sip.metrics_bridge import record_sip_status_code
from as_platform.telemetry import BoundedQueueSink, default_sink
from as_platform.telemetry.metrics import CallMetrics, MetricsRegistry, emit_snapshot

_DEFAULT_DRAIN_TIMEOUT_SECONDS = 300.0
_DRAIN_TIMEOUT_EXIT_CODE = 1
_RUNTIME_ERROR_EXIT_CODE = 2
_METRICS_INTERVAL_SECONDS = 15.0


def build_shell(
    config: ShellConfig,
    active_calls: Callable[[], int],
    sleep: Callable[[float], None],
    now: Callable[[], float],
) -> ProcessShell:
    """Assemble the process shell from explicitly injected collaborators.

    Args:
        config: Draining and polling parameters.
        active_calls: Returns the current number of in-flight calls.
        sleep: Suspends draining between active-call checks.
        now: Returns monotonic seconds for the drain deadline.

    Returns:
        A shell that initially accepts new requests.
    """
    return ProcessShell(config=config, active_calls=active_calls, sleep=sleep, now=now)


def _parse_config(argv: Sequence[str] | None) -> tuple[ShellConfig, bool]:
    """Parse process-shell configuration from command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the AS process shell.")
    parser.add_argument(
        "--drain-timeout-seconds",
        type=float,
        default=_DEFAULT_DRAIN_TIMEOUT_SECONDS,
        help="maximum time to wait for in-flight calls during termination",
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=float,
        default=ShellConfig.poll_interval_seconds,
        help="delay between active-call checks while draining",
    )
    parser.add_argument(
        "--no-health-server",
        action="store_true",
        help="disable the HTTP health/metrics server (unit tests)",
    )
    arguments = parser.parse_args(list(argv) if argv is not None else None)
    config = ShellConfig(
        drain_timeout_seconds=arguments.drain_timeout_seconds,
        poll_interval_seconds=arguments.poll_interval_seconds,
    )
    return config, arguments.no_health_server


def _optional_int_env(name: str) -> int | None:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return None
    return int(raw)


def _apply_m5_metrics_probes(call_metrics: CallMetrics, use_case: str) -> None:
    """Optional Helm/kind probes that prove ``as_sip_responses_total`` wiring (M5.1 G-4).

    Production on-prem leaves ``AS_M5_PROBE_SIP_STATUS`` unset. Kind/M5 evidence may set
    one terminal status (for example ``404``) once at process start.
    """
    raw_status = os.environ.get("AS_M5_PROBE_SIP_STATUS", "").strip()
    if not raw_status:
        return
    record_sip_status_code(call_metrics, use_case, int(raw_status))


def _start_metrics_loop(
    registry: MetricsRegistry,
    call_metrics: CallMetrics,
    active_calls: ActiveCallSource,
    instance_id: str,
    use_case: str,
    guard: DownscaleGuardConfig,
    is_draining: Callable[[], bool],
    sink: BoundedQueueSink | object,
    stop: threading.Event,
) -> threading.Thread:
    last_telemetry_drops = 0

    def loop() -> None:
        nonlocal last_telemetry_drops
        while not stop.is_set():
            count = active_calls.count()
            call_metrics.set_active_calls(instance_id, use_case, count)
            removable = pod_removable_under_guard(
                guard,
                instance_id=instance_id,
                active_calls=count,
                draining=is_draining(),
            )
            call_metrics.set_downscale_removable(instance_id, use_case, removable)
            redis_url = os.environ.get("REDIS_URL", "").strip()
            if redis_url:
                call_metrics.set_state_store_available(
                    use_case,
                    probe_redis_available(redis_url),
                )
            if isinstance(sink, BoundedQueueSink):
                dropped = sink.dropped_count
                delta = dropped - last_telemetry_drops
                if delta > 0:
                    call_metrics.record_telemetry_dropped(use_case, delta)
                last_telemetry_drops = dropped
                emit_snapshot(sink, registry)
            stop.wait(_METRICS_INTERVAL_SECONDS)

    thread = threading.Thread(target=loop, name="as-metrics-loop", daemon=True)
    thread.start()
    return thread


def main(argv: Sequence[str] | None = None) -> int:
    """Run the signal-aware process shell until termination.

    Exit code ``0`` means draining completed normally. A non-zero exit code means
    that draining timed out or the runtime raised an exception.

    Args:
        argv: Optional command-line arguments. ``None`` reads the process command
            line through :mod:`argparse`.

    Returns:
        ``0`` after a clean drain, ``1`` after a drain timeout, or ``2`` after a
        runtime exception.
    """
    config, disable_health = _parse_config(argv)
    try:
        guard = load_downscale_guard_config()
    except ValueError:
        logging.exception("Invalid downscale guard configuration")
        return _RUNTIME_ERROR_EXIT_CODE
    logging.info(
        "downscale guard enabled=%s protect_above=%s",
        guard.enabled,
        guard.protect_when_active_calls_above,
    )

    shell_holder: list[ProcessShell] = []

    def is_terminating() -> bool:
        return not shell_holder[0].accepts_new_requests() if shell_holder else False

    call_source = ActiveCallSource(is_terminating=is_terminating, now=time.monotonic)
    shell = build_shell(
        config=config,
        active_calls=call_source.count,
        sleep=time.sleep,
        now=time.monotonic,
    )
    shell_holder.append(shell)

    instance_id = resolve_instance_id()
    use_case = os.environ.get("AS_USE_CASE", "unknown")
    registry = MetricsRegistry()
    call_metrics = CallMetrics(registry)
    _apply_m5_metrics_probes(call_metrics, use_case)

    telemetry_sink = default_sink()
    bounded_sink: BoundedQueueSink | None = None
    otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if otel_endpoint:
        bounded_sink = BoundedQueueSink(capacity=256)
        bounded_sink.start()

    # SipStackService handle declared before try so finally can clean up.
    # Creation happens inside the try block below so that a missing native
    # extension (RuntimeError from from_env) is caught and mapped to exit
    # code 2 instead of an unhandled traceback.
    sip_service: SipStackService | None = None

    health_server: HealthServer | None = None
    health_port = _optional_int_env("AS_HEALTH_PORT")
    if health_port is not None and not disable_health:
        health_server = HealthServer(
            HealthServerConfig(port=health_port),
            is_ready=shell.accepts_new_requests,
            metrics_registry=registry,
        )
        health_server.start()

    metrics_stop = threading.Event()
    metrics_thread = _start_metrics_loop(
        registry,
        call_metrics,
        call_source,
        instance_id,
        use_case,
        guard,
        is_terminating,
        bounded_sink if bounded_sink is not None else telemetry_sink,
        metrics_stop,
    )

    def request_terminate(_signum: int, _frame: FrameType | None) -> None:
        shell.request_terminate()

    termination_signals = (signal.SIGTERM, signal.SIGINT)
    previous_handlers = {signum: signal.getsignal(signum) for signum in termination_signals}

    try:
        # SipStackService: start SIP runtime listener when AS_ENABLE_SIP_RUNTIME=1.
        # Fail-closed: if the env var is set but the native extension is missing,
        # from_env raises RuntimeError which is caught below and maps to exit 2.
        if os.environ.get("AS_ENABLE_SIP_RUNTIME", "").strip():
            sip_service = SipStackService.from_env(call_source)
            if sip_service is not None:
                sip_service.start()
                logging.info("SipStackService started (SIP runtime listener active)")

        for signum in termination_signals:
            signal.signal(signum, request_terminate)

        while shell.accepts_new_requests():
            signal.pause()

        # Drain: stop the SIP listener so no new calls are accepted, then wait
        # for in-flight dialogs to finish via shell.run_until_drained().
        if sip_service is not None:
            sip_service.stop()

        return 0 if shell.run_until_drained() else _DRAIN_TIMEOUT_EXIT_CODE
    except Exception:
        logging.exception("The AS process shell failed")
        return _RUNTIME_ERROR_EXIT_CODE
    finally:
        metrics_stop.set()
        metrics_thread.join(timeout=2.0)
        if sip_service is not None:
            try:
                sip_service.stop()
            except Exception:
                logging.exception("Error stopping SipStackService during cleanup")
        if bounded_sink is not None:
            bounded_sink.stop()
        if health_server is not None:
            health_server.stop()
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)


if __name__ == "__main__":
    raise SystemExit(main())
