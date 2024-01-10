import json
import torch
from torch.utils.data import DataLoader, TensorDataset
from multiprocessing import Pool, freeze_support
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from Network_v_1 import NNetwork

import json

from Network_v_1 import NNetwork

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import numpy as np

import pandas as pd

import re

import logging

from datetime import datetime

from tqdm import tqdm

from multiprocessing import Pool

def load_data(index, data_path):
    with open(data_path, 'r') as file:
        data = json.load(file)
    return data[index]

def parallel_loader(data_path, num_workers=4):
    with Pool(num_workers) as pool:
        data = pool.starmap(load_data, [(i, data_path) for i in range(num_workers)])

    return data

class MLModule:
    def __init__(self, params: dict, nn_params: dict, dataset_filename: str, new_model=True, model=None):
        log_format = '%(asctime)s - %(levelname)s - %(message)s'

        # Создаем объект логгера
        self.logger = logging.getLogger('MLModule')

        # Устанавливаем уровень логгирования для консольного логгера
        console_handler = logging.StreamHandler()
        console_handler.setLevel('INFO')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Устанавливаем уровень логгирования для файлового логгера
        file_handler = logging.FileHandler(f"log-ml_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        file_handler.setLevel('DEBUG')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        self.logger.setLevel(logging.DEBUG)

        # Данные по модели
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = params['MODEL_NAME']
        self.nn_params = nn_params
        if new_model:
            self.model = NNetwork(nn_params['input_size'], nn_params['hidden_size'], nn_params['hidden_size_two'],
                                  nn_params['hidden_size_three'], nn_params['output_size']).to(self.device)
        else:
            if model is None:
                raise ValueError('Модель не была загружена, передайте в параметры название файла модели')
            else:
                self.model, self.scaler_x, self.scaler_y = self.download_model()

        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=nn_params['learning_rate'])
        self.scaler_x = None
        self.scaler_y = None

        # Настройка датасета
        self.dataset_filename = dataset_filename
        self.dataset = None

    def load_dataset(self):
        self.dataset = parallel_loader(self.dataset_filename)

    def train_model(self, train_loader, test_loader):
        # Ваш код обучения модели
        for epoch in range(self.nn_params['num_epochs']):
            for batch_inp, batch_out in train_loader:
                self.model.train()
                outputs = self.model(batch_inp)
                loss = self.criterion(outputs, batch_out)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            print(f'Epoch: {epoch}, Loss: {loss.item():.5f}')

        # Тестирование
        final_loss = []
        self.model.eval()
        for batch_inp, batch_out in test_loader:
            outputs = self.model(batch_inp)
            loss = self.criterion(outputs, batch_out)
            final_loss.append(loss.item())

        print(f'Model error: {np.mean(final_loss) * 100:.5f} %')

    def main(self):
        # Загрузка данных
        self.logger.info('Loading dataset...')
        data = parallel_loader(self.dataset_filename)
        self.logger.info('Loading dataset completed!')

        # Разбиение на обучающий и тестовый наборы
        self.logger.info('Splitting data...')
        train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

        # Предобработка и нормализация данных
        self.logger.info('Data preprocessing...')
        train_loader, test_loader = self.data_preprocessing(train_data, test_data)

        # Обучение модели
        self.train_model(train_loader, test_loader)

        # Сохранение модели
        self.logger.info(f'Saving model to {self.model_name + "_new"}')
        self.save_model()

if __name__ == "__main__":
    params = {"MODEL_NAME": "test_model.pth"}
    nn_params = {
        'input_size': 8,
        'hidden_size': 32,
        'hidden_size_two': 64,
        'hidden_size_three': 32,
        'output_size': 1,
        'num_epochs': 100,
        'learning_rate': 0.001,
        'batch_size': 32
    }
    dataset_filename = "DATASET.json"

    freeze_support()

    ml_module = MLModule(params=params, nn_params=nn_params, dataset_filename=dataset_filename)
    ml_module.main()