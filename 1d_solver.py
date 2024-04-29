import numpy as np
from tabu import TabuSampler
import dimod

dwave_answers = []

correct_answers = []

data_values_list = []

for line in open('data_values.txt', 'r'):
    data_values_list.append([int(value) for value in line.split()])

data_weights_list = []

for line in open('data_weights.txt', 'r'):
    data_weights_list.append([int(value) for value in line.split()])
    

def buildQUBO(count_of_elements, number_of_slack, weights_array, values_array, lambd, max_weight):

    Q = np.zeros((count_of_elements + number_of_slack, count_of_elements + number_of_slack))

    np.fill_diagonal(Q, -values_array)

    diag_values = lambd * weights_array * (weights_array - 2 * max_weight)

    np.fill_diagonal(Q, Q.diagonal() + diag_values)

    off_diag_values = np.triu(np.outer(2 * lambd * weights_array, weights_array), k=1)

    Q += off_diag_values
    
    return Q

file_output_count = open('file_output_count.txt', 'w')

file_output_answers = open('file_output_answers.txt', 'w')

file_output_spins = open('file_output_spins.txt', 'w')

file_output_max_weight_constraint = open('file_output_max_weight_constraint.txt', 'w')

for test in range(len(data_values_list)):
    lambd = max([int(x) for x in data_values_list[test]]) + 1
    
    max_weight = 1500 + test * 75
    
    number_of_slack = round(np.ceil(np.log2(max_weight)))
    
    offset = lambd * max_weight ** 2
    
    count_of_elements = len(data_values_list[test])
        
    values_array = np.array(data_values_list[test] + [0 for _ in range(number_of_slack)])
            
    weights_array = np.array(data_weights_list[test] + [2**k for k in range(number_of_slack)])
    
    Q = buildQUBO(count_of_elements, number_of_slack, weights_array, values_array, lambd, max_weight)
    
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
        
    response = TabuSampler().sample(bqm, num_reads = 1000)
        
    dwave_answers.append(-(response.first.energy + offset))
    
    file_output_count.write(str(len(data_values_list[test])) + ' ')
    
    file_output_answers.write(str(-(response.first.energy + offset)) + ' ')
    
    file_output_max_weight_constraint.write(str(max_weight) + ' ')
    
    for key in response.first[0]:
        if (response.first[0][key] == 1):
            file_output_spins.write(str(key) + ' ')
            
    file_output_spins.write('\n')
    
    file_output_answers.write('\n')
    
    file_output_count.write('\n')
    
    file_output_max_weight_constraint.write('\n')
    
    