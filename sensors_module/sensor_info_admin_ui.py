import requests
from pydantic import BaseModel
import json

from network_models.measurement_source_info import MeasurementSourceInfo
from network_models.sensor_model_info import SensorModelInfo

API_BASE_URL = 'http://localhost:3000'


def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def execute_api_request(method: str, url: str, data=None, success_message: str = None,
                        error_message: str = "Ошибка при выполнении запроса"):
    try:
        if method.upper() == 'GET':
            response = requests.get(url)
        elif method.upper() == 'POST':
            print("Данные, которые будут отправлены:")
            print_json(data)
            confirm = input("Подтвердите отправку (да/нет): ")
            if confirm.lower() == "да":
                response = requests.post(url, json=data)
            else:
                print("Отправка отменена.")
                return
        else:
            print(f"Метод {method} не поддерживается.")
            return

        if response.status_code in [200, 201]:
            print(success_message if success_message else "Успешно.")
            if response.content and response.content.decode('utf-8') != 'null':
                print_json(response.json())
        else:
            print(error_message, " код ответа: ", response.status_code)
    except Exception as e:
        print(f"{error_message}: {e}")


def get_measurement_sources():
    execute_api_request('GET', f"{API_BASE_URL}/measurement_source",
                        success_message="Список источников измерений получен успешно.")


def add_measurement_source():
    print("Добавление источника измерений.")
    name = input("Введите имя: ")
    description = input("Введите описание (можно пропустить): ")
    unit = input("Введите единицу измерения: ")

    source = MeasurementSourceInfo(name=name, description=description, unit=unit).dict(exclude_none=True)
    execute_api_request('POST', f"{API_BASE_URL}/measurement_source", data=source,
                        success_message="Источник измерений добавлен успешно.")


def get_sensor_models():
    execute_api_request(
        'GET',
        f"{API_BASE_URL}/sensor_model",
        success_message="Список моделей датчиков получен успешно."
    )


def add_sensor_model():
    print("Добавление модели датчика.")
    name = input("Введите имя модели: ")
    description = input("Введите описание модели (можно пропустить): ")

    model = SensorModelInfo(name=name, description=description)

    execute_api_request(
        'POST',
        f"{API_BASE_URL}/sensor_model",
        data=model.dict(exclude_none=True),
        success_message="Модель датчика добавлена успешно."
    )


def main_menu():
    actions = [
        {"name": "Получить список источников измерений", "function": get_measurement_sources},
        {"name": "Добавить источник измерений", "function": add_measurement_source},
        {"name": "Получить список моделей датчиков", "function": get_sensor_models},
        {"name": "Добавить модель датчика", "function": add_sensor_model},
        {"name": "Выйти", "function": exit}
    ]

    while True:
        for i, action in enumerate(actions, start=1):
            print(f"{i}. {action['name']}")

        choice = input("Выберите действие: ")
        if choice.isdigit() and 1 <= int(choice) <= len(actions):
            selected_action = actions[int(choice) - 1]
            if selected_action["name"] == "Выйти":
                print("Выход.")
                break
            else:
                selected_action["function"]()
        else:
            print("Неверный ввод, пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main_menu()
