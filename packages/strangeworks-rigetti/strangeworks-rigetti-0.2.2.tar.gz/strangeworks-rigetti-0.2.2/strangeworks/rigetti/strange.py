import strangeworks
from typing import List, Optional
from .qc import QuantumComputer
from qcs_api_client.client import QCSClientConfiguration
import pyquil


def list_quantum_computers(
    qpus: bool = True,
    qvms: bool = True,
    timeout: float = 10.0,
    client_configuration: Optional[QCSClientConfiguration] = None,
) -> List[str]:
    res = []
    backends = strangeworks.client.circuit_runner.get_backends(pprint=False)
    for b in backends:
        if "rigetti" in b.selector_id():
            res.append(b.selector_id().replace("rigetti.", ""))
    return res


def get_qc(
    name: str,
    as_qvm: Optional[bool] = None,
    noisy: Optional[bool] = None,
    compiler_timeout: float = 10.0,
    execution_timeout: float = 10.0,
    client_configuration: Optional[QCSClientConfiguration] = None,
) -> QuantumComputer:
    ogc = pyquil.get_qc(
        name=name,
        as_qvm=as_qvm,
        noisy=noisy,
        compiler_timeout=compiler_timeout,
        execution_timeout=execution_timeout,
        client_configuration=client_configuration,
    )
    return QuantumComputer(ogc, as_qvm=as_qvm)
