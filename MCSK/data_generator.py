from random import randint

file_values = open('data_values.txt', 'w')
file_weights = open('data_weights.txt', 'w')
file_cores = open('data_cores.txt', 'w')

data_items_cnt = randint(5, 10)
data_values = [randint(1, 10) for _ in range(data_items_cnt)]
data_weights = [randint(1, 10) for _ in range(data_items_cnt)]
data_cores = [randint(1, 10) for _ in range(data_items_cnt)]

file_values.write(' '.join(str(item) for item in data_values) + '\n')
file_weights.write(' '.join(str(item) for item in data_weights) + '\n')
file_cores.write(' '.join(str(item) for item in data_cores) + '\n')

file_weights.close()
file_values.close()
file_cores.close()