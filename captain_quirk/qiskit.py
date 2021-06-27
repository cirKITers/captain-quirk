import json
from functools import singledispatch
from typing import List, Union
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.controlledgate import ControlledGate
from qiskit.circuit.library.standard_gates import HGate
from qiskit.circuit.library.standard_gates.rx import RXGate
from qiskit.circuit.library.standard_gates.ry import RYGate
from qiskit.circuit.library.standard_gates.rz import RZGate
from qiskit.circuit.library.standard_gates.x import XGate
from qiskit.circuit.library.standard_gates.y import YGate
from qiskit.circuit.library.standard_gates.z import ZGate
from qiskit.circuit.quantumregister import Qubit

from ._utils import AbstractSyntaxGrid, AbstractGate


def parse(url: str):
    """Takes a quirk URL and creates an appropriate qiskit circuit"""
    ...


def _parse_column(
    unparsed_gate: List[AbstractGate], placement: List[Qubit]
) -> List[Union[int, AbstractGate]]:
    column = []
    for gate_index, current_placement in enumerate(placement):
        qubit_index = current_placement.index
        while len(column) <= qubit_index:
            column.append(1)
        column[qubit_index] = unparsed_gate[gate_index]
    return column


@singledispatch
def unparse(circuit: QuantumCircuit) -> str:
    """Takes a qiskit circuit and returns the appropriate quirk URL"""
    if not isinstance(circuit, QuantumCircuit):
        raise NotImplementedError(f"Unparsing of object {circuit} is not implemented")
    columns = AbstractSyntaxGrid()
    for gate, placement, _ in circuit.data:
        unparsed_gate = convert(gate)
        assert len(unparsed_gate) == len(
            placement
        ), "length of gates and placement should be equal"
        new_column = _parse_column(unparsed_gate, placement)
        columns.append(new_column)
    return "https://algassert.com/quirk#circuit=" + json.dumps(
        {"cols": columns.to_json()}, separators=(",", ":")
    )


@singledispatch
def convert(gate: Union[HGate, XGate, YGate, ZGate]) -> List[AbstractGate]:
    return [AbstractGate(label=gate.name.upper())]


@convert.register
def _(gate: ControlledGate) -> List[AbstractGate]:
    result = []
    for _ in range(gate.num_ctrl_qubits):
        result.append(AbstractGate(label="•"))
    result.extend(convert(gate.base_gate))
    return result


@convert.register(RXGate)
@convert.register(RYGate)
@convert.register(RZGate)
def _(gate: Union[RXGate, RYGate, RZGate]) -> List[AbstractGate]:
    return [AbstractGate(label=gate.name.capitalize()+"ft", param=gate.params[0])]


if __name__ == "__main__":
    register = QuantumRegister(2)
    circuit = QuantumCircuit(register)
    circuit.crz(0.5, register[0], register[1])
    circuit.cx(register[1], register[0])
    print(circuit)
    print(unparse(circuit))
