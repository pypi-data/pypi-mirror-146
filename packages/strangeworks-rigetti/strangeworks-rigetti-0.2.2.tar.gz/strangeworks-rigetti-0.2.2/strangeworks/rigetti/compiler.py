import pyquil
from pyquil.api import AbstractCompiler, QuantumExecutable
from pyquil.api import QPUCompiler, QuantumComputer, WavefunctionSimulator
from pyquil.quil import Program
from typing import Optional
import strangeworks

from strangeworks.rigetti.program import CompiledProgram


class StrangeworksCompiler(AbstractCompiler):
    def __init__(self, target: str, as_qvm: str):
        self.target = target
        self.as_qvm = as_qvm

    def quil_to_native_quil(
        self, prg: Program, *, protoquil: Optional[bool] = None
    ) -> CompiledProgram:
        payload = self.__serialize_program(prg)
        payload["target"] = self.target
        shots = prg.num_shots
        if shots is None:
            shots = 1
        payload["shots"] = shots
        res = strangeworks.client.rest_client.post(
            "/plugins/rigetti/compile?return_executable=False", json=payload
        )
        return CompiledProgram.from_json(program=prg, payload=res)

    def native_quil_to_executable(self, nq_program: Program) -> QuantumExecutable:
        payload = self.__serialize_program(nq_program)
        payload["target"] = self.target
        shots = nq_program.num_shots
        if shots is None:
            shots = 1
        payload["shots"] = shots
        res = strangeworks.client.rest_client.post(
            "/plugins/rigetti/compile?return_executable=True", json=payload
        )
        return CompiledProgram.from_json(program=nq_program, payload=res)

    def get_calibration_program(self, force_refresh: bool = False) -> Program:
        payload = {
            "as_qvm": self.as_qvm,
            "circuit": "",
            "circuit_type": "pyquil.Program",
            "version": pyquil.pyquil_version,
        }
        payload["target"] = self.target
        res = strangeworks.client.rest_client.post(
            "/plugins/rigetti/compile?get_calibration_program=True", json=payload
        )
        return CompiledProgram.from_json(program=None, payload=res)

    def __serialize_program(self, p: Program) -> dict:
        return {
            "as_qvm": self.as_qvm,
            "circuit": p.out(calibrations=False),
            "circuit_type": "pyquil.Program",
            "version": pyquil.pyquil_version,
        }
