import matplotlib.pyplot as plt
import os

import qubo_type_1_solver as solver

def solver_test(data, data_graph, start_reads, end_reads, range_reads, num_test = 0):
    assert(start_reads > 0)
    assert(start_reads < end_reads)
    assert(range_reads > 0)

    for num_reads in range(start_reads, end_reads, range_reads):
        
        answer, time = solver.solver(data, num_reads)
            
        data_graph["first_qubo_percents"].append(answer / data["correct_answer"] * 100)
        
        data_graph["first_qubo_timer"].append(time)
        
        data_graph["num_reads"].append(num_reads)

    fig, axs = plt.subplots(2, 2)

    # создаём надпись на Oy
    axs[0, 0].set_ylabel('Вес предмета')

    # заголовок
    axs[0, 0].set_title('Распределение веса')

    # создаём график распределения веса
    axs[0, 0].scatter(list(range(1, data["num_items"] + 1)), data["weights"], color="r", linewidth=.2, label="Предметы")

    # создаём ограничение на оси
    axs[0, 0].set_xlim(0, data["num_items"] + 1)
    axs[0, 0].set_ylim(0, max(data["weights"]) + 1)

    # скрываем значения по Ox
    axs[0, 0].axes.get_xaxis().set_visible(False)

    # графики и описание
    axs[0, 1].plot(data_graph["num_reads"], data_graph["first_qubo_percents"], 'r--')

    # заголовок
    axs[0, 1].set_title('Точность работы')
    axs[0, 1].set_ylabel('Точность, %')

    axs[0, 1].set_ylim(0, 110)
    axs[0, 1].set_xlim(0, max(data_graph["num_reads"]) + 1)

    # заголовок
    axs[1, 0].set_title('Временная сложность')
    axs[1, 0].set_ylabel('Время работы, s')
    
    axs[0, 1].set_xlim(min(data_graph["num_reads"]) - 1, max(data_graph["num_reads"]) + 1)

    # графики и описание
    axs[1, 0].plot(data_graph["num_reads"], data_graph["first_qubo_timer"], 'r--')

    for ax in axs.flat[2:3]:
        ax.set(xlabel="num_reads")
        
    # создаём надпись на Oy
    axs[1, 1].set_ylabel('Стоимость предмета')

    # заголовоки
    axs[1, 1].set_title('Распределение стоимости')

    # создаём график распределения стоимости
    axs[1, 1].scatter(list(range(1, data["num_items"] + 1)), data["values"], color="r", linewidth=.2, label="Предметы")

    # создаём ограничение на оси
    axs[1, 1].set_xlim(0, data["num_items"] + 1)
    axs[1, 1].set_ylim(0, max(data["values"]) + 1)

    # скрываем значения по Ox
    axs[1, 1].axes.get_xaxis().set_visible(False)

    # общий заголовок
    plt.suptitle('Тест №1, количество предметов = ' + str(data["num_items"]) +
                ', вместимость рюкзака = ' + str(data["max_weight"]) +
                ', значение лямбды = ' +
                str(data["first_lambda"]))

    axs[0, 0].legend(loc='upper left', fontsize='small')

    axs[1, 1].legend(loc='upper left', fontsize='small')

    fig.set_size_inches(19.20, 10.80)

    if (num_test == 0):
        plt.savefig("autosave_fig_solver_test.png", format="png")
    else:
        plt.savefig(os.path.join(data["os_save_path"] + "\\autosave_fig_solver_test_" + str(num_test) + ".png"), format="png")
    
    plt.close()