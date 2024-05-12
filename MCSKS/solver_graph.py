import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def build_graph(data, num_test):
    chosen_items = data["first_sample_data_vector"]

    space = [data["space"][i] for i in chosen_items]
    cores = [data["cores"][i] for i in chosen_items]
    memory = [data["memory"][i] for i in chosen_items]
            
    # Категории
    categories = ['Диск', 'Ядра', 'Память']
    color = ['#FFB836', '#009B00', '#9C9CFF']

    plt.bar(categories[0], data["max_space"], color='white', edgecolor='red')
    
    plt.bar(categories[1], data["max_cores"], color='white', edgecolor='red')
    
    plt.bar(categories[2], data["max_memory"], color='white', edgecolor='red')
    
    bottom_values = [sum(space) / len(space), sum(cores) / len(cores), sum(memory) / len(memory)]

    # Построение столбчатой диаграммы с накоплением
    
    bottom = 0
    for i in range(len(space)):
        if i % 2 == 0:
            plt.bar(categories[0], bottom_values[0], bottom=bottom, edgecolor='black', color=color[0])
        else:
            plt.bar(categories[0], bottom_values[0], bottom=bottom, edgecolor='black', color=color[1])
        bottom += bottom_values[0]
        
    plt.text(0, data["max_space"] + 2, f"{sum(space)} из {data['max_space']}", ha = 'center')
    
    bottom = 0
    for _ in range(len(cores)):
        plt.bar(categories[1], bottom_values[1], bottom=bottom, edgecolor='black')
        bottom += bottom_values[1]
        
    plt.text(1, data["max_cores"] + 2, f"{sum(cores)} из {data['max_cores']}", ha = 'center')

    bottom = 0
    for i in range(len(memory)):
        if i % 3 == 0:
            plt.bar(categories[2], bottom_values[2], bottom=bottom, edgecolor='black', color=color[0])
        elif i % 3 == 1:
            plt.bar(categories[2], bottom_values[2], bottom=bottom, edgecolor='black', color=color[1])
        else:
            plt.bar(categories[2], bottom_values[2], bottom=bottom, edgecolor='black', color=color[2])
        bottom += bottom_values[2]

    plt.text(2, data["max_memory"] + 2, f"{sum(memory)} из {data['max_memory']}", ha = 'center')

    constraint = False
    if (sum(space) > data["max_space"]):
        plt.bar(categories[0], sum(space) - data["max_space"], bottom=data["max_space"], edgecolor='black', color='red')
        constraint = True
    if (sum(cores) > data["max_cores"]):
        plt.bar(categories[1], sum(cores) - data["max_cores"], bottom=data["max_cores"], edgecolor='black', color='red')
        constraint = True
    if (sum(memory) > data["max_memory"]):
        plt.bar(categories[2], sum(memory) - data["max_memory"], bottom=data["max_memory"], edgecolor='black', color='red')
        constraint = True

    plt.ylabel('Значение')
    plt.title(f"Распределение ресурсов на сервере. Количество задач: {data['num_items']}. Значение num_reads: {data['num_reads']}")
    
    orange_rectangle = mpatches.Rectangle((0, 0), 1, 1, fc="orange", edgecolor='black')
    if constraint == False:
        red_line = mlines.Line2D([0, 1], [0, 0], color='red', linestyle='-')
        plt.legend(handles=[red_line, orange_rectangle], labels=['Ограничение', 'Параметр i-й задачи'], loc='upper right')
    if constraint == True:
        red_rectangle = mpatches.Rectangle((0, 0), 1, 1, fc="red", edgecolor='black')
        plt.legend(handles=[red_rectangle, orange_rectangle], labels=['Превышение', 'Параметр i-й задачи'], loc='upper right')

    plt.show()
    # plt.savefig(os.path.join(data["os_save_path"] + f"\\autosave_fig_lambda_test_{num_test}.png"), format="png")