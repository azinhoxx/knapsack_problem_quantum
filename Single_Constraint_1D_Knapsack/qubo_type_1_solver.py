from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler

import time

import qubo_type_1 as type_1

def solver(data_weights_list, data_values_list, max_weight, lambd, num_reads):
    
    Q = type_1.build_qubo(data_weights_list, data_values_list, max_weight, lambd)
    
    bqm = BinaryQuadraticModel.from_qubo(Q)
    
    seconds_before = time.time()
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads)
    
    seconds_after = time.time()
    
    offset = max_weight ** 2 * lambd
    
    answer = -(response.first.energy + offset)
    
    total_time = seconds_after - seconds_before
    
    return answer, total_time