import numpy as np
from itertools import combinations

def build_qubo(data):
        data_max_space_list = np.array(data["max_space"])
        data_max_memory_list = np.array(data["max_memory"])
        data_max_cores_list = np.array(data["max_cores"])
    
        num_knapsacks = len(data_max_space_list)
        
        num_items = data["num_items"]
    
        # создаём для удобства двумерный массив
        # для более широкой постановки можно изменить реализацию
        # на произвольные значения для каждого из рюкзаков
        data_space_array = [data["space"] for _ in range(num_knapsacks)]
        data_memory_array = [data["memory"] for _ in range(num_knapsacks)]
        data_cores_array = [data["cores"] for _ in range(num_knapsacks)]
        
        # определяем соответствующие коэффициенты
        # betta_1 = 2 * np.max(np.concatenate(data_space_array).ravel()) + 1
        # betta_2 = 2 * np.max(np.concatenate(data_memory_array).ravel()) + 1
        # betta_3 = 2 * np.max(np.concatenate(data_cores_array).ravel()) + 1
        # alpha = max(betta_1, betta_2, betta_3)
        betta_1 = 10
        betta_2 = 10
        betta_3 = 10
        alpha = 10
        gamma = 1 
    
        # количество дополнительных битов для каждого рюкзака по отдельности
        num_slack_bits = data["total_num_slack_bits_array"]
        
        # общее количество переменных
        num_qubits = (num_items * num_knapsacks + num_slack_bits.sum()).astype(int)

        Q = np.zeros((num_qubits, num_qubits))

        # заполнение диагональных элементов
        for i in range(num_knapsacks):

            # в терминах x_ij
            for j in range(num_items):
                # вычисление индекса на диагонали
                index = i * num_items + num_slack_bits[:i].sum() + j
                # заполняем диагональ (максимизация используемых ресурсов)
                Q[index][index] += betta_1 * data_space_array[i][j] ** 2 - 2 * betta_1 * data_max_space_list[i] * data_space_array[i][j] - gamma * data_space_array[i][j]
                Q[index][index] += betta_2 * data_memory_array[i][j] ** 2 - 2 * betta_2 * data_max_memory_list[i] * data_memory_array[i][j] - gamma * data_memory_array[i][j]
                Q[index][index] += betta_3 * data_cores_array[i][j] ** 2 - 2 * betta_3 * data_max_cores_list[i] * data_cores_array[i][j] - gamma * data_cores_array[i][j]

            # в терминах a_ib -- заполнение диагонали (огр. диска)
            for b in range(data["num_slack_bits_array_space"][i]):
                index = (i + 1) * num_items + num_slack_bits[:i].sum() + b
                Q[index][index] = betta_1 * 2 ** (2 * b) - 2 * betta_1 * data_max_space_list[i] * 2 ** b
                
            # в терминах b_ib -- заполнение диагонали (огр. оперативной памяти)
            for b in range(data["num_slack_bits_array_memory"][i]):
                index = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + b
                Q[index][index] = betta_2 * 2 ** (2 * b) - 2 * betta_2 * data_max_memory_list[i] * 2 ** b
                
            # в терминах c_ib -- заполнение диагонали (огр. ядер)
            for b in range(data["num_slack_bits_array_cores"][i]):
                index = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + data["num_slack_bits_array_memory"][i] + b
                Q[index][index] = betta_3 * 2 ** (2 * b) - 2 * betta_3 * data_max_cores_list[i] * 2 ** b

        # создаём всевозможные пары предметов
        knapsack_ind_pairs = list(combinations(range(num_knapsacks), 2))
        item_ind_pairs = list(combinations(range(num_items), 2))

        slack_ind_pairs_space = []
        for i in range(num_knapsacks):
            slack_ind_pairs_space.append(list(combinations(range(data["num_slack_bits_array_space"][i]), 2)))
    
        slack_ind_pairs_memory = []
        for i in range(num_knapsacks):
            slack_ind_pairs_memory.append(list(combinations(range(data["num_slack_bits_array_memory"][i]), 2)))
    
        slack_ind_pairs_cores = []
        for i in range(num_knapsacks):
            slack_ind_pairs_cores.append(list(combinations(range(data["num_slack_bits_array_cores"][i]), 2)))

        # пенальти на вне диагональные элементы: нельзя быть в нескольких рюкзаках одновременно
        for j in range(num_items):
            for pair in knapsack_ind_pairs:
                index1 = pair[0] * num_items + num_slack_bits[:pair[0]].sum() + j
                index2 = pair[1] * num_items + num_slack_bits[:pair[1]].sum() + j
                Q[index1][index2] = 2 * alpha

        # пенальти на все ограничения для xx
        for i in range(num_knapsacks):
            for pair in item_ind_pairs:
                index1 = i * num_items + num_slack_bits[:i].sum() + pair[0]
                index2 = i * num_items + num_slack_bits[:i].sum() + pair[1]
                Q[index1][index2] += 2 * betta_1 * data_space_array[i][pair[0]] * data_space_array[i][pair[1]]
                Q[index1][index2] += 2 * betta_2 * data_memory_array[i][pair[0]] * data_memory_array[i][pair[1]]
                Q[index1][index2] += 2 * betta_3 * data_cores_array[i][pair[0]] * data_cores_array[i][pair[1]]

        # пенальти на ограничения для yy
        for i in range(num_knapsacks):
            # вместительность диска
            for pair in slack_ind_pairs_space[i]:
                index1 = (i + 1) * num_items + num_slack_bits[:i].sum() + pair[0]
                index2 = (i + 1) * num_items + num_slack_bits[:i].sum() + pair[1]
                Q[index1][index2] = 2 * betta_1 * 2 ** (pair[0] + pair[1])
            
            # вместительность оперативной памяти
            for pair in slack_ind_pairs_memory[i]:
                index1 = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + pair[0]
                index2 = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + pair[1]
                Q[index1][index2] = 2 * betta_2 * 2 ** (pair[0] + pair[1])
            
            # вместительность по количеству ядер
            for pair in slack_ind_pairs_cores[i]:
                index1 = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + data["num_slack_bits_array_memory"][i] + pair[0]
                index2 = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + data["num_slack_bits_array_memory"][i] + pair[1]
                Q[index1][index2] = 2 * betta_3 * 2 ** (pair[0] + pair[1])

        # пенальти на вместительность на xy
        for i in range(num_knapsacks):
            for j in range(num_items):   
    
                # вместительность по диску
                for b in range(data["num_slack_bits_array_space"][i]):
                    index1 = i * num_items + num_slack_bits[:i].sum() + j
                    index2 = (i + 1) * num_items + num_slack_bits[:i].sum() + b
                    Q[index1][index2] = 2 * betta_1 * data_space_array[i][j] * 2 ** b
                
                # вместительность по оперативной памяти
                for b in range(data["num_slack_bits_array_memory"][i]):
                    index1 = i * num_items + num_slack_bits[:i].sum() + j
                    index2 = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + b
                    Q[index1][index2] = 2 * betta_2 * data_memory_array[i][j] * 2 ** b
                
                # вместительность по количеству ядер
                for b in range(data["num_slack_bits_array_cores"][i]):
                    index1 = i * num_items + num_slack_bits[:i].sum() + j
                    index2 = (i + 1) * num_items + num_slack_bits[:i].sum() + data["num_slack_bits_array_space"][i] + data["num_slack_bits_array_memory"] + b
                    Q[index1][index2] = 2 * betta_3 * data_cores_array[i][j] * 2 ** b

        offset = betta_1 * (data_max_space_list ** 2).sum()
        offset += betta_2 * (data_max_memory_list ** 2).sum()
        offset += betta_3 * (data_max_cores_list ** 2).sum()

        return Q, offset