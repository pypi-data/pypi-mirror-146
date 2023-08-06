# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=missing-module-docstring

# Repository: https://gitlab.com/quantify-os/quantify-scheduler
# Licensed according to the LICENCE file on the main branch
"""Tests for Qblox backend."""
import copy
import inspect
import json
import logging
import os
import re
import shutil
import tempfile
from typing import Any, Dict

import numpy as np
import pytest
from qblox_instruments import Pulsar, PulsarType

# pylint: disable=no-name-in-module
from quantify_core.data.handling import set_datadir

import quantify_scheduler
import quantify_scheduler.schemas.examples as es
from quantify_scheduler import Schedule
from quantify_scheduler.backends import qblox_backend as qb
from quantify_scheduler.backends.qblox import (
    compiler_container,
    constants,
    q1asm_instructions,
    register_manager,
)
from quantify_scheduler.backends.qblox.compiler_abc import Sequencer
from quantify_scheduler.backends.qblox.helpers import (
    find_all_port_clock_combinations,
    find_inner_dicts_containing_key,
    generate_uuid_from_wf_data,
    generate_waveform_data,
    to_grid_time,
)
from quantify_scheduler.backends.qblox.instrument_compilers import (
    QcmModule,
    QcmRfModule,
    QrmModule,
    QrmRfModule,
)
from quantify_scheduler.backends.qblox.qasm_program import QASMProgram
from quantify_scheduler.backends.types import qblox as types
from quantify_scheduler.backends.types.qblox import BasebandModuleSettings

from quantify_scheduler.compilation import (
    determine_absolute_timing,
    device_compile,
    qcompile,
)
from quantify_scheduler.operations.acquisition_library import (
    Trace,
)
from quantify_scheduler.operations.gate_library import Measure, Reset, X
from quantify_scheduler.operations.pulse_library import (
    DRAGPulse,
    RampPulse,
    SquarePulse,
)
from quantify_scheduler.resources import BasebandClockResource, ClockResource
from quantify_scheduler.schedules.timedomain_schedules import (
    allxy_sched,
    readout_calibration_sched,
)

esp = inspect.getfile(es)

cfg_f = os.path.abspath(os.path.join(esp, "..", "transmon_test_config.json"))
with open(cfg_f, "r", encoding="utf-8") as f:
    DEVICE_CFG = json.load(f)

map_f = os.path.abspath(os.path.join(esp, "..", "qblox_test_mapping.json"))
with open(map_f, "r", encoding="utf-8") as f:
    HARDWARE_MAPPING = json.load(f)


REGENERATE_REF_FILES: bool = False  # Set flag to true to regenerate the reference files


# --------- Test fixtures ---------
@pytest.fixture(name="hardware_cfg_latency_correction")
def make_hardware_cfg_latency_correction():
    def _make_hardware_cfg_latency_correction(correction: float, port: str, clock: str):
        return {
            "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
            "qcm0": {
                "instrument_type": "Pulsar_QCM",
                "ref": "internal",
                "complex_output_0": {
                    "line_gain_db": 0,
                    "seq0": {
                        "port": port,
                        "clock": clock,
                        "latency_correction": correction,
                    },
                },
            },
        }

    return _make_hardware_cfg_latency_correction


@pytest.fixture
def hardware_cfg_baseband():
    yield {
        "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
        "qcm0": {
            "name": "qcm0",
            "instrument_type": "Pulsar_QCM",
            "ref": "internal",
            "complex_output_0": {
                "line_gain_db": 0,
                "lo_name": "lo0",
                "seq0": {
                    "port": "q0:mw",
                    "clock": "cl0.baseband",
                    "instruction_generated_pulses_enabled": True,
                    "interm_freq": 50e6,
                },
            },
            "complex_output_1": {
                "line_gain_db": 0,
                "seq1": {"port": "q1:mw", "clock": "q1.01"},
            },
        },
        "lo0": {"instrument_type": "LocalOscillator", "frequency": None, "power": 1},
    }


@pytest.fixture
def hardware_cfg_real_mode():
    yield {
        "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
        "qcm0": {
            "name": "qcm0",
            "instrument_type": "Pulsar_QCM",
            "ref": "internal",
            "real_output_0": {
                "line_gain_db": 0,
                "seq0": {
                    "port": "LP",
                    "clock": "cl0.baseband",
                    "instruction_generated_pulses_enabled": True,
                },
            },
            "real_output_1": {
                "line_gain_db": 0,
                "seq1": {
                    "port": "RP",
                    "clock": "cl0.baseband",
                    "instruction_generated_pulses_enabled": True,
                },
            },
            "real_output_2": {
                "line_gain_db": 0,
                "seq2": {
                    "port": "TB",
                    "clock": "cl0.baseband",
                    "instruction_generated_pulses_enabled": True,
                },
            },
        },
    }


@pytest.fixture
def hardware_cfg_multiplexing():
    yield {
        "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
        "qcm0": {
            "name": "qcm0",
            "instrument_type": "Pulsar_QCM",
            "ref": "internal",
            "complex_output_0": {
                "line_gain_db": 0,
                "lo_name": "lo0",
                "seq0": {
                    "port": "q0:mw",
                    "clock": "q0.01",
                    "interm_freq": 50e6,
                },
                "seq2": {
                    "port": "q1:mw",
                    "clock": "q0.01",
                    "interm_freq": 50e6,
                },
                "seq3": {
                    "port": "q2:mw",
                    "clock": "q0.01",
                    "interm_freq": 50e6,
                },
                "seq4": {
                    "port": "q3:mw",
                    "clock": "q0.01",
                    "interm_freq": 50e6,
                },
                "seq5": {
                    "port": "q4:mw",
                    "clock": "q0.01",
                    "interm_freq": 50e6,
                },
            },
            "complex_output_1": {
                "line_gain_db": 0,
                "seq1": {"port": "q1:mw", "clock": "q1.01"},
            },
        },
        "lo0": {"instrument_type": "LocalOscillator", "frequency": None, "power": 1},
    }


