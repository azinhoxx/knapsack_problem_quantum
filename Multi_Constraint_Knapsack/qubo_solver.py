from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler

import qubo_builder as build

def qubo_solver(data, num_reads):
    
    Q, offset = build.build_qubo(data)
    
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=offset)
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads)
    
    return response