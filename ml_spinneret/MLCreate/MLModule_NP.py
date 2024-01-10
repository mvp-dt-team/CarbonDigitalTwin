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


class MLmodule:
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
        # self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = torch.device("cpu")
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
        self.logger.info('Загрузка датасета ...')
        self.load_dataset()
        self.logger.info('Загрузка датасета завершена!')

    def load_dataset(self):
        with open(self.dataset_filename, 'r') as file:
            self.dataset = json.load(file)

    def data_preprocessing(self, outer_values, central_values):
        self.logger.info('Предобработка данных')

        outer_x = np.array(outer_values, dtype=np.float32).T
        central_y = np.array(central_values, dtype=np.float32)

        outer_x = torch.tensor(outer_values, dtype=torch.float32)
        central_y = torch.tensor(central_values, dtype=torch.float32)

        X = outer_x.t()
        y = central_y.view(-1, 1)

        # Нормализация данных
        self.logger.info('Нормализация данных')
        self.scaler_x = StandardScaler()
        self.scaler_y = StandardScaler()

        # Разделение данных на обучающий и тестовый наборы
        self.logger.info('Разбиение данных')
        X_train, X_test, y_train, y_test = train_test_split(outer_x, central_y, test_size=0.2, random_state=42)

        # Преобразование данных в тензоры PyTorch
        if not torch.cuda.is_available():
            X_train_scaled = torch.tensor(self.scaler_x.fit_transform(X_train), dtype=torch.float32).to('cuda')
            y_train_scaled = torch.tensor(self.scaler_y.fit_transform(y_train.reshape(-1, 1)), dtype=torch.float32).to('cuda')

            X_test_scaled = torch.tensor(self.scaler_x.transform(X_test), dtype=torch.float32).to('cuda')
            y_test_scaled = torch.tensor(self.scaler_y.transform(y_test.reshape(-1, 1)), dtype=torch.float32).to('cuda')
        else:
            X_train_scaled = torch.tensor(self.scaler_x.fit_transform(X_train), dtype=torch.float32)
            y_train_scaled = torch.tensor(self.scaler_y.fit_transform(y_train.reshape(-1, 1)), dtype=torch.float32)

            X_test_scaled = torch.tensor(self.scaler_x.transform(X_test), dtype=torch.float32)
            y_test_scaled = torch.tensor(self.scaler_y.transform(y_test.reshape(-1, 1)), dtype=torch.float32)

        train_set = TensorDataset(X_train_scaled, y_train_scaled)
        test_set = TensorDataset(X_test_scaled, y_test_scaled)

        train_loader = DataLoader(train_set, batch_size=self.nn_params['batch_size'], shuffle=True)
        test_loader = DataLoader(test_set, batch_size=self.nn_params['batch_size'], shuffle=True)


        return train_loader, test_loader

    def fit_model(self, outer_values, central_values):
        train_loader, test_loader = self.data_preprocessing(outer_values, central_values)
        self.logger.info('Обучение сети')
        for epoch in range(self.nn_params['num_epochs']):
            for batch_inp, batch_out in tqdm(train_loader):
                self.model.train()

                outputs = self.model(batch_inp)
                loss = self.criterion(outputs, batch_out)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            self.logger.info(f'Epoch: {epoch}, Loss: {loss.item():.5f}')

        self.logger.info(f'Тестирование ...')

        final_loss = []
        self.model.eval()
        for batch_inp, batch_out in tqdm(test_loader):
            outputs = self.model(batch_inp)
            loss = self.criterion(outputs, batch_out)
            final_loss.append(loss.item())    
        self.logger.info(f'Ошибка модели составляет: {np.mean(final_loss) * 100:5f} %')
        return np.mean(final_loss)

    def save_model(self):
        checkpoint = {'model_state_dict': self.model.state_dict(),
                      'scaler_x_mean': self.scaler_x.mean_,
                      'scaler_x_scale': self.scaler_x.scale_,
                      'scaler_y_mean': self.scaler_y.mean_,
                      'scaler_y_scale': self.scaler_y.scale_, }

        torch.save(checkpoint, self.model_name + "_new")

    def download_model(self):
        model_new = NNetwork(self.nn_params['input_size'], self.nn_params['hidden_size'],
                             self.nn_params['hidden_size_two'], self.nn_params['hidden_size_three'],
                             self.nn_params['output_size'])

        checkpoint = torch.load(self.model_name)
        model_new.load_state_dict(checkpoint['model_state_dict'])

        scaler_x = StandardScaler()
        scaler_x.mean_ = checkpoint['scaler_x_mean']
        scaler_x.scale_ = checkpoint['scaler_x_scale']

        scaler_y = StandardScaler()
        scaler_y.mean_ = checkpoint['scaler_y_mean']
        scaler_y.scale_ = checkpoint['scaler_y_scale']
        return model_new, scaler_x, scaler_y

    def action(self):
        all_outer_values = []
        all_central_values = []
        self.logger.info(f'Разбитие на samples')
        for item in tqdm(self.dataset):
            all_outer_values.append(item['input'])
            all_central_values.append(item['output'])

        loss = self.fit_model(all_outer_values, all_central_values)

        self.logger.info(f'Модель обучена, сохраняю модель в файл {self.model_name + "_new"}')
        self.save_model()
        return loss
