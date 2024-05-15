from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler
from tabu import TabuSampler
import time

import qubo_builder as builder

def qubo_solver(data):
    Q, offset = builder.build_qubo(data)
    
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=offset)
    
    seconds_before = time.time()
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=data["num_reads"])
    
    seconds_after = time.time()
    
    data['response_time'] = round(seconds_after - seconds_before, 3)
    
    return response