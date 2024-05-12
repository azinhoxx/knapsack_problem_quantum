import os

import qubo_solver as solver
import solver_graph as graph

data = {}

def input(data):
    
    for line in open('data_values.txt', 'r'):
        data["values"] = [int(value) for value in line.split()]

    for line in open('data_weights.txt', 'r'):
        data["weights"] = [int(value) for value in line.split()]
        
    for line in open('data_cores.txt', 'r'):
        data["cores"] = [int(value) for value in line.split()]

# считываем данные
input(data)

assert(len(data["values"]) == len(data["weights"]))

data["first_lambda"] = 10
data["second_lambda"] = 100
data["max_weight"] = 1024
data["max_cores"] = 128
data["num_items"] = len(data["values"])

data["num_reads"] = 100000

data["dwave_response"] = solver.qubo_solver(data, data["num_reads"])

data["os_save_path"] = os.path.join(os.getcwd() + '\\MCSK\\data\\test_3\\')

data["first_sample_data_vector"] = []

for i in range(data["num_items"]):
    if (data["dwave_response"].first.sample.get(i) == 1):
        data["first_sample_data_vector"].append(i)
        
graph.build_graph(data, 5)