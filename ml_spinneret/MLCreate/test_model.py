from Network_v_1 import NNetwork
import torch
from sklearn.preprocessing import StandardScaler

nn_params = { 'input_size': 8, 'hidden_size': 32, 'hidden_size_two': 128, 'hidden_size_three': 64, 'output_size': 1, # MLv3
    'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6}

# ЗАГРУЗКА МОДЕЛИ ИЗ ФАЙЛА
model_new = NNetwork(nn_params['input_size'], nn_params['hidden_size'], nn_params['hidden_size_two'],
                              nn_params['hidden_size_three'], nn_params['output_size'])

checkpoint = torch.load('MLv3.pth_new')
model_new.load_state_dict(checkpoint['model_state_dict'])

scaler_x = StandardScaler()
scaler_x.mean_ = checkpoint['scaler_x_mean']
scaler_x.scale_ = checkpoint['scaler_x_scale']

scaler_y = StandardScaler()
scaler_y.mean_ = checkpoint['scaler_y_mean']
scaler_y.scale_ = checkpoint['scaler_y_scale']

# ПОДГОТОВКА ДАННЫХ ИЗ ДРУГОГО СТОЛБЦА

# df = pd.read_csv('CORRECTED_g1-g24.csv')
#
# step_x = 0.01
# step_y = 0.01
#
# matrixrix = pd.pivot_table(df, values='spf.U (m/s) @ v0=0.02_y2=5.5E-4', index=pd.cut(df['y'], np.arange(0, 2 + step_y, step_y)),
#                         columns=pd.cut(df['x'], np.arange(-1, 1 + step_x, step_x)), fill_value=-1)


# def process_matrix(matrix):
#     outer_values = []
#     central_values = []
#     for i in range(1, len(matrix) - 1):
#         for j in range(1, len(matrix.columns) - 1):
#             central_value = matrix.iloc[i, j]
#             central_values.append(central_value)
#             outer = []
#             for x_offset, y_offset in [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
#                 outer_value = matrix.iloc[i + x_offset, j + y_offset]
#                 outer.append(outer_value)
#             outer_values.append(outer.copy())
#     return outer_values.copy(), central_values.copy()


# outer_values, central_values = process_matrix(matrix)

# ТЕСТ МОДЕЛИ


# import time
# start = time.time()
# for i in range(10000):
#     new_outer_values = torch.tensor([[-1, 0.02, 0.02, -1, 0, -1, 0, 0]], dtype=torch.float32)
#     new_outer_values_scaled = torch.tensor(scaler_x.transform(new_outer_values), dtype=torch.float32)
#     with torch.no_grad():
#         predicted_scaled = model_new(new_outer_values_scaled)
#         predicted = scaler_y.inverse_transform(predicted_scaled)

#         # Вывод прогноза
#         # print("Predicted Central Value:", predicted)
# print(f'{(time.time() - start) * 1000} ms')


# import time
# import numpy as np
# firsts = []
# seconds = []
# for i in range(1):
#     start = time.time()
#     tensors = []
#     for i in range(100000):
#         new_outer_values = torch.tensor([[-1, 0.02, 0.02, -1, 0, -1, 0, 0]], dtype=torch.float32)
#         new_outer_values_scaled = torch.tensor(scaler_x.transform(new_outer_values), dtype=torch.float32)
#         tensors.append(new_outer_values_scaled)
#     checkpoint = time.time()
#     first = (checkpoint - start) * 1000
#     print(f'{first} ms')
#     with torch.no_grad():
#         for i in tensors:
#             predicted_scaled = model_new(i)
#             predicted = scaler_y.inverse_transform(predicted_scaled)

#             # Вывод прогноза
#             # print("Predicted Central Value:", predicted)
#     second = (time.time() - checkpoint) * 1000
#     print(f'{second} ms')
#     firsts.append(first)
#     seconds.append(second)

# print('-' * 100)
# print(np.mean(firsts))
# print(np.mean(seconds))




import concurrent.futures
from multiprocessing import freeze_support
import time
import numpy as np

def process_chunk(chunk):
    processed_data = []
    # times = []
    model_new.eval()
    with torch.no_grad():
        for i in chunk:
            # start = time.time()
            predicted_scaled = model_new(i)
            predicted = scaler_y.inverse_transform(predicted_scaled)
            processed_data.append(predicted.item())
            # times.append((time.time() - start) * 1000)
    # print(f'цикл завершился за {np.sum(times)} мс, каждая иттерация в среднем за {np.mean(times)} мс')
    return processed_data

def parallel_process_data(data, chunk_size=1000):
    results = []
    tensors = []
    
    for d in data:
        new_outer_values = torch.tensor([d], dtype=torch.float32)
        new_outer_values_scaled = torch.tensor(scaler_x.transform(new_outer_values), dtype=torch.float32)
        tensors.append(new_outer_values_scaled)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Разбиваем массив данных на куски
        chunks = [tensors[i:i + chunk_size] for i in range(0, len(tensors), chunk_size)]
        # print(chunks)

        # Подаем каждый кусок на обработку в отдельном потоке
        futures = [executor.submit(process_chunk, chunk) for chunk in chunks]

        # Собираем результаты обработки
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())

    # Результат - объединенный массив данных после параллельной обработки
    return results

# Используйте эту функцию, передав ваш большой массив данных
# и размер куска, который вы хотите обработать одновременно
if __name__ == '__main__':
    freeze_support()
    start = time.time()
    result = parallel_process_data([[-1, 0.02, 0.02, -1, 0, -1, 0, 0] for i in range(100000)], chunk_size=10000)
    # print(result)
    print(f'{(time.time() - start) * 1000} ms')
    start = time.time()
    for i in range(10000):
        pass
    print(f'{(time.time() - start) * 1000} ms')
# Вывод реального числа
# print("Real Central Value:", central_values[110])
