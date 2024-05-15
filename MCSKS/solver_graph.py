import os
import matplotlib.pyplot as plt
from colour import Color

def build_graph(data, num_test):
    chosen_items = data["first_sample_data_vector"]

    space = [data["space"][i] for i in chosen_items]
    cores = [data["cores"][i] for i in chosen_items]
    memory = [data["memory"][i] for i in chosen_items]
            
    fig, axs = plt.subplots(1, 3)
    
    categories = ['Диск', 'Ядра', 'Память']

    yellow = Color("#FFB28B")
    green = Color("#77DD77")
    colors = list(yellow.range_to(green, len(space))) 
    
    axs[0].bar(categories[0], data["max_space"], color='white', edgecolor='red')
    
    axs[1].bar(categories[1], data["max_cores"], color='white', edgecolor='red')
    
    axs[2].bar(categories[2], data["max_memory"], color='white', edgecolor='red')
    
    edge_color = 'black'
    
    if (len(space) >= 40):
        edge_color = 'none'
    
    bottom = 0
    
    for i in range(len(space)):
        axs[0].bar(categories[0], space[i], bottom=bottom, edgecolor=edge_color, color=colors[i].get_hex_l())
        bottom += space[i]
        
    axs[0].text(0, data["max_space"] + data["max_space"] * 0.01, f"{sum(space)} из {data['max_space']}", ha = 'center')
    
    bottom = 0
    for i in range(len(cores)):
        axs[1].bar(categories[1], cores[i], bottom=bottom, edgecolor=edge_color, color=colors[i].get_hex_l())
        bottom += cores[i]
        
    axs[1].text(0, data["max_cores"] + data["max_cores"] * 0.01, f"{sum(cores)} из {data['max_cores']}", ha = 'center')

    bottom = 0
    for i in range(len(memory)):
        axs[2].bar(categories[2], memory[i], bottom=bottom, edgecolor=edge_color, color=colors[i].get_hex_l())
        bottom += memory[i]

    axs[2].text(0, data["max_memory"] + data["max_memory"] * 0.01, f"{sum(memory)} из {data['max_memory']}", ha = 'center')

    if (sum(space) > data["max_space"]):
        axs[0].bar(categories[0], sum(space) - data["max_space"], bottom=data["max_space"], edgecolor='black', color='red')
    if (sum(cores) > data["max_cores"]):
        axs[1].bar(categories[1], sum(cores) - data["max_cores"], bottom=data["max_cores"], edgecolor='black', color='red')
    if (sum(memory) > data["max_memory"]):
        axs[2].bar(categories[2], sum(memory) - data["max_memory"], bottom=data["max_memory"], edgecolor='black', color='red')

    plt.suptitle(f"Распределение ресурсов на сервере. Количество задач: {data['num_items']}. Значение num_reads: {data['num_reads']}. Время работы: {data['response_time']} s. \n $\lambda_1$ = {data['first_lambda']}, $\lambda_2$ = {data['second_lambda']}, $\lambda_3$ = {data['third_lambda']}")
    
    fig.set_size_inches(19.20, 10.80)
    
    plt.savefig(os.path.join(data["os_save_path"] + f"\\autosave_fig_test_{num_test}.png"), format="png")