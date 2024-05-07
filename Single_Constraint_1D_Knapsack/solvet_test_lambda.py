import matplotlib.pyplot as plt
import os

import qubo_type_1_solver as solver

def solver_test(data, data_graph, num_reads, first_lambda_value, end_lambda_value, range_lambda_value, num_test = 0):
    assert(num_reads > 0)
    assert(first_lambda_value < end_lambda_value)
    assert(range_lambda_value > 0)
    
    new_data = data
    
    data_graph["lambda_value"] = []
    
    first_x = 0
    first_y = 0
   
    for lambd in range(first_lambda_value, end_lambda_value, range_lambda_value):
        new_data["first_lambda"] = lambd
        
        answer, time = solver.solver(new_data, num_reads)
            
        data_graph["first_qubo_percents"].append(answer / data["correct_answer"] * 100)
        
        if (first_x == 0 and first_y == 0):
            if (answer / data["correct_answer"] * 100 < 85):
                first_y = answer / data["correct_answer"] * 100
                first_x = lambd

        data_graph["first_qubo_timer"].append(time)
        
        data_graph["lambda_value"].append(lambd)
        
    font_size = plt.rcParams['xtick.labelsize']
    font_name = plt.rcParams['font.family']

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
    axs[0, 1].plot(data_graph["lambda_value"], data_graph["first_qubo_percents"], 'r--')

    # заголовок
    axs[0, 1].set_title('Точность работы')
    axs[0, 1].set_ylabel('Точность, %')

    min_ylim = max(min(data_graph["first_qubo_percents"]) - 20, 0)
    axs[0, 1].set_ylim(min_ylim, 110)
    axs[0, 1].set_xlim(0, max(data_graph["lambda_value"]) + 1)

    # заголовок
    axs[1, 0].set_title('Временная сложность')
    axs[1, 0].set_ylabel('Время работы, s')

    # графики и описание
    axs[1, 0].plot(data_graph["lambda_value"], data_graph["first_qubo_timer"], 'r--')

    for ax in axs.flat[2:3]:
        ax.set(xlabel="lambda_value")
        
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
                ', значение num_reads = ' +
                str(num_reads))

    axs[0, 0].legend(loc='upper left', fontsize='small')

    axs[1, 1].legend(loc='upper left', fontsize='small')
    
    axs[0, 1].plot([first_x, 0], [first_y, first_y], color='g', linestyle='--')
    
    axs[0, 1].text(max(first_x / 3, max(data_graph["lambda_value"]) / 100 * 5), first_y + 1, f'{round(first_y, 1)}%', fontdict={'size': 9, 'family': font_name, 'color': 'green'}, ha='center', va='bottom')
    
    axs[0, 1].plot([first_x, first_x], [0, first_y], color='g', linestyle='--')
    
    axs[0, 1].text(first_x - max(data_graph["lambda_value"]) / 100 * 2, min_ylim + 5, f'lambda_value: {first_x}', fontdict={'size': 7, 'family': font_name, 'color': 'green'}, ha='center', va='bottom', rotation=90)

    fig.set_size_inches(19.20, 10.80)

    if (num_test == 0):
        plt.savefig("autosave_fig_lambda_test.png", format="png")
    else:
        plt.savefig(os.path.join(data["os_save_path"] + "\\autosave_fig_lambda_test_" + str(num_test) + ".png"), format="png")
