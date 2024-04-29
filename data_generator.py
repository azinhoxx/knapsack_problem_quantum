from random import randint

file_values = open('data_values.txt', 'w')
file_weights = open('data_weights.txt', 'w')

for _ in range(10):
    data_items_cnt = randint(1e2, 1e3)
    data_values = [randint(1, 1e3) for _ in range(data_items_cnt)]
    data_weights = [randint(1, 1e3) for _ in range(data_items_cnt)]
    file_values.write(' '.join(str(item) for item in data_values) + '\n')
    file_weights.write(' '.join(str(item) for item in data_weights) + '\n')

file_weights.close()
file_values.close()
    