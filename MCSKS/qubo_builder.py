import numpy as np

def build_qubo(data):
        
    number_of_slack_bits_space = int(np.round(np.log2(data["max_space"] + 1)))
    
    number_of_slack_bits_cores = int(np.round(np.log2(data["max_cores"] + 1)))
    
    number_of_slack_bits_memory = int(np.round(np.log2(data["max_memory"] + 1)))
    
    total_count_of_slack_bits = data["num_items"] + number_of_slack_bits_space + number_of_slack_bits_cores + number_of_slack_bits_memory
        
    data_space_array = data["space"] + [2**k for k in range(number_of_slack_bits_space)] + [0 for _ in range(number_of_slack_bits_cores)] + [0 for _ in range(number_of_slack_bits_memory)]
    
    data_cores_array = data["cores"] + [0 for _ in range(number_of_slack_bits_space)] + [2**k for k in range(number_of_slack_bits_cores)] + [0 for _ in range(number_of_slack_bits_memory)]
    
    data_memory_array = data["memory"] + [0 for _ in range(number_of_slack_bits_space)] + [0 for _ in range(number_of_slack_bits_cores)] + [2**k for k in range(number_of_slack_bits_memory)]
    
    Q = np.zeros((total_count_of_slack_bits, total_count_of_slack_bits))
    
    offset = data["first_lambda"] * data["max_space"] ** 2
    
    offset += data["second_lambda"] * data["max_cores"] ** 2
    
    offset += data["third_lambda"] * data["max_memory"] ** 2
    
    for i in range(total_count_of_slack_bits):
        # заполнение диагонали
        if (i < data["num_items"]):
            Q[i][i] += -data_space_array[i] 
            Q[i][i] += -data_cores_array[i]
            Q[i][i] += -data_memory_array[i]
        Q[i][i] += -data["first_lambda"] * data_space_array[i] * (2 * data["max_space"] - data_space_array[i])
        Q[i][i] += -data["second_lambda"] * data_cores_array[i] * (2 * data["max_cores"] - data_cores_array[i])
        Q[i][i] += -data["third_lambda"] * data_memory_array[i] * (2 * data["max_memory"] - data_memory_array[i])
        for j in range(i + 1, total_count_of_slack_bits):
            # заполнение вне диагонали
            Q[i][j] += 2 * data["first_lambda"] * data_space_array[i] * data_space_array[j]
            Q[i][j] += 2 * data["second_lambda"] * data_cores_array[i] * data_cores_array[j]
            Q[i][j] += 2 * data["third_lambda"] * data_memory_array[i] * data_memory_array[j]
    return Q, offset