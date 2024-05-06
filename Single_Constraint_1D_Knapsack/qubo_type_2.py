import numpy as np

# построение матрицы qubo для второго типа ограничений
# (P.S. смотреть доку прикреплённую к репозиторию)

def build_qubo(data_weights_list, data_values_list, max_weight, lambd):
    
    count_of_elements = len(data_values_list)
    
    number_of_slack_bits = int(np.round(np.log2(max_weight + 1)))
    
    total_count_of_bits = count_of_elements + number_of_slack_bits

    data_values_array = np.array(data_values_list + [0 for _ in range(number_of_slack_bits)])
        
    data_weights_array = np.array([-int(x) for x in data_weights_list] + [2**k for k in range(number_of_slack_bits - 1)] + [max_weight + 1 - 2**(number_of_slack_bits - 1)])
    
    Q = np.zeros((total_count_of_bits, total_count_of_bits))
    
    for i in range(total_count_of_bits):
        # заполнение диагонали
        Q[i][i] = -data_values_array[i] + lambd * data_weights_array[i] ** 2
        for j in range(i + 1, total_count_of_bits):
            if (i < count_of_elements and j < count_of_elements):
                Q[i][j] += 2 * lambd * data_weights_array[i] * data_weights_array[j]
            elif (i >= count_of_elements and j >= count_of_elements):
                Q[i][j] += 2 * lambd * data_weights_array[i] * data_weights_array[j]
            elif (i < count_of_elements and j >= count_of_elements):
                Q[i][j] -= 4 * lambd * data_weights_array[i] * data_weights_array[j]
    
    return Q