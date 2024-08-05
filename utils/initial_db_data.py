import requests

URL_DATA_STORAGE = "http://localhost:3000"

# Добавляем модели датчиков
requests.post(
    url=f"{URL_DATA_STORAGE}/sensor_model",
    json={"name": "unit1", "description": "unit1"},
)  # Температура
requests.post(
    url=f"{URL_DATA_STORAGE}/sensor_model",
    json={"name": "unit2", "description": "unit2"},
)  # Давление
requests.post(
    url=f"{URL_DATA_STORAGE}/sensor_model",
    json={
        "name": "Датчик влажности стандартный",
        "description": "Датчик влажности стандартный",
    },
)  # Влажность

# Добавляем точки измерения
requests.post(
    url=f"{URL_DATA_STORAGE}/measurement_source",
    json={"name": "Pressure_unit1", "description": "Pressure_unit1", "unit": "Паскали"},
)  # Давление 1
requests.post(
    url=f"{URL_DATA_STORAGE}/measurement_source",
    json={
        "name": "Temperature_unit1",
        "description": "Temperature_unit1",
        "unit": "Цельсии",
    },
)  # Температура 1
requests.post(
    url=f"{URL_DATA_STORAGE}/measurement_source",
    json={
        "name": "Humidity_unit1",
        "description": "Humidity_unit1",
        "unit": "Проценты",
    },
)  # Влажность
requests.post(
    url=f"{URL_DATA_STORAGE}/measurement_source",
    json={
        "name": "Temperature_unit2",
        "description": "Temperature_unit2",
        "unit": "Цельсии",
    },
)  # Температура 2
requests.post(
    url=f"{URL_DATA_STORAGE}/measurement_source",
    json={"name": "Pressure_unit2", "description": "Pressure_unit2", "unit": "Паскали"},
)  # Давление 2

# Добавляем датчики
data1 = {
    "parameters": {},
    "type": "random",
    "properties": [
        {"name": "Pressure_unit1", "parameters": {}, "measurement_source_id": 1},
        {"name": "Temperature_unit1", "parameters": {}, "measurement_source_id": 2},
    ],
    "is_active": True,
    "description": "unit1",
    "sensor_model_id": 1,
}
data2 = {
    "parameters": {},
    "type": "random",
    "properties": [
        {"name": "Pressure_unit2", "parameters": {}, "measurement_source_id": 5},
        {"name": "Temperature_unit2", "parameters": {}, "measurement_source_id": 4},
    ],
    "is_active": True,
    "description": "unit2",
    "sensor_model_id": 2,
}

data3 = {
    "parameters": {},
    "type": "random",
    "properties": [
        {"name": "Humidity_unit1", "parameters": {}, "measurement_source_id": 3}
    ],
    "is_active": True,
    "description": "all",
    "sensor_model_id": 3,
}

requests.post(url=f"{URL_DATA_STORAGE}/sensor", json=data1)
requests.post(url=f"{URL_DATA_STORAGE}/sensor", json=data2)
requests.post(url=f"{URL_DATA_STORAGE}/sensor", json=data3)
