import requests
import json

data_storage_address = 'http://localhost:3000'
url = data_storage_address + '/measurement'

data = {
    "query_id": 145,
    "insert_ts": '2024-03-31 15:44:54.179336',
    "insert_values": [
        {
            "m_data": 25.5,
            "sensor_item_id": 1,
            "measurement_source_id": 1
        },
        {
            "m_data": 26.3,
            "sensor_item_id": 2,
            "measurement_source_id": 2
        }
    ]
}

# Заголовки запроса
headers = {'Content-Type': 'application/json'}

# Отправка POST-запроса
response = requests.post(url, data=json.dumps(data), headers=headers)

# Вывод ответа от сервера
print(f'Status Code: {response.status_code}')
print(f'Response Body: {response.json()}')


def fetch_data(url: str):
    try:
        measurement_source_ids = [1, 2, 3]

        response = requests.get(url, params={'measurement_source_ids': measurement_source_ids})

        response.raise_for_status()  # Это вызовет исключение для кодов состояния 4xx/5xx
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return []

print(str(fetch_data(url)))
