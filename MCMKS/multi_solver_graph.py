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
            
    fig, axs = plt.subplots(int(data["num_knapsacks"] / 4), 4)
    
    categories = ['Диск', 'Ядра', 'Память']
    for p in range(int(data["num_knapsacks"] / 4)):
        for i in range(4):
            
            max_value = max(data["max_space"][p * 4 + i], data["max_cores"][p * 4 + i], data["max_memory"][p * 4 + i])
            
            axs_0_percents =  max_value / data["max_space"][p * 4 + i];    
            axs_1_percents = max_value / data["max_cores"][p * 4 + i];
            axs_2_percents = max_value / data["max_memory"][p * 4 + i];
        
            axs[p][i].bar(categories[0], data["max_space"][p * 4 + i] * axs_0_percents, color='white', edgecolor='red')
            axs[p][i].axes.get_yaxis().set_visible(False)
            axs[p][i].bar(categories[1], data["max_cores"][p * 4 + i] * axs_1_percents, color='white', edgecolor='red')
            axs[p][i].axes.get_yaxis().set_visible(False)
            axs[p][i].bar(categories[2], data["max_memory"][p * 4 + i] * axs_2_percents, color='white', edgecolor='red')
            axs[p][i].axes.get_yaxis().set_visible(False)
            
            yellow = Color("#FFB28B")
            green = Color("#77DD77")
            colors = list(yellow.range_to(green, len(space[p * 4 + i])))
        
            edge_color = 'black'
            
            if (len(space[p * 4 + i]) >= 40):
                edge_color = 'none'
        
            bottom = 0
            for j in range(len(space[p * 4 + i])):
                axs[p][i].bar(categories[0], space[p * 4 + i][j] * axs_0_percents, bottom=bottom, edgecolor=edge_color, color=colors[j].get_hex_l())
                bottom += space[p * 4 + i][j] * axs_0_percents

            axs[p][i].text(0, max(sum(space[p * 4 + i]) * 1.015 * axs_0_percents, max_value * 1.015), f"{sum(space[p * 4 + i])} из {data['max_space'][p * 4 + i]}", ha = 'center')
                
            bottom = 0
            for j in range(len(cores[p * 4 + i])):
                axs[p][i].bar(categories[1], cores[p * 4 + i][j] * axs_1_percents, bottom=bottom, edgecolor=edge_color, color=colors[j].get_hex_l())
                bottom += cores[p * 4 + i][j] * axs_1_percents
                
            axs[p][i].text(1, max(sum(cores[p * 4 + i]) * 1.015 * axs_1_percents, max_value * 1.015), f"{sum(cores[p * 4 + i])} из {data['max_cores'][p * 4 + i]}", ha = 'center')

            bottom = 0
            for j in range(len(memory[p * 4 + i])):
                axs[p][i].bar(categories[2], memory[p * 4 + i][j] * axs_2_percents, bottom=bottom, edgecolor=edge_color, color=colors[j].get_hex_l())
                bottom += memory[p * 4 + i][j] * axs_2_percents

            axs[p][i].text(2, max(sum(memory[p * 4 + i]) * 1.015 * axs_2_percents, max_value * 1.015), f"{sum(memory[p * 4 + i])} из {data['max_memory'][p * 4 + i]}", ha = 'center')

            if (sum(space[p * 4 + i]) > data["max_space"][p * 4 + i]):
                axs[p][i].bar(categories[0], (sum(space[p * 4 + i]) - data["max_space"][p * 4 + i]) * axs_0_percents, bottom=data["max_space"][p * 4 + i] * axs_0_percents, edgecolor='black', color='red')
            if (sum(cores[p * 4 + i]) > data["max_cores"][p * 4 + i]):
                axs[p][i].bar(categories[1], (sum(cores[p * 4 + i]) - data["max_cores"][p * 4 + i]) * axs_1_percents, bottom=data["max_cores"][p * 4 + i] * axs_1_percents, edgecolor='black', color='red')
            if (sum(memory[p * 4 + i]) > data["max_memory"][p * 4 + i]):
                axs[p][i].bar(categories[2], (sum(memory[p * 4 + i]) - data["max_memory"][p * 4 + i]) * axs_2_percents, bottom=data["max_memory"][p * 4 + i] * axs_2_percents, edgecolor='black', color='red')

            axs[p][i].set_xlabel(f"Сервер {p * 4 + i + 1}", fontsize=15)

    plt.subplots_adjust(hspace=0.3)

    plt.suptitle(f"Распределение ресурсов на сервере. Количество задач: {data['num_items']}. Значение num_reads: {data['num_reads']}. Время работы: {data['response_time']} s.")
    
    fig.set_size_inches(19.20, 10.80)
        
    plt.savefig(os.path.join(data["os_save_path"] + f"\\autosave_test_{num_test}.png"), format="png")