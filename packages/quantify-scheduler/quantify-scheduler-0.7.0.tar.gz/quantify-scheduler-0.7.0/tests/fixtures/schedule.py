# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=missing-module-docstring

# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the main branch
"""Pytest fixtures for quantify-scheduler."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict, Optional

import numpy as np
import pytest
from quantify_scheduler.schemas.examples.circuit_to_device_example_cfgs import (
    example_transmon_cfg,
)
from quantify_scheduler.backends.circuit_to_device import DeviceCompilationConfig
from quantify_scheduler import Schedule
from quantify_scheduler.compilation import (
    device_compile,
    qcompile,
)
from quantify_scheduler.operations.gate_library import X90, Measure, Reset, X
from quantify_scheduler.schemas.examples import utils

# load here to avoid loading every time a fixture is used
DEVICE_CONFIG = utils.load_json_example_scheme("transmon_test_config.json")

QBLOX_HARDWARE_MAPPING = utils.load_json_example_scheme("qblox_test_mapping.json")
ZHINST_HARDWARE_MAPPING = utils.load_json_example_scheme("zhinst_test_mapping.json")


@pytest.fixture
def load_example_transmon_config() -> Dict[str, Any]:
    """
    Circuit to device level compilation for the add_pulse_info_transmon compilation
    backend.
    """

    def _load_example_transmon_config():
        return DeviceCompilationConfig.parse_obj(example_transmon_cfg)

    yield _load_example_transmon_config


@pytest.fixture
def load_legacy_transmon_config() -> Dict[str, Any]:
    """
    Loads the configuration for `add_pulse_information_transmon`.
    To be removed after 0.7.0 when this functionality is phased out.
    """

    def _load_example_transmon_config():
        return dict(DEVICE_CONFIG)

    yield _load_example_transmon_config


@pytest.fixture
def load_example_qblox_hardware_config() -> Dict[str, Any]:
    def _load_example_qblox_hardware_config():
        return dict(QBLOX_HARDWARE_MAPPING)

    yield _load_example_qblox_hardware_config


@pytest.fixture
def load_example_zhinst_hardware_config() -> Dict[str, Any]:
    def _load_example_zhinst_hardware_config():
        return dict(ZHINST_HARDWARE_MAPPING)

    yield _load_example_zhinst_hardware_config


@pytest.fixture
def create_schedule_with_pulse_info(
    load_example_transmon_config, basic_schedule: Schedule
):
    def _create_schedule_with_pulse_info(
        schedule: Optional[Schedule] = None, device_config: Optional[dict] = None
    ) -> Schedule:
        _schedule = schedule if schedule is not None else deepcopy(basic_schedule)
        _device_config = (
            device_config
            if device_config is not None
            else load_example_transmon_config()
        )
        _schedule = device_compile(_schedule, _device_config)
        return _schedule

    yield _create_schedule_with_pulse_info


@pytest.fixture
def empty_schedule() -> Schedule:
    return Schedule("Empty Experiment")


@pytest.fixture
def basic_schedule(make_basic_schedule) -> Schedule:
    return make_basic_schedule("q0")


@pytest.fixture
def make_basic_schedule() -> Callable[[str], Schedule]:
    def _make_basic_schedule(qubit: str) -> Schedule:
        schedule = Schedule(f'Basic schedule{" "+qubit if qubit != "q0" else ""}')
        schedule.add(X90(qubit))
        return schedule

    return _make_basic_schedule


@pytest.fixture
def schedule_with_measurement(make_schedule_with_measurement) -> Schedule:
    """
    Simple schedule with gate and measurement on qubit 0.
    """
    return make_schedule_with_measurement("q0")


@pytest.fixture
def schedule_with_measurement_q2(make_schedule_with_measurement) -> Schedule:
    """
    Simple schedule with gate and measurement on qubit 2.
    """
    return make_schedule_with_measurement("q2")


@pytest.fixture
def make_schedule_with_measurement() -> Callable[[str], Schedule]:
    """
    Simple schedule with gate and measurement on single qubit.
    """

    def _make_schedule_with_measurement(qubit: str):
        schedule = Schedule(f"Schedule with measurement {qubit}")
        schedule.add(Reset(qubit))
        schedule.add(X90(qubit))
        schedule.add(Measure(qubit))
        return schedule

    return _make_schedule_with_measurement


@pytest.fixture
def schedule_with_pulse_info(create_schedule_with_pulse_info) -> Schedule:
    return create_schedule_with_pulse_info()


@pytest.fixture
def compiled_two_qubit_t1_schedule(load_example_transmon_config):
    """
    a schedule performing T1 on two-qubits simultaneously
    """
    device_config = load_example_transmon_config()

    q0, q1 = ("q0", "q1")
    repetitions = 1024
    schedule = Schedule("Multi-qubit T1", repetitions)

    times = np.arange(0, 60e-6, 3e-6)

    for i, tau in enumerate(times):
        schedule.add(Reset(q0, q1), label=f"Reset {i}")
        schedule.add(X(q0), label=f"pi {i} {q0}")
        schedule.add(X(q1), label=f"pi {i} {q1}", ref_pt="start")

        schedule.add(
            Measure(q0, acq_index=i, acq_channel=0),
            ref_pt="start",
            rel_time=tau,
            label=f"Measurement {q0}{i}",
        )
        schedule.add(
            Measure(q1, acq_index=i, acq_channel=1),
            ref_pt="start",
            rel_time=tau,
            label=f"Measurement {q1}{i}",
        )

    comp_t1_sched = qcompile(schedule, device_config)
    return comp_t1_sched
