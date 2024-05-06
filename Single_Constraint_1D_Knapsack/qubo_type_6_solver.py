from dimod import BinaryQuadraticModel
from neal import SimulatedAnnealingSampler
import time

import qubo_type_6 as type_6

def solver(data_weights_list, data_values_list, max_weight, lambd1, lambd2, num_reads):
    
    Q = type_6.build_qubo(data_weights_list, data_values_list, max_weight, lambd1, lambd2)
    
    bqm = BinaryQuadraticModel.from_qubo(Q)    
    
    seconds_before = time.time()
    
    response = SimulatedAnnealingSampler().sample(bqm, num_reads=num_reads)
    
    seconds_after = time.time()
    
    offset = max_weight ** 2 * lambd1 + lambd2
    
    answer = -(response.first.energy + offset)
    
    total_time = seconds_after - seconds_before
        
    return answer, total_time