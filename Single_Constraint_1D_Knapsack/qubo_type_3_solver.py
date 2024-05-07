from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler
import time

import qubo_type_3 as type_3

def solver(data, num_reads):
    
    Q = type_3.build_qubo(data)
    
    bqm = BinaryQuadraticModel.from_qubo(Q)

    seconds_before = time.time()
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads)
    
    seconds_after = time.time()
    
    offset = data["max_weight"] ** 2 * data["first_lambda"]
    
    answer = -(response.first.energy + offset)
    
    total_time = seconds_after - seconds_before
        
    return answer, total_time