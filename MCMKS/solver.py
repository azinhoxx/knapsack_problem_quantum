import os

import qubo_solver as solver

import solver_graph
import multi_solver_graph

import numpy as np

# функция обработки входных данных

data = {}

def input(data):
    
    for line in open('data_cores.txt', 'r'):
        data["cores"] = [int(value) for value in line.split()]

    for line in open('data_space.txt', 'r'):
        data["space"] = [int(value) for value in line.split()]
        
    for line in open('data_memory.txt', 'r'):
        data["memory"] = [int(value) for value in line.split()]

# считываем данные
input(data)

assert(len(data["cores"]) == len(data["space"]))
assert(len(data["cores"]) == len(data["memory"]))

data["max_space"] = [1024 for _ in range(8)]
data["max_cores"] = [196 for _ in range(8)]
data["max_memory"] = [512 for _ in range(8)]

assert(len(data["max_space"]) == len(data["max_cores"]))
assert(len(data["max_cores"]) == len(data["max_memory"]))

data["num_items"] = len(data["space"])
data["num_knapsacks"] = len(data["max_space"])

# запускаем тестирование

data["total_num_slack_bits_array"] = (np.floor(np.log2(np.array(data["max_memory"]))) + 1
                                      + np.floor(np.log2(np.array(data["max_cores"]))) + 1
                                      + np.floor(np.log2(np.array(data["max_space"]))) + 1).astype(int)

data["num_slack_bits_array_memory"] = (np.floor(np.log2(np.array(data["max_memory"]))) + 1).astype(int)
data["num_slack_bits_array_space"] = (np.floor(np.log2(np.array(data["max_space"]))) + 1).astype(int)
data["num_slack_bits_array_cores"] = (np.floor(np.log2(np.array(data["max_cores"]))) + 1).astype(int)

data['num_reads'] = 10
data["dwave_response"] = solver.qubo_solver(data)

data_graph = {}

data_graph["taken_items"] = [[] for _ in range(data["num_knapsacks"])]

# проход по рюкзаку
for j in range(data["num_knapsacks"]):
    # проверка на наличие соответствующего предмета
    for i in range(data["num_items"]):
        # определяем конкретный индекс
        index = j * data["num_items"] + data["total_num_slack_bits_array"][:j].sum() + i
        if (data["dwave_response"].first.sample.get(index) == 1):
            data_graph["taken_items"][j].append(i)
            
data["os_save_path"] = os.path.join(os.getcwd() + '\MCMKS\\data\\test_5')

print(data["dwave_response"].first)

# multi_solver_graph.build_graph(data, data_graph, 1)