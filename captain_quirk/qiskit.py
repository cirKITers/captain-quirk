import json
from functools import singledispatch
from typing import List, Union
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import HGate
from qiskit.circuit.library.standard_gates.x import CXGate, XGate
from qiskit.circuit.library.standard_gates.y import YGate
from qiskit.circuit.library.standard_gates.z import ZGate
from qiskit.circuit.quantumregister import Qubit

from ._utils import AbstractSyntaxGrid


def parse(url: str):
    """Takes a quirk URL and creates an appropriate qiskit circuit"""
    ...


def _parse_column(
    unparsed_gate: List[str], placement: List[Qubit]
) -> List[Union[int, str]]:
    column = []
    for gate_index, current_placement in enumerate(placement):
        qubit_index = current_placement.index
        while len(column) <= qubit_index:
            column.append(1)
        column[qubit_index] = unparsed_gate[gate_index]
    return column


@singledispatch
def unparse(circuit: QuantumCircuit) -> Union[str, List[str]]:
    """Takes a qiskit circuit and returns the appropriate quirk URL"""
    columns = AbstractSyntaxGrid()
    for gate, placement, _ in circuit.data:
        unparsed_gate = unparse(gate)
        print(f"{unparsed_gate} at {placement}")
        if isinstance(unparsed_gate, str):  # ensure equal treatment
            unparsed_gate = [unparsed_gate]
            assert len(unparsed_gate) == len(
                placement
            ), "length of gates and placement should be equal"
        new_column = _parse_column(unparsed_gate, placement)
        columns.append(new_column)
    return "https://algassert.com/quirk#circuit=" + json.dumps(
        {"cols": columns.to_json()}, separators=(",", ":")
    )


@unparse.register
def _(gate: HGate) -> str:
    return "H"


@unparse.register
def _(gate: XGate) -> str:
    return "X"


@unparse.register
def _(gate: CXGate) -> List[str]:
    return ["•", "X"]


@unparse.register
def _(gate: YGate) -> str:
    return "Y"


@unparse.register
def _(gate: ZGate) -> str:
    return "Z"


if __name__ == "__main__":
    register = QuantumRegister(2)
    circuit = QuantumCircuit(register)
    circuit.h(register)
    circuit.cx(register[1], register[0])
    print(circuit)
    print(unparse(circuit))
