import matplotlib.pyplot as plt

import dp_solver as dp

import qubo_type_1_solver

# функция обработки входных данных

def input():
    data_weights_list = []
    data_values_list = []
    
    for line in open('data_values.txt', 'r'):
        data_values_list = [int(value) for value in line.split()]

    for line in open('data_weights.txt', 'r'):
        data_weights_list = [int(value) for value in line.split()]
    
    return data_values_list, data_weights_list

# считываем данные
data_weights_list, data_values_list = input()

lambd1 = 10

max_weight = 300

correct_answer = dp.dp_solver(data_weights_list, data_values_list, max_weight)

data_qubo_1_percents = []

data_qubo_1_time = []

data_qubo_3_percents = []

data_qubo_3_time = []

num_reads_array = []

reads = 10000

# запускаем тестирование
for num_reads in range(reads, 10 * reads, reads):
    
    qubo_1_answer, qubo_1_time = qubo_type_1_solver.solver(data_weights_list, data_values_list, max_weight, lambd1, num_reads)
        
    data_qubo_1_percents += [qubo_1_answer / correct_answer * 100]
    
    data_qubo_1_time += [qubo_1_time]
    
    num_reads_array += [num_reads]

fig, axs = plt.subplots(2, 2)

count_of_items = len(data_weights_list)

# создаём надпись на Oy
axs[0, 0].set_ylabel('Вес предмета')

# заголовок
axs[0, 0].set_title('Распределение веса')

# создаём график распределения веса
axs[0, 0].scatter([int(x) for x in range(1, count_of_items + 1)], data_weights_list, color="r", linewidth=.2, label="Предметы")

# создаём ограничение на оси
axs[0, 0].set_xlim(0, count_of_items + 1)
axs[0, 0].set_ylim(0, max(data_weights_list) + 1)

# скрываем значения по Ox
axs[0, 0].axes.get_xaxis().set_visible(False)

# графики и описание
axs[0, 1].plot(num_reads_array, data_qubo_1_percents, 'r--')

# заголовок
axs[0, 1].set_title('Точность работы')
axs[0, 1].set_ylabel('Точность, %')

axs[0, 1].set_ylim(0, 110)
axs[0, 1].set_xlim(0, max(num_reads_array) + 1)

# заголовок
axs[1, 0].set_title('Временная сложность')
axs[1, 0].set_ylabel('Время работы, s')

# графики и описание
axs[1, 0].plot(num_reads_array, data_qubo_1_time, 'r--')

for ax in axs.flat[2:3]:
    ax.set(xlabel="num_reads")
    
# создаём надпись на Oy
axs[1, 1].set_ylabel('Стоимость предмета')

# заголовоки
axs[1, 1].set_title('Распределение стоимости')

# создаём график распределения стоимости
axs[1, 1].scatter([int(x) for x in range(1, len(data_values_list) + 1)], data_values_list, color="r", linewidth=.2, label="Предметы")

# создаём ограничение на оси
axs[1, 1].set_xlim(0, len(data_values_list) + 1)
axs[1, 1].set_ylim(0, max(data_values_list) + 1)

# скрываем значения по Ox
axs[1, 1].axes.get_xaxis().set_visible(False)

# общий заголовок
plt.suptitle('Тест №1, количество предметов = ' + str(len(data_weights_list)) + ', вместимость рюкзака = ' + str(max_weight))

for ax in axs.flat:
    ax.legend(loc='upper left', fontsize='small')

plt.show()