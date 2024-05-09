import qubo_solver as solver
import os

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
data["max_weight"] = 150
data["max_cores"] = 48
data["num_items"] = len(data["values"])

data["dwave_response"] = solver.qubo_solver(data, 1000)

data["os_save_path"] = os.path.join(os.getcwd() + '\\Multi_Constraint_Knapsack\\data\\test_1\\')

data["first_sample_data_vector"] = []

for i in range(data["num_items"]):
    if (data["dwave_response"].first.sample.get(i) == 1):
        data["first_sample_data_vector"].append(i)

file_to_save = open(data["os_save_path"] + 'test_1.txt', 'w')
file_to_save.write(' '.join(str(item) for item in data["first_sample_data_vector"]) + '\n')