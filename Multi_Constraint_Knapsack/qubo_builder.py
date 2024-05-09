import numpy as np

def build_qubo(data):
    
    count_of_elements = data["num_items"]
    
    number_of_slack_bits_weight = int(np.round(np.log2(data["max_weight"] + 1)))
    
    number_of_slack_bits_cores = int(np.round(np.log2(data["max_cores"] + 1)))
    
    total_count_of_slack_bits = count_of_elements + number_of_slack_bits_weight + number_of_slack_bits_cores

    data_values_array = np.array(data["values"] + [0 for _ in range(total_count_of_slack_bits)])
        
    data_weights_array = np.array(data["weights"] + [2**k for k in range(number_of_slack_bits_weight)] + [0 for _ in range(number_of_slack_bits_cores)])
    
    data_cores_array = np.array(data["cores"] + [0 for _ in range(number_of_slack_bits_weight)] + [2**k for k in range(number_of_slack_bits_cores)])
    
    Q = np.zeros((total_count_of_slack_bits, total_count_of_slack_bits))
    
    offset = data["first_lambda"] * (data["max_weight"] ** 2 + data["max_cores"] ** 2)
    
    for i in range(total_count_of_slack_bits):
        # заполнение диагонали
        Q[i][i] += -data_values_array[i] 
        Q[i][i] += -data["first_lambda"] * data_weights_array[i] * (2 * data["max_weight"] - data_weights_array[i])
        Q[i][i] += -data["second_lambda"] * data_cores_array[i] * (2 * data["max_cores"] - data_cores_array[i])
        for j in range(i + 1, total_count_of_slack_bits):
            # заполнение вне диагонали
            Q[i][j] += 2 * data["first_lambda"] * data_weights_array[i] * data_weights_array[j]
            Q[i][j] += 2 * data["second_lambda"] * data_cores_array[i] * data_cores_array[j]
    return Q, offset