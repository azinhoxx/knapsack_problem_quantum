import numpy as np
# import dwave.system
from matplotlib import pyplot as plt
# from dwave_qbsolv import QBSolv
from tabu import TabuSampler
import dimod
# from dwave.samplers import SimulatedAnnealingSamplerW

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

def default_algorithm(weights_array, values_array, count_items, max_weight):
    A = [[0 for _ in range(max_weight + 1)] for _ in range(count_items + 1)]
    for k in range(1, count_items + 1):
        for s in range(1, max_weight + 1):
            if s >= weights_array[k - 1]:
                A[k][s] = max(A[k - 1][s], A[k - 1][s - weights_array[k - 1]] + values_array[k - 1])
            else:
                A[k][s] = A[k - 1][s]
    return A[count_items][max_weight]


lambd = 2

max_weight = 500

number_of_slack = round(np.ceil(np.log2(max_weight)))

offset = lambd * max_weight ** 2

for test in range(len(data_values_list)):
    count_of_elements = len(data_values_list[test])
    
    values_array = np.array(data_values_list[test] + [0 for _ in range(number_of_slack)])
        
    weights_array = np.array(data_weights_list[test] + [2**k for k in range(number_of_slack)])
    
    Q = buildQUBO(count_of_elements, number_of_slack, weights_array, values_array, lambd, max_weight)

    # sampler = dwave.system.EmbeddingComposite(dwave.system.DWaveSampler())
    # response = sampler.sample_qubo(Q, num_reads = 1000)
    ###
    # response = QBSolv().sample_qubo(Q)
    ###
    # sampler = SimulatedAnnealingSampler()
    # response = sampler.sample_qubo(Q, num_reads = 500)
    
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    response = TabuSampler().sample(bqm, num_reads = 200)

    dwave_answers.append(-(response.first.energy + offset))
    
    correct_answers.append(default_algorithm(weights_array, values_array, count_of_elements, max_weight))

y1 = dwave_answers
y2 = correct_answers

plt.plot(y1, color="red")

plt.plot(y2, color="blue")

plt.show()