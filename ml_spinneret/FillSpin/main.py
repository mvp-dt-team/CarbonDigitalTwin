from PIL import Image
import numpy as np
import pandas as pd

from Network_v_1 import NNetwork
import torch
from sklearn.preprocessing import StandardScaler

from tqdm import tqdm

import time
import matplotlib.pyplot as plt
# import logging
from datetime import datetime

import requests
from config import APIKEY

import os
import zipfile

def image_to_numpy(image_path, v: float) -> np.ndarray :
    """
    Конвертирует пиксельное изображение в матрицу NumPy с учетом указанных значений.

    Параметры:
    - image_path (str): Путь к изображению.
    - v (float): Значение переменной v для голубого цвета.

    Возвращает:
    - numpy_array (матрица NumPy): Матрица, представляющая пиксели изображения.
    """

    image = Image.open(image_path)
    pixel_array = np.array(image)
    numpy_array = np.zeros((pixel_array.shape[0], pixel_array.shape[1]))
    for i in range(pixel_array.shape[0]):
        for j in range(pixel_array.shape[1]):
            # print(pixel_array)
            if (np.equal(np.array([0, 0, 0]), pixel_array[i, j, :3])).all():
                numpy_array[i, j] = -1
            elif (np.equal(np.array([255, 255, 255]), pixel_array[i, j, :3])).all():
                numpy_array[i, j] = 0
            elif (np.equal(np.array([0, 127, 255]), pixel_array[i, j, :3])).all():
                numpy_array[i, j] = v

    return numpy_array

def numpy_to_image(numpy_array: np.ndarray, save_path: str, v: float) -> None :
    """
    Конвертирует матрицу NumPy в пиксельное изображение с учетом указанных значений и сохраняет его.

    Параметры:
    - numpy_array (np.ndarray): Матрица, представляющая пиксели изображения.
    - save_path (str): Путь для сохранения изображения.
    - v (float): Значение переменной v для голубого цвета.
    """

    pixel_array = np.zeros((numpy_array.shape[0], numpy_array.shape[1], 3))
    for i in range(pixel_array.shape[0]):
        for j in range(pixel_array.shape[1]):
            if numpy_array[i, j] == -1:
                pixel_array[i, j] = np.array([0, 0, 0])
            elif numpy_array[i, j] == 0:
                pixel_array[i, j] = np.array([255, 255, 255])
            elif numpy_array[i, j] == v:
                pixel_array[i, j] = np.array([255, 0, 0])
            else:
                interval_size = 1 / 127
                index =  int(numpy_array[i, j] / interval_size)
                pixel_array[i, j] = np.array([index + 127, 27 + index, 0])

    image = Image.fromarray(pixel_array.astype('uint8'))
    image.save(save_path)

def load_model(nn_params: dict, model_filename: str):
    model_new = NNetwork(nn_params['input_size'], nn_params['hidden_size'], nn_params['hidden_size_two'],
                              nn_params['hidden_size_three'], nn_params['output_size'])

    checkpoint = torch.load(model_filename)
    model_new.load_state_dict(checkpoint['model_state_dict'])

    scaler_x = StandardScaler()
    scaler_x.mean_ = checkpoint['scaler_x_mean']
    scaler_x.scale_ = checkpoint['scaler_x_scale']

    scaler_y = StandardScaler()
    scaler_y.mean_ = checkpoint['scaler_y_mean']
    scaler_y.scale_ = checkpoint['scaler_y_scale']
    
    return model_new, scaler_x, scaler_y,

def process_matrix(matrix_array):
    dataset = []

    # Задаем форму матрицы 3x3
    shape = (3, 3)

    # Используем nditer для итерации по матрицам 3x3
    it = np.nditer(matrix_array, flags=['multi_index'], op_flags=['readwrite'], order='C')
    while not it.finished:
        # Получаем текущий индекс
        i, j = it.multi_index

        # Проверяем, что матрица 3x3 целиком помещается внутри массива
        if i + shape[0] <= matrix_array.shape[0] and j + shape[1] <= matrix_array.shape[1]:
            # Выполняем операции над матрицей 3x3
            submatrix = matrix_array[i:i + shape[0], j:j + shape[1]]
            # Ваш код для обработки submatrix
            central_value = submatrix[1, 1]
            if central_value != -1:
                outer = []
                for x_offset, y_offset in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]:
                    outer_value = submatrix[x_offset, y_offset]
                    outer.append(outer_value)
                dataset.append(outer.copy())
        # Переходим к следующему элементу с учетом шага матрицы 3x3
        it.iternext()
    return dataset

