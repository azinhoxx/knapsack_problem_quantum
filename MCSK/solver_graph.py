import os
import numpy as np
import matplotlib.pyplot as plt

def build_graph(data, num_test):
    data_memory = data["weights"]
    data_cores = data["cores"]
    chosen_items = data["first_sample_data_vector"]

    memory = [data_memory[i] for i in chosen_items]
    cores = [data_cores[i] for i in chosen_items]
    
    values_sum = sum(data["values"][i] for i in chosen_items)

    max_memory = data["max_weight"]
    max_core = data["max_cores"]

    pr_sum_mem = [0]
    pr_sum_cor = [0]
    for i in range(len(memory)):
        pr_sum_mem.append(pr_sum_mem[-1] + memory[i])
        pr_sum_cor.append(pr_sum_cor[-1] + cores[i])

    fig, axs = plt.subplots(2, 2)
    plt.subplots_adjust(hspace=0.3)

    # создаём надпись на Oy
    axs[0, 0].set_ylabel('Вес задачи')

    # заголовок
    axs[0, 0].set_title('Распределение веса')

    # создаём график распределения веса
    axs[0, 0].scatter(list(range(1, data["num_items"] + 1)), data["weights"], color="r", linewidth=.2, label="Предметы")

    # создаём ограничение на оси
    axs[0, 0].set_xlim(0, data["num_items"] + 1)
    axs[0, 0].set_ylim(min(data["weights"]) - 1, max(data["weights"]) + 1)

    # скрываем значения по Ox
    axs[0, 0].axes.get_xaxis().set_visible(False)

    axs[0, 1].plot(pr_sum_mem, pr_sum_cor)

    axs[0, 1].set(xlabel='Memory', ylabel='Cores',
        title=f'Memory and core usage')
    axs[0, 1].set(xlim=(0, pr_sum_mem[-1] + int(0.2 * pr_sum_mem[-1])), xticks=np.arange(0, pr_sum_mem[-1] + int(0.2 * pr_sum_mem[-1])),
        ylim=(0, pr_sum_cor[-1] + int(0.2 * pr_sum_cor[-1])), yticks=np.arange(0, pr_sum_cor[-1] + int(0.2 * pr_sum_cor[-1])))

    x_chosen_dots = [0]
    y_chosen_dots = [0]
    for i in range(1, len(pr_sum_mem) - 2):
        if (x_chosen_dots[-1] / pr_sum_mem[i]) * 100 < 65 and (y_chosen_dots[-1] / pr_sum_cor[i]) * 100 < 65:
                x_chosen_dots.append(pr_sum_mem[i])
                if x_chosen_dots[-1] and x_chosen_dots[-1] / pr_sum_mem[-1] < 0.1:
                        x_chosen_dots.pop()
                        y_chosen_dots.pop()
                y_chosen_dots.append(pr_sum_cor[i])
    x_chosen_dots.append(pr_sum_mem[-1])
    y_chosen_dots.append(pr_sum_cor[-1])

    a = [x for x in pr_sum_mem if x not in x_chosen_dots[2:]]
    b = [y for y in pr_sum_cor if y not in y_chosen_dots[2:]]

    axs[0, 1].stem(x_chosen_dots[2:], y_chosen_dots[2:], linefmt='C0:')
    axs[0, 1].stem(y_chosen_dots[2:], x_chosen_dots[2:], linefmt='C0:', orientation = 'horizontal')

    axs[0, 1].stem(max_memory, max_core, linefmt='C3-', markerfmt='red')
    axs[0, 1].stem(max_core, max_memory, linefmt='C3-', orientation = 'horizontal', markerfmt='red')

    axs[0, 1].plot(a, b, 'bo', label='items')
    axs[0, 1].plot([max_memory], [max_core], label='constraint', color="red")
    axs[0, 1].legend(loc='upper left')
    axs[0, 1].set_xlim([0, data["max_weight"] + data["max_weight"] / 8])
    axs[0, 1].set_ylim([0, data["max_cores"] + data["max_cores"] / 8])

    axs[0, 1].text(max_memory / 3, max_core + 0.03 * max_core, 'cores constraint = ' + str(max_core))
    axs[0, 1].text(max_memory + 0.02 * max_memory, max_core / 5, 'memory constraint = ' + str(max_memory), rotation=-90)

    axs[0, 1].set_xticks(x_chosen_dots[2:] + [0])
    axs[0, 1].set_yticks(y_chosen_dots[2:] + [0])

    # создаём надпись на Oy
    axs[1, 1].set_ylabel('Стоимость задачи')

    # заголовоки
    axs[1, 1].set_title('Распределение стоимости')

    # создаём график распределения стоимости
    axs[1, 1].scatter(list(range(1, data["num_items"] + 1)), data["values"], color="r", linewidth=.2, label="Предметы")

    # создаём ограничение на оси    
    axs[1, 1].set_xlim(0, data["num_items"] + 1)
    axs[1, 1].set_ylim(0, max(data["values"]) + 1)

    # скрываем значения по Ox
    axs[1, 1].axes.get_xaxis().set_visible(False)

    # создаём надпись на Oy
    axs[1, 0].set_ylabel('Потребление ядер')

    # заголовоки
    axs[1, 0].set_title('Распределение ядер')

    # создаём график распределения стоимости
    axs[1, 0].scatter(list(range(1, data["num_items"] + 1)), data["cores"], color="r", linewidth=.2, label="Предметы")

    # создаём ограничение на оси    
    axs[1, 0].set_xlim(0, data["num_items"] + 1)
    axs[1, 0].set_ylim(min(data["cores"]) - 1, max(data["cores"]) + 1)

    # скрываем значения по Ox
    axs[1, 0].axes.get_xaxis().set_visible(False)

    # общий заголовок
    plt.suptitle(f'Количество предметов = {data["num_items"]}, num_reads = {data["num_reads"]}, первый коэффициент пенальти: {data["first_lambda"]}, второй коэффициент пенальти: {data["second_lambda"]}' + '\n' + f'Найденная стоимость предметов: {values_sum}, время выполнения в секундах: {data["response_time"]}')

    fig.set_size_inches(19.20, 10.80)

    plt.savefig(os.path.join(data["os_save_path"] + f"\\autosave_fig_lambda_test_{num_test}.png"), format="png")