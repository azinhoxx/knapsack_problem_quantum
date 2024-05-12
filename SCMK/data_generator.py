from random import randint

# генерация стоимости предметов для одного рюкзака
# далее считаем, что такая стоимость и в других для i-го предмета
file_values = open('data_values.txt', 'w')
file_weights = open('data_weights.txt', 'w')

data_items_cnt = randint(1, 10)
data_values = [randint(1, 10) for _ in range(data_items_cnt)]
data_weights = [randint(1, 10) for _ in range(data_items_cnt)]

file_values.write(' '.join(str(item) for item in data_values) + '\n')
file_weights.write(' '.join(str(item) for item in data_weights) + '\n')

file_weights.close()
file_values.close()