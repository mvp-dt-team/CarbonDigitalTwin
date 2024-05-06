# Договоренности по интеграции модуля хранения к другим модулям
## Модуль компьютерного зрения
- Модуль хранения будет содержать записи об ip камеры и информацию о ее местонахождении
- Каждой камере будет присвоен идентификационный номер, который нужно указывать при последующих запросах, номер приходит вместе с остальной информацией о камере
- При инициализации модуль комп. зрения запрашивает информацию о камерах:
`curl -X GET http://storage-module-address/camera`

    Пример ответа:
     ``` json
    [
        {
            "ip": "192.168.1.101",
            "id": "1",
            "description": "Выход из фильеры"
        },
        {
            "ip": "192.168.1.102",
            "id": "2",
            "description": "На входе в печь термостабилизации"
        }
    ]
    ```
- При инициализации также запрашиваются предобученные модели.
    Пример кода на питон, который запрашивает модели и сохраняет их в файл:
    ```python
  import requests
    camera_id = '123'  # Пример ID камеры
    url = f'http://storage-module-address/camera/{camera_id}/model'
    
    response = requests.get(url)
    if response.ok:
        with open('model_filename', 'wb') as f:
            f.write(response.content)
        print("Модель сохранена успешно.")
    else:
        print("Ошибка при получении модели:", response.status_code)
  ```
- После анализа сделанных фотографий результат так же передается модулю хранения, пример для камеры номер 123:

    `curl -X POST http://storage-module-address/camera/123 -H "Content-Type: application/json" -d '{"value": 12.34}'`

    При успешном добавлении вернется код ответа 200
- Также переодически будут архивироваться изображения с камер, для этого нужно отправить запрос:
    
  ```curl -X POST http://storage-module-address/camera/123/archivate -F "image=@/path/to/your/image.jpg"```
    
    или вариант на python

    ``` python
  import requests
    url = 'http://storage-module-address/camera/123/archivate'
    files = {'image': open('/path/to/your/image.jpg', 'rb')}
    
    response = requests.post(url, files=files)
    print(response.text)
  ```
- Изменение ip адреса камеры будет возможно через панель администратора

## Модуль анализа свойств волокна
- Для выбора датасета необходимо предоставить способы получения информации о датчиках, ниже представлены примеры запросов и ответов:
  - ```curl -X GET http://storage-module-address/measurement_source```
    ```json
    [
      {
        "id": 1,
        "name": "Температура на входе в фильеру ",      
        "unit": "0"
      },
      {
        "id": 2,
        "name": "Расход растворителя",
        "unit": "1"
      }
    ]    
    ```
  - ```curl -X GET http://storage-module-address/sensors_by_source?id=1```
    ```json
    [
      {
        "description": "Датчик в зоне А",
        "installation_time": "2020-01-01T00:00:00Z",
        "deactivation_time": "2021-01-01T00:00:00Z",
        "model_name": "Модель A"
      },
      {
        "description": "Датчик в зоне В",
        "installation_time": "2020-05-01T00:00:00Z",
        "deactivation_time": null,
        "model_name": "Модель B"
      }
    ]
    ```
- Запрос на получения данных будет выглядеть так:
    ```shell
    curl -X POST http://storage-module-address/measurement_data \
    -H "Content-Type: application/json" \
    -d '{
      "measurements": [
        {
          "sensor_id": 101,
          "measurement_source_id": 1,
          "time_from": "2022-01-01T00:00:00Z",
          "time_to": "2022-01-10T00:00:00Z"
        },
        {
          "sensor_id": 102,
          "measurement_source_id": 2,
          "time_from": "2022-02-01T00:00:00Z",
          "time_to": "2022-02-10T00:00:00Z"
        }
      ]
    }'
    ```

    Ответ:
    
  ```json
  [
    {
      "measurement_source_id": 1,
      "data": [10.5, 10.7, 10.8]
    },
    {
      "measurement_source_id": 2,
      "data": [1.1, 1.2, 1.3]
    }
  ]
    ```