def run_matrix(matrix: np.ndarray, model, scaler_x, scaler_y, v):
    output_values = []
    dataset = process_matrix(matrix)
    model.eval()
    
    for data in dataset:
        new_outer_values = torch.tensor([data], dtype=torch.float32)
        new_outer_values_scaled = torch.tensor(scaler_x.transform(new_outer_values), dtype=torch.float32)
        with torch.no_grad():
            predicted_scaled = model(new_outer_values_scaled)
            predicted = scaler_y.inverse_transform(predicted_scaled)
            output_values.append(predicted.item())
    

    numpy_array = np.zeros((matrix.shape[0], matrix.shape[1]))
    output_values_iter = iter(output_values)
    
    for i in range(1, matrix.shape[0]-1):
        for j in range(1, matrix.shape[1] - 1):
            if matrix[i, j] == -1:
                numpy_array[i, j] = -1
                continue
            out = output_values_iter.__next__()
            if out <= 0:
                out = 0
            numpy_array[i, j] = out

    for j in range(1, matrix.shape[1] - 1):
        numpy_array[0, j] = v
    
    
    for j in range(1, matrix.shape[1] - 1):
        numpy_array[matrix.shape[0] - 1, j] = numpy_array[matrix.shape[0] - 2, j]

    for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j] == -1:
                    numpy_array[i, j] = -1
    
    return numpy_array


def fill_matrix(matrix, v):
    count_non_minus_1_elements = np.sum(matrix != -1, axis=1)
    max_element = np.max(count_non_minus_1_elements)
    
    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1] - 1):
            if matrix[i, j] == -1:
                continue
            matrix[i, j] = (max_element / count_non_minus_1_elements[i]) * v
            
    return matrix

def func_change(matrix_old, matrix_new):
    dx = []
    for i in range(1, matrix_old.shape[0] - 1):
        for j in range(1, matrix_old.shape[1] - 1):
            if matrix_old[i, j] == -1:
                continue
            dx.append(np.abs(matrix_old[i, j] - matrix_new[i, j]))
    return np.max(dx), np.min(dx), np.mean(dx)

AMOUNT_ITTER = 10
STEP = 1

def action(image_path, v_value, gif_name, table_name, model_param, amount_iter=AMOUNT_ITTER, step=STEP):
                      
#     log_format = '%(asctime)s - %(levelname)s - %(message)s'

#     # Создаем объект логгера
#     logger = logging.getLogger('FillDIE')
#     formatter = logging.Formatter(log_format)

#     # Устанавливаем уровень логгирования для файлового логгера
#     file_handler = logging.FileHandler(f"log-fill_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
#     file_handler.setLevel('INFO')
#     file_handler.setFormatter(formatter)
#     logger.addHandler(file_handler)

#     logger.setLevel(logging.INFO)
    # nn_param = { 'input_size': 8, 'hidden_size': 32, 'hidden_size_two': 128, 'hidden_size_three': 64, 'output_size': 1, # MLv3
    # 'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6}


    # image_path = "f2.png"
    # v_value = 0.02  # Значение переменной v
    
    numpy_array = fill_matrix(image_to_numpy(image_path, v_value), v_value)
    df = pd.DataFrame(numpy_array)
    df.to_csv('FillSpin/test_table.csv')

    model, scaler_x, scaler_y = load_model(nn_params=model_param['nn_param'], model_filename=model_param['ML_name'])
    matrix = numpy_array
    count = 0
    dx_change = []
    for i in tqdm(range(amount_iter)):
        res_array = run_matrix(matrix, model, scaler_x=scaler_x, scaler_y=scaler_y, v=v_value)
        max_change, min_change, mean_change = func_change(matrix, res_array)
        dx_change.append([i + 1, max_change, min_change, mean_change])
        # logger.info(f'Itteration: {i+1}, max change: {max_change:.2e}, min change: {min_change:.2e}, mean change: {mean_change:.2e}')
        matrix = res_array.copy()
        # numpy_to_image(matrix, 'res2.png', v_value)
        if count % step == 0:
            new_matrix = np.where(matrix == -1, np.nan, matrix.copy())
            # df = pd.DataFrame(new_matrix)
            # df.to_csv(f'test_table{count}.csv')
            plt.imshow(new_matrix)
            # cbar = plt.colorbar(ticks=np.linspace(0, 0.3, 20))
            plt.clim(0, 1)
            plt.colorbar()
            plt.savefig(f'FillSpin/imgs/frame_{count}.png')
            plt.clf()
        count += 1
    
    
    frames = []
    for frame_number in range(0, amount_iter, step):
        # Открываем изображение каждого кадра.
        frame = Image.open(f'FillSpin/imgs/frame_{frame_number}.png')
        # Добавляем кадр в список с кадрами.
        frames.append(frame)

    # Берем первый кадр и в него добавляем оставшееся кадры.
    frames[0].save(
        gif_name,
        save_all=True,
        append_images=frames,  # Срез который игнорирует первый кадр.
        optimize=True,
        duration=100,
        loop=0
    )
    pd.DataFrame(data=np.array(dx_change), columns=['ITTERATION', 'MAX', 'MIN', 'MEAN']).to_csv(table_name)
    
