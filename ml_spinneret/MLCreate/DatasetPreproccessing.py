import json
import logging
from datetime import datetime
import pandas as pd
import numpy as np
import re


class DatasetPreProc:
    def __init__(self, filenames: list, columns: list, params: dict, dataset_filename: str):
        log_format = '%(asctime)s - %(levelname)s - %(message)s'

        # Создаем объект логгера
        self.logger = logging.getLogger('DatasetPreProc')

        # Устанавливаем уровень логгирования для консольного логгера
        console_handler = logging.StreamHandler()
        console_handler.setLevel('INFO')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Устанавливаем уровень логгирования для файлового логгера
        file_handler = logging.FileHandler(f"log-dataset_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        file_handler.setLevel('DEBUG')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.setLevel(logging.DEBUG)

        # Данные по файлу
        self.filenames = filenames
        self.columns = columns
        self.corrected_files = self.file_preprocessing()

        # Данные по датасету
        self.step_x = params['STEP_X']
        self.step_y = params['STEP_Y']
        self.matrixes = []
        self.dataset = []
        self.dataset_filename = dataset_filename

    def file_preprocessing(self):
        self.logger.debug('Процесс корректировки файла с данными')
        output_files = []

        for filename in self.filenames:
            output_file = 'CORRECTED_' + filename
            # Открываем исходный файл и создаем выходной файл
            with open(filename, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
                for row in infile.readlines():
                    # Замена запятых перед "y2=" на нижнее подчеркивание
                    modified_row = row.replace(', y2=', '_y2=')
                    modified_row = modified_row.replace(', y3=', '_y3=')
                    modified_row = modified_row.replace(', ay3=', '_ay3=')
                    # Записываем отредактированную строку в выходной файл
                    outfile.write(modified_row)
            output_files.append(output_file)

        return output_files

    @staticmethod
    def create_pandas_file(output_file: str):
        return pd.read_csv(output_file)

    def process_matrix(self, matrix_array):
        self.logger.debug('Процесс выделение данных по матрице')
        outer_values = []
        central_values = []

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
                    # outer_values.append(outer.copy())
                    self.dataset.append({'input': outer.copy(), 'output': [central_value]})
            # Переходим к следующему элементу с учетом шага матрицы 3x3
            it.iternext()

    def create_matrices(self, idx, pandas_file, step_x, step_y):
        for col in self.columns[idx]:
            matrix = pd.pivot_table(pandas_file, values=col,
                                    index=pd.cut(pandas_file['y'], np.arange(0, 2 + step_y, step_y)),
                                    columns=pd.cut(pandas_file['x'], np.arange(-1, 1 + step_x, step_x)),
                                    fill_value=-1)
            self.matrixes.append(matrix.to_numpy())

    def save_json_dataset(self):
        with open(self.dataset_filename, 'w') as file:
            json.dump(self.dataset, file)

    def action(self):
        self.logger.info(f'Предобработка файлов')
        for idx, file in enumerate(self.corrected_files):
            self.logger.info(f'Обработка данных в файле {file}...')
            df = self.create_pandas_file(file)
            self.create_matrices(idx, df, self.step_x[idx], self.step_y[idx])
        for idx2, matrix in enumerate(self.matrixes):
            self.logger.info(f'Сбор данных из матрицы по столбцу \"{idx2}\"')
            self.process_matrix(matrix)
        # self.dataset = np.array(self.dataset)
        self.logger.info(f'Всего пар input-output {len(self.dataset)}')
        self.logger.info(f'Сохранение датасета в json файл (процесс может быть долгим)...')
        self.save_json_dataset()
        self.logger.info(f'Датасет сохранен!')
