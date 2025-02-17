from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler

import time

import qubo_builder as build

def qubo_solver(data):
    
    Q, offset = build.build_qubo(data)
        
    bqm = BinaryQuadraticModel.from_qubo(Q, offset=offset)
    
    seconds_before = time.time()
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=data["num_reads"])
    
    second_after = time.time()
    
    data["response_time"] = round(second_after - seconds_before, 2)
    
    return response