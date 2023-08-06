from __future__ import annotations
from pyquil import Program
import base64
import pickle


class CompiledProgram(Program):
    def __init__(
        self,
        prg: Program,
        compiled_quil: str = None,
        encrypted_program: str = None,
        pickled_executable: str = None,
        digest: str = None,
    ):
        super().__init__(prg)
        self.compiled_quil = compiled_quil
        self.encrypted_program = encrypted_program
        self.pickled_executable = pickled_executable
        self.digest = digest

    @classmethod
    def from_json(cls, program: Program, payload: dict) -> CompiledProgram:
        pickled_executable = None
        digest = None
        if program is None:
            pickled_program = payload["pickled_program"]
            pickle_bytes = base64.b64decode(pickled_program)
            program = pickle.loads(pickle_bytes)
        if "pickled_executable" in payload:
            pickled_executable = payload["pickled_executable"]
            digest = payload["digest"]
        return cls(
            prg=program,
            compiled_quil=payload["compiled_quil"],
            pickled_executable=pickled_executable,
            digest=digest,
        )

    def to_dict(self) -> dict:
        return {
            "compiled_quil": self.compiled_quil,
            "encrypted_program": self.encrypted_program,
            "pickled_executable": self.pickled_executable,
            "digest": self.digest,
        }
