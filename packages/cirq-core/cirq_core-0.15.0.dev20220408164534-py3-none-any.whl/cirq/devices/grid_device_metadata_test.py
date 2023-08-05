# Copyright 2022 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for GridDevicemetadata."""

import pytest
import cirq
import networkx as nx


def test_griddevice_metadata():
    qubits = cirq.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    isolated_qubits = [cirq.GridQubit(9, 9), cirq.GridQubit(10, 10)]
    gateset = cirq.Gateset(cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate, cirq.CZ)
    metadata = cirq.GridDeviceMetadata(qubit_pairs, gateset, all_qubits=qubits + isolated_qubits)
    expected_pairings = frozenset(
        {
            (cirq.GridQubit(0, 0), cirq.GridQubit(0, 1)),
            (cirq.GridQubit(0, 1), cirq.GridQubit(0, 2)),
            (cirq.GridQubit(0, 1), cirq.GridQubit(1, 1)),
            (cirq.GridQubit(0, 2), cirq.GridQubit(1, 2)),
            (cirq.GridQubit(1, 0), cirq.GridQubit(1, 1)),
            (cirq.GridQubit(1, 1), cirq.GridQubit(1, 2)),
            (cirq.GridQubit(0, 0), cirq.GridQubit(1, 0)),
        }
    )
    assert metadata.qubit_set == frozenset(qubits + isolated_qubits)
    assert metadata.qubit_pairs == expected_pairings
    assert metadata.gateset == gateset
    expected_graph = nx.Graph()
    expected_graph.add_nodes_from(sorted(list(qubits + isolated_qubits)))
    expected_graph.add_edges_from(sorted(list(expected_pairings)), directed=False)
    assert metadata.nx_graph.edges() == expected_graph.edges()
    assert metadata.nx_graph.nodes() == expected_graph.nodes()
    assert metadata.gate_durations is None
    assert metadata.isolated_qubits == frozenset(isolated_qubits)


def test_griddevice_metadata_bad_durations():
    qubits = tuple(cirq.GridQubit.rect(1, 2))

    gateset = cirq.Gateset(cirq.XPowGate, cirq.YPowGate)
    invalid_duration = {
        cirq.GateFamily(cirq.XPowGate): cirq.Duration(nanos=1),
        cirq.GateFamily(cirq.ZPowGate): cirq.Duration(picos=1),
    }
    with pytest.raises(ValueError, match="ZPowGate"):
        cirq.GridDeviceMetadata([qubits], gateset, gate_durations=invalid_duration)


def test_griddevice_metadata_bad_isolated():
    qubits = cirq.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    fewer_qubits = [cirq.GridQubit(0, 0)]
    gateset = cirq.Gateset(cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate, cirq.CZ)
    with pytest.raises(ValueError, match='node_set'):
        _ = cirq.GridDeviceMetadata(qubit_pairs, gateset, all_qubits=fewer_qubits)


def test_griddevice_self_loop():
    bad_pairs = [
        (cirq.GridQubit(0, 0), cirq.GridQubit(0, 0)),
        (cirq.GridQubit(1, 0), cirq.GridQubit(1, 1)),
    ]
    with pytest.raises(ValueError, match='Self loop'):
        _ = cirq.GridDeviceMetadata(bad_pairs, cirq.Gateset(cirq.XPowGate))


def test_griddevice_json_load():
    qubits = cirq.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = cirq.Gateset(cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate)
    duration = {
        cirq.GateFamily(cirq.XPowGate): cirq.Duration(nanos=1),
        cirq.GateFamily(cirq.YPowGate): cirq.Duration(picos=2),
        cirq.GateFamily(cirq.ZPowGate): cirq.Duration(picos=3),
    }
    isolated_qubits = [cirq.GridQubit(9, 9), cirq.GridQubit(10, 10)]
    metadata = cirq.GridDeviceMetadata(
        qubit_pairs, gateset, gate_durations=duration, all_qubits=qubits + isolated_qubits
    )
    rep_str = cirq.to_json(metadata)
    assert metadata == cirq.read_json(json_text=rep_str)


def test_griddevice_metadata_equality():
    qubits = cirq.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = cirq.Gateset(cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate)
    duration = {
        cirq.GateFamily(cirq.XPowGate): cirq.Duration(nanos=1),
        cirq.GateFamily(cirq.YPowGate): cirq.Duration(picos=3),
        cirq.GateFamily(cirq.ZPowGate): cirq.Duration(picos=2),
    }
    duration2 = {
        cirq.GateFamily(cirq.XPowGate): cirq.Duration(nanos=10),
        cirq.GateFamily(cirq.YPowGate): cirq.Duration(picos=13),
        cirq.GateFamily(cirq.ZPowGate): cirq.Duration(picos=12),
    }
    isolated_qubits = [cirq.GridQubit(9, 9)]
    metadata = cirq.GridDeviceMetadata(qubit_pairs, gateset, gate_durations=duration)
    metadata2 = cirq.GridDeviceMetadata(qubit_pairs[:2], gateset, gate_durations=duration)
    metadata3 = cirq.GridDeviceMetadata(qubit_pairs, gateset, gate_durations=None)
    metadata4 = cirq.GridDeviceMetadata(qubit_pairs, gateset, gate_durations=duration2)
    metadata5 = cirq.GridDeviceMetadata(reversed(qubit_pairs), gateset, gate_durations=duration)
    metadata6 = cirq.GridDeviceMetadata(
        qubit_pairs, gateset, gate_durations=duration, all_qubits=qubits + isolated_qubits
    )

    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(metadata)
    eq.add_equality_group(metadata2)
    eq.add_equality_group(metadata3)
    eq.add_equality_group(metadata4)
    eq.add_equality_group(metadata6)

    assert metadata == metadata5


def test_repr():
    qubits = cirq.GridQubit.rect(2, 3)
    qubit_pairs = [(a, b) for a in qubits for b in qubits if a != b and a.is_adjacent(b)]
    gateset = cirq.Gateset(cirq.XPowGate, cirq.YPowGate, cirq.ZPowGate)
    duration = {
        cirq.GateFamily(cirq.XPowGate): cirq.Duration(nanos=1),
        cirq.GateFamily(cirq.YPowGate): cirq.Duration(picos=3),
        cirq.GateFamily(cirq.ZPowGate): cirq.Duration(picos=2),
    }
    isolated_qubits = [cirq.GridQubit(9, 9)]
    metadata = cirq.GridDeviceMetadata(
        qubit_pairs, gateset, gate_durations=duration, all_qubits=qubits + isolated_qubits
    )
    cirq.testing.assert_equivalent_repr(metadata)
