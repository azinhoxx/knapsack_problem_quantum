import os

import qubo_solver as solver
import solver_graph as graph

data = {}
    
def input(data):
    
    for line in open('data_memory.txt', 'r'):
        data["memory"] = [int(value) for value in line.split()]

    for line in open('data_space.txt', 'r'):
        data["space"] = [int(value) for value in line.split()]
        
    for line in open('data_cores.txt', 'r'):
        data["cores"] = [int(value) for value in line.split()]

# считываем данные
input(data)

assert(len(data["memory"]) == len(data["space"]))
assert(len(data["memory"]) == len(data["cores"]))

data["first_lambda"] = 10
data["second_lambda"] = 10
data["third_lambda"] = 10

data["max_space"] = 150
data["max_cores"] = 64
data["max_memory"] = 120

data["num_items"] = len(data["cores"])

data["num_reads"] = 1000

data["dwave_response"] = solver.qubo_solver(data)

data["os_save_path"] = os.path.join(os.getcwd() + '\\MCSKS\\data\\test_1\\')

data["first_sample_data_vector"] = []

for i in range(data["num_items"]):
    if (data["dwave_response"].first.sample.get(i) == 1):
        data["first_sample_data_vector"].append(i)

graph.build_graph(data, 1)