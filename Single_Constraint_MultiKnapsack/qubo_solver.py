from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler

import qubo_builder as builder

def solver(data, num_reads):
    Q, offset = builder.build_qubo(data)
    
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=offset)
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads)
    
    return -response.first.energy