if __name__ == '__main__':
    
    model_params = [
        {
            'ML_name': 'FillSpin/MLv3.pth',
            'nn_param': { 'input_size': 8, 'hidden_size': 32, 'hidden_size_two': 128, 'hidden_size_three': 64, 'output_size': 1, # MLv3
                          'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6}
        },
        { 
            'ML_name': 'FillSpin/MLv4.pth',
            'nn_param': { 'input_size': 8, 'hidden_size': 64, 'hidden_size_two': 64, 'hidden_size_three': 64, 'output_size': 1, # MLv4
                          'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 2 * 10**6}
        },
        { 
            'ML_name': 'FillSpin/MLv8.pth',
            'nn_param': { 'input_size': 8, 'hidden_size': 16, 'hidden_size_two': 64, 'hidden_size_three': 12, 'output_size': 1, # MLv8
                          'num_epochs': 100, 'learning_rate': 0.01, 'batch_size': 2 * 10**6}
        },
        {
            'ML_name': 'FillSpin/MLv9.pth',
            'nn_param': { 'input_size': 8, 'hidden_size': 32, 'hidden_size_two': 128, 'hidden_size_three': 64, 'output_size': 1, # MLv9
                          'num_epochs': 100, 'learning_rate': 0.0012, 'batch_size': 2 * 10**6}
        }
    ]
    amounts_iter = [1000, 10000, 15000, 20000]
    steps = [10, 20, 30, 40]
    
    for idx, i in enumerate(amounts_iter):
        for model in model_params:
            ml_name = model['ML_name'].split('.')
            ml_name = ml_name[0].split('/')

            try:
                action('FillSpin/f2.png', 0.02, f'FillSpin/ML_{ml_name[0]}_IT_{i}.gif', f'FillSpin/ML_{ml_name[0]}_IT_{i}.csv', model, i, steps[idx])
            except Exception as exc:
                requests.get(f'https://api.telegram.org/bot{APIKEY}/sendMessage?chat_id=463762417&text=Не удалась модуляция ML_{ml_name[0]}_IT_{i}. Ошибка: {str(exc)}')
                continue
    
            with open(f'FillSpin/ML_{ml_name[0]}_IT_{i}.gif', 'rb') as inputfile:
                data  = {'chat_id': 463762417}
                files_gif = {'animation': inputfile}
                requests.get(f'https://api.telegram.org/bot{APIKEY}/sendAnimation', data=data, files=files_gif)

            with open(f'FillSpin/ML_{ml_name[0]}_IT_{i}.csv', 'rb') as inputfile:
                data  = {'chat_id': 463762417}
                files_csv = {'document': inputfile}
                requests.get(f'https://api.telegram.org/bot{APIKEY}/sendDocument', data=data, files=files_csv)
    
    fantasy_zip = zipfile.ZipFile('C:\\Users\\boiko.k.v\\Desktop\\MLSpinneretDT\\FillSpin\\die.zip', 'w')
    for folder, subfolders, files in os.walk('C:\\Users\\boiko.k.v\\Desktop\\MLSpinneretDT\\FillSpin'):
        for file in files:
            if file.endswith('.csv') or file.endswith('.gif'):
                fantasy_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'C:\\Users\\boiko.k.v\\Desktop\\MLSpinneretDT\\FillSpin'), compress_type = zipfile.ZIP_DEFLATED)
    fantasy_zip.close()
    with open('FillSpin/die.zip', 'rb') as inputfile:
        data  = {'chat_id': 463762417}
        files_zip = {'document': inputfile}
        req = requests.get(f'https://api.telegram.org/bot{APIKEY}/sendDocument', data=data, files=files_zip)
        if not req.ok:
            requests.get(f'https://api.telegram.org/bot{APIKEY}/sendMessage?chat_id=463762417&text=zip отправить не удалось, поэтому посмотришь в ПИШе')
        