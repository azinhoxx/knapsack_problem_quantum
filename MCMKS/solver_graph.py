import os
import matplotlib.pyplot as plt
from colour import Color

def build_graph(data, data_graph, num_test):
    chosen_items = data_graph["taken_items"]

    space = [[] for _ in range(data['num_knapsacks'])]
    cores = [[] for _ in range(data['num_knapsacks'])]
    memory = [[] for _ in range(data['num_knapsacks'])]

    for i in range(data["num_knapsacks"]):
        space[i] = [data['space'][j] for j in chosen_items[i]]
        cores[i] = [data["cores"][j] for j in chosen_items[i]]
        memory[i] = [data["memory"][j] for j in chosen_items[i]]
            
    fig, axs = plt.subplots(1, data["num_knapsacks"])
    
    categories = ['Диск', 'Ядра', 'Память']
    
    for i in range(data["num_knapsacks"]):
        
        max_value = max(data["max_space"][i], data["max_cores"][i], data["max_memory"][i])
        
        axs_0_percents =  max_value / data["max_space"][i];    
        axs_1_percents = max_value / data["max_cores"][i];
        axs_2_percents = max_value / data["max_memory"][i];
    
        axs[i].bar(categories[0], data["max_space"][i] * axs_0_percents, color='white', edgecolor='red')
        axs[i].axes.get_yaxis().set_visible(False)
        axs[i].bar(categories[1], data["max_cores"][i] * axs_1_percents, color='white', edgecolor='red')
        axs[i].axes.get_yaxis().set_visible(False)
        axs[i].bar(categories[2], data["max_memory"][i] * axs_2_percents, color='white', edgecolor='red')
        axs[i].axes.get_yaxis().set_visible(False)
        
        yellow = Color("#FFB28B")
        green = Color("#77DD77")
        colors = list(yellow.range_to(green, len(space[i])))
    
        edge_color = 'black'
        
        if (len(space[i]) >= 40):
            edge_color = 'none'
    
        bottom = 0
        for j in range(len(space[i])):
            axs[i].bar(categories[0], space[i][j] * axs_0_percents, bottom=bottom, edgecolor=edge_color, color=colors[j].get_hex_l())
            bottom += space[i][j] * axs_0_percents

        axs[i].text(0, max(sum(space[i]) * 1.015 * axs_0_percents, max_value * 1.015), f"{sum(space[i])} из {data['max_space'][i]}", ha = 'center')
            
        bottom = 0
        for j in range(len(cores[i])):
            axs[i].bar(categories[1], cores[i][j] * axs_1_percents, bottom=bottom, edgecolor=edge_color, color=colors[j].get_hex_l())
            bottom += cores[i][j] * axs_1_percents
            
        axs[i].text(1, max(sum(cores[i]) * 1.015 * axs_1_percents, max_value * 1.015), f"{sum(cores[i])} из {data['max_cores'][i]}", ha = 'center')

        bottom = 0
        for j in range(len(memory[i])):
            axs[i].bar(categories[2], memory[i][j] * axs_2_percents, bottom=bottom, edgecolor=edge_color, color=colors[j].get_hex_l())
            bottom += memory[i][j] * axs_2_percents

        axs[i].text(2, max(sum(memory[i]) * 1.015 * axs_2_percents, max_value * 1.015), f"{sum(memory[i])} из {data['max_memory'][i]}", ha = 'center')

        if (sum(space[i]) > data["max_space"][i]):
            axs[i].bar(categories[0], (sum(space[i]) - data["max_space"][i]) * axs_0_percents, bottom=data["max_space"][i] * axs_0_percents, edgecolor='black', color='red')
        if (sum(cores[i]) > data["max_cores"][i]):
            axs[i].bar(categories[1], (sum(cores[i]) - data["max_cores"][i]) * axs_1_percents, bottom=data["max_cores"][i] * axs_1_percents, edgecolor='black', color='red')
        if (sum(memory[i]) > data["max_memory"][i]):
            axs[i].bar(categories[2], (sum(memory[i]) - data["max_memory"][i]) * axs_2_percents, bottom=data["max_memory"][i] * axs_2_percents, edgecolor='black', color='red')

        axs[i].set_xlabel(f"Сервер {i + 1}", fontsize=15)

    plt.suptitle(f"Распределение ресурсов на сервере. Количество задач: {data['num_items']}. Значение num_reads: {data['num_reads']}. Время работы: {data['response_time']} s.")
    
    fig.set_size_inches(19.20, 10.80)
        
    plt.savefig(os.path.join(data["os_save_path"] + f"\\autosave_test_{num_test}.png"), format="png")