@pytest.fixture
def dummy_pulsars():
    _pulsars = []
    for qcm_name in ["qcm0", "qcm1"]:
        _pulsars.append(Pulsar(name=qcm_name, dummy_type=PulsarType.PULSAR_QCM))
    for qrm_name in ["qrm0", "qrm1"]:
        _pulsars.append(Pulsar(name=qrm_name, dummy_type=PulsarType.PULSAR_QRM))

    yield _pulsars

    # teardown
    for instrument in Pulsar.instances():
        instrument.close()


@pytest.fixture
def pulse_only_schedule():
    sched = Schedule("pulse_only_experiment")
    sched.add(Reset("q0"))
    sched.add(
        DRAGPulse(
            G_amp=0.5,
            D_amp=-0.2,
            phase=90,
            port="q0:mw",
            duration=20e-9,
            clock="q0.01",
            t0=4e-9,
        )
    )
    sched.add(RampPulse(t0=2e-3, amp=0.5, duration=28e-9, port="q0:mw", clock="q0.01"))
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def cluster_only_schedule():
    sched = Schedule("cluster_only_schedule")
    sched.add(Reset("q4"))
    sched.add(
        DRAGPulse(
            G_amp=0.7,
            D_amp=-0.2,
            phase=90,
            port="q4:mw",
            duration=20e-9,
            clock="q4.01",
            t0=4e-9,
        )
    )
    sched.add(
        DRAGPulse(
            G_amp=0.2,
            D_amp=-0.2,
            phase=90,
            port="q5:mw",
            duration=20e-9,
            clock="q5.01",
            t0=4e-9,
        )
    )
    sched.add(RampPulse(t0=2e-3, amp=0.5, duration=28e-9, port="q4:mw", clock="q4.01"))
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q4.01", freq=5e9)])
    sched.add_resources([ClockResource("q5.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def pulse_only_schedule_multiplexed():
    sched = Schedule("pulse_only_experiment")
    sched.add(Reset("q0"))
    operation = sched.add(
        DRAGPulse(
            G_amp=0.7,
            D_amp=-0.2,
            phase=90,
            port="q0:mw",
            duration=20e-9,
            clock="q0.01",
            t0=4e-9,
        )
    )
    for i in range(1, 4):
        sched.add(
            DRAGPulse(
                G_amp=0.7,
                D_amp=-0.2,
                phase=90,
                port=f"q{i}:mw",
                duration=20e-9,
                clock="q0.01",
                t0=8e-9,
            ),
            ref_op=operation,
            ref_pt="start",
        )

    sched.add(RampPulse(t0=2e-3, amp=0.5, duration=28e-9, port="q0:mw", clock="q0.01"))
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def pulse_only_schedule_no_lo():
    sched = Schedule("pulse_only_schedule_no_lo")
    sched.add(Reset("q1"))
    sched.add(
        SquarePulse(
            amp=0.5,
            phase=0,
            port="q1:res",
            duration=20e-9,
            clock="q1.ro",
            t0=4e-9,
        )
    )
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q1.ro", freq=100e6)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def identical_pulses_schedule():
    sched = Schedule("identical_pulses_schedule")
    sched.add(Reset("q0"))
    sched.add(
        DRAGPulse(
            G_amp=0.7,
            D_amp=-0.2,
            phase=90,
            port="q0:mw",
            duration=20e-9,
            clock="q0.01",
            t0=4e-9,
        )
    )
    sched.add(
        DRAGPulse(
            G_amp=0.8,
            D_amp=-0.2,
            phase=90,
            port="q0:mw",
            duration=20e-9,
            clock="q0.01",
            t0=0,
        )
    )
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def pulse_only_schedule_with_operation_timing():
    sched = Schedule("pulse_only_schedule_with_operation_timing")
    sched.add(Reset("q0"))
    first_op = sched.add(
        DRAGPulse(
            G_amp=0.7,
            D_amp=-0.2,
            phase=90,
            port="q0:mw",
            duration=20e-9,
            clock="q0.01",
            t0=4e-9,
        )
    )
    sched.add(
        RampPulse(t0=2e-3, amp=0.5, duration=28e-9, port="q0:mw", clock="q0.01"),
        ref_op=first_op,
        ref_pt="end",
        rel_time=1e-3,
    )
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def mixed_schedule_with_acquisition():
    sched = Schedule("mixed_schedule_with_acquisition")
    sched.add(Reset("q0"))
    sched.add(
        DRAGPulse(
            G_amp=0.7,
            D_amp=-0.2,
            phase=90,
            port="q0:mw",
            duration=20e-9,
            clock="q0.01",
            t0=4e-9,
        )
    )
    sched.add(Measure("q0"))
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def gate_only_schedule():
    sched = Schedule("gate_only_schedule")
    sched.add(Reset("q0"))
    x_gate = sched.add(X("q0"))
    sched.add(Measure("q0"), ref_op=x_gate, rel_time=1e-6, ref_pt="end")
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def duplicate_measure_schedule():
    sched = Schedule("gate_only_schedule")
    sched.add(Reset("q0"))
    x_gate = sched.add(X("q0"))
    sched.add(Measure("q0", acq_index=0), ref_op=x_gate, rel_time=1e-6, ref_pt="end")
    sched.add(Measure("q0", acq_index=1), ref_op=x_gate, rel_time=3e-6, ref_pt="end")
    # Clocks need to be manually added at this stage.
    sched.add_resources([ClockResource("q0.01", freq=5e9)])
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def baseband_square_pulse_schedule():
    sched = Schedule("baseband_square_pulse_schedule")
    sched.add(Reset("q0"))
    sched.add(
        SquarePulse(
            amp=0.0,
            duration=2.5e-6,
            port="q0:mw",
            clock=BasebandClockResource.IDENTITY,
            t0=1e-6,
        )
    )
    sched.add(
        SquarePulse(
            amp=2.0,
            duration=2.5e-6,
            port="q0:mw",
            clock=BasebandClockResource.IDENTITY,
            t0=1e-6,
        )
    )
    determine_absolute_timing(sched)
    return sched


@pytest.fixture
def real_square_pulse_schedule():
    sched = Schedule("real_square_pulse_schedule")
    sched.add(Reset("q0"))
    sched.add(
        SquarePulse(
            amp=2.0,
            duration=2.5e-6,
            port="LP",
            clock=BasebandClockResource.IDENTITY,
            t0=1e-6,
        )
    )
    sched.add(
        SquarePulse(
            amp=1.0,
            duration=2.0e-6,
            port="RP",
            clock=BasebandClockResource.IDENTITY,
            t0=0.5e-6,
        )
    )
    sched.add(
        SquarePulse(
            amp=1.2,
            duration=3.5e-6,
            port="TB",
            clock=BasebandClockResource.IDENTITY,
            t0=0,
        )
    )
    determine_absolute_timing(sched)
    return sched


@pytest.fixture(name="empty_qasm_program_qcm")
def fixture_empty_qasm_program():
    return QASMProgram(
        QcmModule.static_hw_properties, register_manager.RegisterManager()
    )


# --------- Test utility functions ---------
def function_for_test_generate_waveform_data(t, x, y):
    return x * t + y


def test_generate_waveform_data():
    x = 10
    y = np.pi
    sampling_rate = 1e9
    duration = 1e-8
    t_verification = np.arange(0, 0 + duration, 1 / sampling_rate)
    verification_data = function_for_test_generate_waveform_data(t_verification, x, y)
    data_dict = {
        "wf_func": __name__ + ".function_for_test_generate_waveform_data",
        "x": x,
        "y": y,
        "duration": 1e-8,
    }
    gen_data = generate_waveform_data(data_dict, sampling_rate)
    assert np.allclose(gen_data, verification_data)


def test_find_inner_dicts_containing_key():
    test_dict = {
        "foo": "bar",
        "list": [{"key": 1, "hello": "world", "other_key": "other_value"}, 4, "12"],
        "nested": {"hello": "world", "other_key": "other_value"},
    }
    dicts_found = find_inner_dicts_containing_key(test_dict, "hello")
    assert len(dicts_found) == 2
    for inner_dict in dicts_found:
        assert inner_dict["hello"] == "world"
        assert inner_dict["other_key"] == "other_value"


def test_find_all_port_clock_combinations():
    portclocks = find_all_port_clock_combinations(HARDWARE_MAPPING)
    portclocks = set(portclocks)
    portclocks.discard((None, None))
    answer = {
        ("q1:mw", "q1.01"),
        ("q0:mw", "q0.01"),
        ("q0:res", "q0.ro"),
        ("q0:res", "q0.multiplex"),
        ("q1:res", "q1.ro"),
        ("q3:mw", "q3.01"),
        ("q2:mw", "q2.01"),
        ("q2:res", "q2.ro"),
        ("q3:res", "q3.ro"),
        ("q3:mw", "q3.01"),
        ("q4:mw", "q4.01"),
        ("q5:mw", "q5.01"),
        ("q4:res", "q4.ro"),
    }
    assert portclocks == answer


def test_generate_port_clock_to_device_map():
    portclock_map = qb.generate_port_clock_to_device_map(HARDWARE_MAPPING)
    assert (None, None) not in portclock_map.keys()
    assert len(portclock_map.keys()) == 12


# --------- Test classes and member methods ---------
def test_contruct_sequencer():
    class TestPulsar(QcmModule):
        def __init__(self):
            super().__init__(
                parent=None,
                name="tester",
                total_play_time=1,
                hw_mapping=HARDWARE_MAPPING["qcm0"],
            )

        def compile(self, repetitions: int = 1) -> Dict[str, Any]:
            return dict()

    test_p = TestPulsar()
    test_p.sequencers = test_p._construct_sequencers()
    seq_keys = list(test_p.sequencers.keys())
    assert len(seq_keys) == 2
    assert isinstance(test_p.sequencers[seq_keys[0]], Sequencer)


def test_simple_compile(pulse_only_schedule):
    """Tests if compilation with only pulses finishes without exceptions"""
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    qcompile(pulse_only_schedule, DEVICE_CFG, HARDWARE_MAPPING)


def test_compile_cluster(cluster_only_schedule):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    qcompile(cluster_only_schedule, DEVICE_CFG, HARDWARE_MAPPING)


def test_simple_compile_multiplexing(
    pulse_only_schedule_multiplexed, hardware_cfg_multiplexing
):
    """Tests if compilation with only pulses finishes without exceptions"""
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    qcompile(pulse_only_schedule_multiplexed, DEVICE_CFG, hardware_cfg_multiplexing)


def test_identical_pulses_compile(identical_pulses_schedule):
    """Tests if compilation with only pulses finishes without exceptions"""
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    compiled_schedule = qcompile(
        identical_pulses_schedule, DEVICE_CFG, HARDWARE_MAPPING
    )

    seq_fn = compiled_schedule.compiled_instructions["qcm0"]["seq0"]["seq_fn"]
    with open(seq_fn) as file:
        prog = json.load(file)
    assert len(prog["waveforms"]) == 2


def test_compile_measure(duplicate_measure_schedule):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    full_program = qcompile(duplicate_measure_schedule, DEVICE_CFG, HARDWARE_MAPPING)
    qrm0_seq0_json = full_program["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"]

    with open(qrm0_seq0_json) as file:
        wf_and_prog = json.load(file)
    assert len(wf_and_prog["weights"]) == 0


def test_simple_compile_with_acq(dummy_pulsars, mixed_schedule_with_acquisition):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    full_program = qcompile(
        mixed_schedule_with_acquisition, DEVICE_CFG, HARDWARE_MAPPING
    )

    qcm0_seq0_json = full_program["compiled_instructions"]["qcm0"]["seq0"]["seq_fn"]

    qcm0 = dummy_pulsars[0]
    qcm0.sequencer0.sequence(qcm0_seq0_json)
    qcm0.arm_sequencer(0)
    uploaded_waveforms = qcm0.get_waveforms(0)
    assert uploaded_waveforms is not None


def test_acquisitions_back_to_back(mixed_schedule_with_acquisition):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    sched = copy.deepcopy(mixed_schedule_with_acquisition)
    meas_op = sched.add(Measure("q0"))
    # add another one too quickly
    sched.add(Measure("q0"), ref_op=meas_op, rel_time=0.5e-6)

    sched_with_pulse_info = device_compile(sched, DEVICE_CFG)
    with pytest.raises(ValueError):
        qb.hardware_compile(sched_with_pulse_info, HARDWARE_MAPPING)


def test_compile_with_rel_time(
    dummy_pulsars, pulse_only_schedule_with_operation_timing
):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    full_program = qcompile(
        pulse_only_schedule_with_operation_timing, DEVICE_CFG, HARDWARE_MAPPING
    )

    qcm0_seq0_json = full_program["compiled_instructions"]["qcm0"]["seq0"]["seq_fn"]

    qcm0 = dummy_pulsars[0]
    qcm0.sequencer0.sequence(qcm0_seq0_json)


def test_compile_with_repetitions(mixed_schedule_with_acquisition):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    mixed_schedule_with_acquisition.repetitions = 10
    full_program = qcompile(
        mixed_schedule_with_acquisition, DEVICE_CFG, HARDWARE_MAPPING
    )
    qcm0_seq0_json = full_program["compiled_instructions"]["qcm0"]["seq0"]["seq_fn"]

    with open(qcm0_seq0_json) as file:
        wf_and_prog = json.load(file)
    program_from_json = wf_and_prog["program"]
    move_line = program_from_json.split("\n")[5]
    move_items = move_line.split()  # splits on whitespace
    args = move_items[1]
    iterations = int(args.split(",")[0])
    assert iterations == 10


def _func_for_hook_test(qasm: QASMProgram):
    qasm.instructions.insert(
        0, QASMProgram.get_instruction_as_list(q1asm_instructions.NOP)
    )


def test_qasm_hook(pulse_only_schedule):
    hw_config = {
        "backend": "quantify_scheduler.backends.qblox_backend.hardware_compile",
        "qrm0": {
            "instrument_type": "Pulsar_QRM",
            "ref": "external",
            "complex_output_0": {
                "seq0": {
                    "qasm_hook_func": _func_for_hook_test,
                    "port": "q0:mw",
                    "clock": "q0.01",
                }
            },
        },
    }
    sched = pulse_only_schedule
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    sched.repetitions = 11
    full_program = qcompile(sched, DEVICE_CFG, hw_config)
    qrm0_seq0_json = full_program["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"]
    with open(qrm0_seq0_json) as file:
        program = json.load(file)["program"]
    program_lines = program.splitlines()
    assert program_lines[1].strip() == q1asm_instructions.NOP


def test_qcm_acquisition_error():
    qcm = QcmModule(
        None, "qcm0", total_play_time=10, hw_mapping=HARDWARE_MAPPING["qcm0"]
    )
    qcm._acquisitions[0] = 0

    with pytest.raises(RuntimeError):
        qcm.distribute_data()


def test_real_mode_pulses(real_square_pulse_schedule, hardware_cfg_real_mode):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    real_square_pulse_schedule.repetitions = 10
    full_program = qcompile(
        real_square_pulse_schedule, DEVICE_CFG, hardware_cfg_real_mode
    )
    for seq in (f"seq{i}" for i in range(3)):
        assert seq in full_program.compiled_instructions["qcm0"]


# --------- Test QASMProgram class ---------


def test_emit(empty_qasm_program_qcm):
    qasm = empty_qasm_program_qcm
    qasm.emit(q1asm_instructions.PLAY, 0, 1, 120)
    qasm.emit(q1asm_instructions.STOP, comment="This is a comment that is added")

    assert len(qasm.instructions) == 2


def test_auto_wait(empty_qasm_program_qcm):
    qasm = empty_qasm_program_qcm
    qasm.auto_wait(120)
    assert len(qasm.instructions) == 1
    qasm.auto_wait(70000)
    assert len(qasm.instructions) == 3  # since it should split the waits
    assert qasm.elapsed_time == 70120
    qasm.auto_wait(700000)
    assert qasm.elapsed_time == 770120
    assert len(qasm.instructions) == 8  # now loops are used
    with pytest.raises(ValueError):
        qasm.auto_wait(-120)


def test_expand_from_normalised_range():
    minimal_pulse_data = {"duration": 20e-9}
    acq = qb.OpInfo(name="test_acq", data=minimal_pulse_data, timing=4e-9)
    expanded_val = QASMProgram.expand_from_normalised_range(
        1, constants.IMMEDIATE_MAX_WAIT_TIME, "test_param", acq
    )
    assert expanded_val == constants.IMMEDIATE_MAX_WAIT_TIME // 2
    with pytest.raises(ValueError):
        QASMProgram.expand_from_normalised_range(
            10, constants.IMMEDIATE_MAX_WAIT_TIME, "test_param", acq
        )


def test_to_grid_time():
    time_ns = to_grid_time(8e-9)
    assert time_ns == 8
    with pytest.raises(ValueError):
        to_grid_time(7e-9)


def test_loop(empty_qasm_program_qcm):
    num_rep = 10

    qasm = empty_qasm_program_qcm
    qasm.emit(q1asm_instructions.WAIT_SYNC, 4)
    with qasm.loop("this_loop", repetitions=num_rep):
        qasm.emit(q1asm_instructions.WAIT, 20)
    assert len(qasm.instructions) == 5
    assert qasm.instructions[1][1] == q1asm_instructions.MOVE
    num_rep_used, reg_used = qasm.instructions[1][2].split(",")
    assert int(num_rep_used) == num_rep


@pytest.mark.parametrize("amount", [1, 2, 3, 40])
def test_temp_register(amount, empty_qasm_program_qcm):
    qasm = empty_qasm_program_qcm
    with qasm.temp_registers(amount) as registers:
        for reg in registers:
            assert reg not in qasm.register_manager.available_registers
    for reg in registers:
        assert reg in qasm.register_manager.available_registers


# --------- Test compilation functions ---------
def test_assign_pulse_and_acq_info_to_devices(mixed_schedule_with_acquisition):
    sched_with_pulse_info = device_compile(mixed_schedule_with_acquisition, DEVICE_CFG)
    portclock_map = qb.generate_port_clock_to_device_map(HARDWARE_MAPPING)

    container = compiler_container.CompilerContainer.from_mapping(
        sched_with_pulse_info, HARDWARE_MAPPING
    )
    qb._assign_pulse_and_acq_info_to_devices(
        sched_with_pulse_info, container.instrument_compilers, portclock_map
    )
    qrm = container.instrument_compilers["qrm0"]
    assert len(qrm._pulses[list(qrm.portclocks_with_data)[0]]) == 1
    assert len(qrm._acquisitions[list(qrm.portclocks_with_data)[0]]) == 1


def test_container_prepare(pulse_only_schedule):
    container = compiler_container.CompilerContainer.from_mapping(
        pulse_only_schedule, HARDWARE_MAPPING
    )
    for instr in container.instrument_compilers.values():
        instr.prepare()

    assert (
        container.instrument_compilers["qcm0"].sequencers["seq0"].frequency is not None
    )
    assert container.instrument_compilers["lo0"].frequency is not None


def test__determine_scope_mode_acquisition_sequencer(mixed_schedule_with_acquisition):
    sched = copy.deepcopy(mixed_schedule_with_acquisition)
    sched.add(Trace(100e-9, port="q0:res", clock="q0.ro"))
    sched = device_compile(sched, DEVICE_CFG)
    container = compiler_container.CompilerContainer.from_mapping(
        sched, HARDWARE_MAPPING
    )
    portclock_map = qb.generate_port_clock_to_device_map(HARDWARE_MAPPING)
    qb._assign_pulse_and_acq_info_to_devices(
        schedule=sched,
        device_compilers=container.instrument_compilers,
        portclock_mapping=portclock_map,
    )
    for instr in container.instrument_compilers.values():
        if hasattr(instr, "_determine_scope_mode_acquisition_sequencer"):
            instr.prepare()
            instr._determine_scope_mode_acquisition_sequencer()
    scope_mode_sequencer = container.instrument_compilers[
        "qrm0"
    ]._settings.scope_mode_sequencer
    assert scope_mode_sequencer == "seq0"


def test_container_prepare_baseband(
    baseband_square_pulse_schedule, hardware_cfg_baseband
):
    container = compiler_container.CompilerContainer.from_mapping(
        baseband_square_pulse_schedule, hardware_cfg_baseband
    )
    for instr in container.instrument_compilers.values():
        instr.prepare()

    assert (
        container.instrument_compilers["qcm0"].sequencers["seq0"].frequency is not None
    )
    assert container.instrument_compilers["lo0"].frequency is not None


def test_container_prepare_no_lo(pulse_only_schedule_no_lo):
    container = compiler_container.CompilerContainer.from_mapping(
        pulse_only_schedule_no_lo, HARDWARE_MAPPING
    )
    container.compile(repetitions=10)

    assert container.instrument_compilers["qrm1"].sequencers["seq0"].frequency == 100e6


def test_container_add_from_type(pulse_only_schedule):
    container = compiler_container.CompilerContainer(pulse_only_schedule)
    container.add_instrument_compiler("qcm0", QcmModule, HARDWARE_MAPPING["qcm0"])
    assert "qcm0" in container.instrument_compilers
    assert isinstance(container.instrument_compilers["qcm0"], QcmModule)


def test_container_add_from_str(pulse_only_schedule):
    container = compiler_container.CompilerContainer(pulse_only_schedule)
    container.add_instrument_compiler("qcm0", "Pulsar_QCM", HARDWARE_MAPPING["qcm0"])
    assert "qcm0" in container.instrument_compilers
    assert isinstance(container.instrument_compilers["qcm0"], QcmModule)


def test_container_add_from_path(pulse_only_schedule):
    container = compiler_container.CompilerContainer(pulse_only_schedule)
    container.add_instrument_compiler(
        "qcm0",
        "quantify_scheduler.backends.qblox.instrument_compilers.QcmModule",
        HARDWARE_MAPPING["qcm0"],
    )
    assert "qcm0" in container.instrument_compilers
    assert isinstance(container.instrument_compilers["qcm0"], QcmModule)


def test_from_mapping(pulse_only_schedule):
    container = compiler_container.CompilerContainer.from_mapping(
        pulse_only_schedule, HARDWARE_MAPPING
    )
    for instr_name in HARDWARE_MAPPING.keys():
        if instr_name == "backend":
            continue
        assert instr_name in container.instrument_compilers


def test_generate_uuid_from_wf_data():
    arr0 = np.arange(10000)
    arr1 = np.arange(10000)
    arr2 = np.arange(10000) + 1

    hash0 = generate_uuid_from_wf_data(arr0)
    hash1 = generate_uuid_from_wf_data(arr1)
    hash2 = generate_uuid_from_wf_data(arr2)

    assert hash0 == hash1
    assert hash1 != hash2


def test_real_mode_container(real_square_pulse_schedule, hardware_cfg_real_mode):
    container = compiler_container.CompilerContainer.from_mapping(
        real_square_pulse_schedule, hardware_cfg_real_mode
    )
    qcm0 = container.instrument_compilers["qcm0"]
    for output, seq_name in enumerate(f"seq{i}" for i in range(3)):
        seq_settings = qcm0.sequencers[seq_name].settings
        assert seq_settings.connected_outputs[0] == output


def test_assign_frequencies_baseband():
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    sched = Schedule("two_gate_experiment")
    sched.add(X("q0"))
    sched.add(X("q1"))

    q0_clock_freq = DEVICE_CFG["qubits"]["q0"]["params"]["mw_freq"]
    q1_clock_freq = DEVICE_CFG["qubits"]["q1"]["params"]["mw_freq"]

    if0 = HARDWARE_MAPPING["qcm0"]["complex_output_0"]["seq0"].get("interm_freq")
    if1 = HARDWARE_MAPPING["qcm0"]["complex_output_1"]["seq1"].get("interm_freq")
    io0_lo_name = HARDWARE_MAPPING["qcm0"]["complex_output_0"]["lo_name"]
    io1_lo_name = HARDWARE_MAPPING["qcm0"]["complex_output_1"]["lo_name"]
    lo0 = HARDWARE_MAPPING[io0_lo_name].get("frequency")
    lo1 = HARDWARE_MAPPING[io1_lo_name].get("frequency")

    assert if0 is not None
    assert if1 is None
    assert lo0 is None
    assert lo1 is not None

    lo0 = q0_clock_freq - if0
    if1 = q1_clock_freq - lo1

    compiled_schedule = qcompile(sched, DEVICE_CFG, HARDWARE_MAPPING)
    compiled_instructions = compiled_schedule["compiled_instructions"]

    generic_icc = constants.GENERIC_IC_COMPONENT_NAME
    assert compiled_instructions[generic_icc][f"{io0_lo_name}.frequency"] == lo0
    assert compiled_instructions[generic_icc][f"{io1_lo_name}.frequency"] == lo1
    assert compiled_instructions["qcm0"]["seq1"]["settings"]["modulation_freq"] == if1


def test_assign_frequencies_baseband_downconverter():
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    sched = Schedule("two_gate_experiment")
    sched.add(X("q0"))
    sched.add(X("q1"))

    q0_clock_freq = DEVICE_CFG["qubits"]["q0"]["params"]["mw_freq"]
    q1_clock_freq = DEVICE_CFG["qubits"]["q1"]["params"]["mw_freq"]

    if0 = HARDWARE_MAPPING["qcm0"]["complex_output_0"]["seq0"].get("interm_freq")
    if1 = HARDWARE_MAPPING["qcm0"]["complex_output_1"]["seq1"].get("interm_freq")
    io0_lo_name = HARDWARE_MAPPING["qcm0"]["complex_output_0"]["lo_name"]
    io1_lo_name = HARDWARE_MAPPING["qcm0"]["complex_output_1"]["lo_name"]
    lo0 = HARDWARE_MAPPING[io0_lo_name].get("frequency")
    lo1 = HARDWARE_MAPPING[io1_lo_name].get("frequency")

    assert if0 is not None
    assert if1 is None
    assert lo0 is None
    assert lo1 is not None

    hw_mapping_downconverter = HARDWARE_MAPPING.copy()
    hw_mapping_downconverter["qcm0"]["complex_output_0"]["downconverter"] = True
    hw_mapping_downconverter["qcm0"]["complex_output_1"]["downconverter"] = True

    compiled_schedule = qcompile(sched, DEVICE_CFG, hw_mapping_downconverter)
    compiled_instructions = compiled_schedule["compiled_instructions"]

    lo0 = -q0_clock_freq - if0 + constants.DOWNCONVERTER_FREQ
    if1 = -q1_clock_freq - lo1 + constants.DOWNCONVERTER_FREQ

    generic_icc = constants.GENERIC_IC_COMPONENT_NAME
    assert compiled_instructions[generic_icc][f"{io0_lo_name}.frequency"] == lo0
    assert compiled_instructions[generic_icc][f"{io1_lo_name}.frequency"] == lo1
    assert compiled_instructions["qcm0"]["seq1"]["settings"]["modulation_freq"] == if1


def test_assign_frequencies_rf():
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    sched = Schedule("two_gate_experiment")
    sched.add(X("q2"))
    sched.add(X("q3"))

    if0 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_0"]["seq0"].get("interm_freq")
    if1 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_1"]["seq1"].get("interm_freq")
    lo0 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_0"].get("lo_freq")
    lo1 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_1"].get("lo_freq")

    assert if0 is not None
    assert if1 is None
    assert lo0 is None
    assert lo1 is not None

    q2_clock_freq = DEVICE_CFG["qubits"]["q2"]["params"]["mw_freq"]
    q3_clock_freq = DEVICE_CFG["qubits"]["q3"]["params"]["mw_freq"]

    if0 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_0"]["seq0"]["interm_freq"]
    lo1 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_1"]["lo_freq"]

    lo0 = q2_clock_freq - if0
    if1 = q3_clock_freq - lo1

    compiled_schedule = qcompile(sched, DEVICE_CFG, HARDWARE_MAPPING)
    compiled_instructions = compiled_schedule["compiled_instructions"]
    qcm_program = compiled_instructions["qcm_rf0"]
    assert qcm_program["settings"]["lo0_freq"] == lo0
    assert qcm_program["settings"]["lo1_freq"] == lo1
    assert qcm_program["seq1"]["settings"]["modulation_freq"] == if1


def test_assign_frequencies_rf_downconverter():
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    sched = Schedule("two_gate_experiment")
    sched.add(X("q2"))
    sched.add(X("q3"))

    if0 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_0"]["seq0"].get("interm_freq")
    if1 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_1"]["seq1"].get("interm_freq")
    lo0 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_0"].get("lo_freq")
    lo1 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_1"].get("lo_freq")

    assert if0 is not None
    assert if1 is None
    assert lo0 is None
    assert lo1 is not None

    q2_clock_freq = DEVICE_CFG["qubits"]["q2"]["params"]["mw_freq"]
    q3_clock_freq = DEVICE_CFG["qubits"]["q3"]["params"]["mw_freq"]

    if0 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_0"]["seq0"]["interm_freq"]
    lo1 = HARDWARE_MAPPING["qcm_rf0"]["complex_output_1"]["lo_freq"]

    lo0 = q2_clock_freq - if0
    if1 = q3_clock_freq - lo1

    compiled_schedule = qcompile(sched, DEVICE_CFG, HARDWARE_MAPPING)
    compiled_instructions = compiled_schedule["compiled_instructions"]
    qcm_program = compiled_instructions["qcm_rf0"]
    assert qcm_program["settings"]["lo0_freq"] == lo0
    assert qcm_program["settings"]["lo1_freq"] == lo1
    assert qcm_program["seq1"]["settings"]["modulation_freq"] == if1

    hw_mapping_downconverter = HARDWARE_MAPPING.copy()
    hw_mapping_downconverter["qcm_rf0"]["complex_output_0"]["downconverter"] = True
    hw_mapping_downconverter["qcm_rf0"]["complex_output_1"]["downconverter"] = True

    compiled_schedule = qcompile(sched, DEVICE_CFG, hw_mapping_downconverter)
    compiled_instructions = compiled_schedule["compiled_instructions"]
    qcm_program = compiled_instructions["qcm_rf0"]

    lo0 = -q2_clock_freq - if0 + constants.DOWNCONVERTER_FREQ
    if1 = -q3_clock_freq - lo1 + constants.DOWNCONVERTER_FREQ

    assert qcm_program["settings"]["lo0_freq"] == lo0
    assert qcm_program["settings"]["lo1_freq"] == lo1
    assert qcm_program["seq1"]["settings"]["modulation_freq"] == if1


def test_markers():
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    # Test for baseband
    sched = Schedule("gate_experiment")
    sched.add(X("q0"))
    sched.add(X("q2"))
    sched.add(Measure("q0"))
    sched.add(Measure("q2"))

    compiled_schedule = qcompile(sched, DEVICE_CFG, HARDWARE_MAPPING)
    program = compiled_schedule["compiled_instructions"]

    def _confirm_correct_markers(device_program, device_compiler, is_rf=False):
        mrk_config = device_compiler.static_hw_properties.marker_configuration
        answers = (
            mrk_config.init,
            mrk_config.start,
            mrk_config.end,
        )
        with open(device_program["seq0"]["seq_fn"]) as file:
            qasm = json.load(file)["program"]

            matches = re.findall(r"set\_mrk +\d+", qasm)
            matches = [int(m.replace("set_mrk", "").strip()) for m in matches]
            if not is_rf:
                matches = [None, *matches]

            for match, answer in zip(matches, answers):
                assert match == answer

    _confirm_correct_markers(program["qcm0"], QcmModule)
    _confirm_correct_markers(program["qrm0"], QrmModule)
    _confirm_correct_markers(program["qcm_rf0"], QcmRfModule, is_rf=True)
    _confirm_correct_markers(program["qrm_rf0"], QrmRfModule, is_rf=True)


def test_pulsar_rf_extract_from_mapping():
    hw_map = HARDWARE_MAPPING["qcm_rf0"]
    types.PulsarRFSettings.extract_settings_from_mapping(hw_map)


def test_cluster_settings(pulse_only_schedule):
    container = compiler_container.CompilerContainer.from_mapping(
        pulse_only_schedule, HARDWARE_MAPPING
    )
    cluster_compiler = container.instrument_compilers["cluster0"]
    cluster_compiler.prepare()
    cl_qcm0 = cluster_compiler.instrument_compilers["cluster0_module1"]
    assert isinstance(cl_qcm0._settings, BasebandModuleSettings)


def assembly_valid(compiled_schedule, qcm0, qrm0):
    """
    Test helper that takes a compiled schedule and verifies if the assembly is valid
    by passing it to a dummy qcm and qrm.

    Asssumes only qcm0 and qrm0 are used.
    """

    # test the program for the qcm
    qcm0_seq0_json = compiled_schedule["compiled_instructions"]["qcm0"]["seq0"][
        "seq_fn"
    ]
    qcm0.sequencer0.sequence(qcm0_seq0_json)
    qcm0.arm_sequencer(0)
    uploaded_waveforms = qcm0.get_waveforms(0)
    assert uploaded_waveforms is not None

    # test the program for the qrm
    qrm0_seq0_json = compiled_schedule["compiled_instructions"]["qrm0"]["seq0"][
        "seq_fn"
    ]
    qrm0.sequencer0.sequence(qrm0_seq0_json)
    qrm0.arm_sequencer(0)
    uploaded_waveforms = qrm0.get_waveforms(0)
    assert uploaded_waveforms is not None


def test_acq_protocol_append_mode_valid_assembly_ssro(
    dummy_pulsars, load_example_transmon_config
):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    repetitions = 256
    ssro_sched = readout_calibration_sched("q0", [0, 1], repetitions=repetitions)
    compiled_ssro_sched = qcompile(
        ssro_sched, load_example_transmon_config(), HARDWARE_MAPPING
    )
    assembly_valid(
        compiled_schedule=compiled_ssro_sched,
        qcm0=dummy_pulsars[0],
        qrm0=dummy_pulsars[0],
    )

    with open(
        compiled_ssro_sched["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"]
    ) as file:
        qrm0_seq_instructions = json.load(file)
    baseline_assembly = os.path.join(
        quantify_scheduler.__path__[0],
        "..",
        "tests",
        "baseline_qblox_assembly",
        f"{ssro_sched.name}_qrm0_seq0_instr.json",
    )

    if REGENERATE_REF_FILES:
        shutil.copy(
            compiled_ssro_sched["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"],
            baseline_assembly,
        )

    with open(baseline_assembly) as file:
        baseline_qrm0_seq_instructions = json.load(file)
    program = _strip_comments(qrm0_seq_instructions["program"])
    exp_program = _strip_comments(baseline_qrm0_seq_instructions["program"])

    assert list(program) == list(exp_program)


def test_acq_protocol_average_mode_valid_assembly_allxy(
    dummy_pulsars, load_example_transmon_config
):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)
    repetitions = 256
    sched = allxy_sched("q0", element_select_idx=np.arange(21), repetitions=repetitions)
    compiled_allxy_sched = qcompile(
        sched, load_example_transmon_config(), HARDWARE_MAPPING
    )

    assembly_valid(
        compiled_schedule=compiled_allxy_sched,
        qcm0=dummy_pulsars[0],
        qrm0=dummy_pulsars[0],
    )

    with open(
        compiled_allxy_sched["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"]
    ) as file:
        qrm0_seq_instructions = json.load(file)

    baseline_assembly = os.path.join(
        quantify_scheduler.__path__[0],
        "..",
        "tests",
        "baseline_qblox_assembly",
        f"{sched.name}_qrm0_seq0_instr.json",
    )

    if REGENERATE_REF_FILES:
        shutil.copy(
            compiled_allxy_sched["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"],
            baseline_assembly,
        )

    with open(baseline_assembly) as file:
        baseline_qrm0_seq_instructions = json.load(file)
    program = _strip_comments(qrm0_seq_instructions["program"])
    exp_program = _strip_comments(baseline_qrm0_seq_instructions["program"])

    assert list(program) == list(exp_program)


def test_acq_declaration_dict_append_mode(load_example_transmon_config):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    repetitions = 256

    ssro_sched = readout_calibration_sched("q0", [0, 1], repetitions=repetitions)
    compiled_ssro_sched = qcompile(
        ssro_sched, load_example_transmon_config(), HARDWARE_MAPPING
    )

    with open(
        compiled_ssro_sched["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"]
    ) as file:
        qrm0_seq_instructions = json.load(file)

    acquisitions = qrm0_seq_instructions["acquisitions"]
    # the only key corresponds to channel 0
    assert set(acquisitions.keys()) == {"0"}
    assert acquisitions["0"] == {"num_bins": 2 * 256, "index": 0}


def test_acq_declaration_dict_bin_avg_mode(load_example_transmon_config):
    tmp_dir = tempfile.TemporaryDirectory()
    set_datadir(tmp_dir.name)

    allxy = allxy_sched("q0")
    compiled_allxy_sched = qcompile(
        allxy, load_example_transmon_config(), HARDWARE_MAPPING
    )

    with open(
        compiled_allxy_sched["compiled_instructions"]["qrm0"]["seq0"]["seq_fn"]
    ) as file:
        qrm0_seq_instructions = json.load(file)

    acquisitions = qrm0_seq_instructions["acquisitions"]

    # the only key corresponds to channel 0
    assert set(acquisitions.keys()) == {"0"}
    assert acquisitions["0"] == {"num_bins": 21, "index": 0}


class TestLatencyCorrection:
    """Class to group all the tests related to latency correction in backend."""

    # pylint: disable=no-self-use
    def test_compilation_valid(
        self,
        hardware_cfg_latency_correction,
        load_example_transmon_config,
        dummy_pulsars,
    ):
        # Arrange
        tmp_dir = tempfile.TemporaryDirectory()
        set_datadir(tmp_dir.name)

        sched = Schedule("single_gate_experiment")
        sched.add(X("q0"))

        hw_cfg = hardware_cfg_latency_correction(
            correction=4e-9, port="q0:mw", clock="q0.01"
        )
        # Act
        compiled_sched = qcompile(sched, load_example_transmon_config(), hw_cfg)
        compiled_instr = compiled_sched.compiled_instructions

        # Assert
        dummy_pulsars[0].sequencer0.sequence(compiled_instr["qcm0"]["seq0"]["seq_fn"])

    def test_warning(
        self, hardware_cfg_latency_correction, load_example_transmon_config, caplog
    ):
        tmp_dir = tempfile.TemporaryDirectory()
        set_datadir(tmp_dir.name)

        sched = Schedule("single_gate_experiment")
        sched.add(X("q0"))

        hw_cfg = hardware_cfg_latency_correction(
            correction=2e-9, port="q0:mw", clock="q0.01"
        )

        # Act
        with caplog.at_level(
            logging.WARNING, logger="quantify_scheduler.backends.qblox.compiler_abc"
        ):
            qcompile(sched, load_example_transmon_config(), hw_cfg)

        # Assert
        answer = (
            "Latency correction of 2 ns specified for seq0 of qcm0, which is "
            "not a multiple of 4 ns. This feature should be considered "
            "experimental and stable results are not guaranteed at this stage."
        )
        assert answer in caplog.messages


def _strip_comments(program: str):
    # helper function for comparing programs
    stripped_program = []
    for line in program.split("\n"):
        if "#" in line:
            line = line.split("#")[0]
        line = line.rstrip()  # remove trailing whitespace
        stripped_program.append(line)
    return stripped_program
