import pandas as pd
import requests
from config import APIKEY

from MLModule_NP import MLmodule

# Гиперпараметры
nn_params = { 'input_size': 8, 'hidden_size': 8, 'hidden_size_two': 8, 'hidden_size_three': 8, 'output_size': 1,
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6}

all_params = [
    { 'input_size': 8, 'hidden_size': 20, 'hidden_size_two': 60, 'hidden_size_three': 30, 'output_size': 1, # MLv1
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 16, 'hidden_size_two': 64, 'hidden_size_three': 12, 'output_size': 1, # MLv2
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 32, 'hidden_size_two': 128, 'hidden_size_three': 64, 'output_size': 1, # MLv3
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6}, 
    { 'input_size': 8, 'hidden_size': 64, 'hidden_size_two': 64, 'hidden_size_three': 64, 'output_size': 1, # MLv4
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 8, 'hidden_size_two': 64, 'hidden_size_three': 32, 'output_size': 1, # MLv5
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 16, 'hidden_size_two': 16, 'hidden_size_three': 16, 'output_size': 1, # MLv6
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6},
    
    { 'input_size': 8, 'hidden_size': 20, 'hidden_size_two': 60, 'hidden_size_three': 30, 'output_size': 1, # MLv7
    'num_epochs': 100, 'learning_rate': 0.0015, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 16, 'hidden_size_two': 64, 'hidden_size_three': 12, 'output_size': 1, # MLv8
    'num_epochs': 100, 'learning_rate': 0.01, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 32, 'hidden_size_two': 128, 'hidden_size_three': 64, 'output_size': 1, # MLv9
    'num_epochs': 100, 'learning_rate': 0.0012, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 64, 'hidden_size_two': 64, 'hidden_size_three': 64, 'output_size': 1, # MLv10
    'num_epochs': 200, 'learning_rate': 0.0001, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 8, 'hidden_size_two': 64, 'hidden_size_three': 32, 'output_size': 1, # MLv11
    'num_epochs': 100, 'learning_rate': 0.0015, 'batch_size': 2 * 10**6},
    { 'input_size': 8, 'hidden_size': 16, 'hidden_size_two': 16, 'hidden_size_three': 16, 'output_size': 1, # MLv12
    'num_epochs': 100, 'learning_rate': 0.0015, 'batch_size': 2 * 10**6},
]

name_models = ['MLv1', 'MLv2', 'MLv3', 'MLv4', 'MLv5', 'MLv6', 'MLv7', 'MLv8', 'MLv9', 'MLv10', 'MLv11', 'MLv12']
losses = []
winners = []

if __name__ == '__main__':
    for param, name in zip(all_params, name_models):
        print("-"*20, f"Обучение модели {name}", "-"*20)
        requests.get(f'https://api.telegram.org/bot{APIKEY}/sendMessage?chat_id=463762417&text=Расчет начался!')
        module = MLmodule(params={'MODEL_NAME': f'{name}.pth'},
                    nn_params=param,
                    dataset_filename='DATASET.json')
        loss = module.action()
        requests.get(f'https://api.telegram.org/bot{APIKEY}/sendMessage?chat_id=463762417&text=модель: {name}, погрешность: {loss:6f}')
        losses.append(loss)
        if loss < 10 ** (-3):
            winners.append((name, loss))

    with open('winners.txt', 'w', encoding='utf8') as win:
        win.write(winners)
    with open('losses.txt', 'w', encoding='utf8') as win:
        win.write(losses)

