import requests

URL_DATA_STORAGE = "http://localhost:3000"


# Добавляем модели датчиков
requests.post(
    url=f"{URL_DATA_STORAGE}/sensor_model",
    json={"name": "unit1", "description": "unit1"},
)

# Добавляем точки измерения
requests.post(
    url=f"{URL_DATA_STORAGE}/measurement_source",
    json={"name": "Pressure_unit1", "description": "Pressure_unit1", "unit": "Паскали"},
)

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

requests.post(url=f"{URL_DATA_STORAGE}/sensor", json=data1)
