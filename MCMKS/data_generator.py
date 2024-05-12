from random import randint

file_memory = open('data_memory.txt', 'w')
file_space = open('data_space.txt', 'w')
file_cores = open('data_cores.txt', 'w')

data_items_cnt = randint(5, 10)
data_memory = [randint(1, 10) for _ in range(data_items_cnt)]
data_weights = [randint(1, 20) for _ in range(data_items_cnt)]
data_cores = [randint(1, 10) for _ in range(data_items_cnt)]

file_memory.write(' '.join(str(item) for item in data_memory) + '\n')
file_space.write(' '.join(str(item) for item in data_weights) + '\n')
file_cores.write(' '.join(str(item) for item in data_cores) + '\n')

file_space.close()
file_memory.close()
file_cores.close()