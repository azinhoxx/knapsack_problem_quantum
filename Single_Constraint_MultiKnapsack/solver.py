import os

import qubo_solver as solver

import numpy as np

# функция обработки входных данных

data = {}

def input(data):
    
    for line in open('data_values.txt', 'r'):
        data["values"] = [int(value) for value in line.split()]

    for line in open('data_weights.txt', 'r'):
        data["weights"] = [int(value) for value in line.split()]

# считываем данные
input(data)

assert(len(data["values"]) == len(data["weights"]))

data["max_weights"] = [10 for _ in range(2)]
data["num_items"] = len(data["values"])
data["num_knapsacks"] = len(data["max_weights"])

data["os_save_path"] = os.path.join(os.getcwd() + '\\Single_Constraint_MultiKnapsack\\data\\test_1')

# запускаем тестирование

data["dwave_response"] = solver.qubo_solver(data, 1000)

data["num_slack_bits_array"] = (np.floor(np.log2(np.array(data["max_weights"]))) + 1).astype(int)

data_graph = {}

data_graph["taken_items"] = [[] for _ in range(data["num_knapsacks"])]

# проход по рюкзаку
for j in range(data["num_knapsacks"]):
    # проверка на наличие соответствующего предмета
    for i in range(data["num_items"]):
        # определяем конкретный индекс
        index = j * data["num_items"] + data["num_slack_bits_array"][:j].sum() + i
        if (data["dwave_response"].first.sample.get(index) == 1):
            data_graph["taken_items"][j].append(i)