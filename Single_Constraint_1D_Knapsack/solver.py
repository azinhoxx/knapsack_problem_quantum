import dp_solver as dp
import os

import solver_test as test
import solvet_test_lambda as test_lambda

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

data["first_lambda"] = 10
data["max_weight"] = 2000
data["num_items"] = len(data["values"])

data["correct_answer"] = dp.dp_solver(data)

data_graph = {}

data_graph["first_qubo_percents"] = []
data_graph["first_qubo_timer"] = []
data_graph["num_reads"] = []

data["os_save_path"] = os.path.join(os.getcwd() + '\\Single_Constraint_1D_Knapsack\\data\\test_3')

# запускаем тестирование
for test_i in range(1, 2): 
    test.solver_test(data, data_graph, 1000, 5000, 1500, 2)