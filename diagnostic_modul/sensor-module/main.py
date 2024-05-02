from classes import Handler, Source, Model, create_database
import os
import requests

sources = [
    Source(id=0, description='source 1 unit 1 number 1', address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")),
    Source(id=1, description='source 2 unit 1 number 1', address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")),
    Source(id=2, description='source 3 unit 1 number 1', address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")),
    Source(id=3, description='source 4 unit 1 number 1', address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4"))
]

getting_sources = requests.get('http://storage-module-address/camera')
if getting_sources.ok:
    for camera in getting_sources:
        sources.append(Source(id=camera['id'], address=camera['ip'], description=camera['description']))
else:
    raise ConnectionError('Нет подключения к серверу')

print(os.path.abspath('./data/videos/test-video-1.mp4'))

models = {}

for camera in sources:
    getting_model = requests.get(f'http://storage-module-address/camera/{camera.id}/model')
    if getting_model.ok:
        with open(f'model_{camera.id}', 'wb') as f:
            f.write(getting_model.content)
        models[camera.id] = Model(path=os.path.abspath(f'model_{camera.id}'))
        print("Модель сохранена успешно.")
    else:
        print("Ошибка при получении модели:", getting_model.status_code)

create_database()
test_handler = Handler()
# Необходимо реализорвать через конфиг файл
test_handler.polling_interval = 2

# В дальнейшем такая настройка будет производиться в приложении
for camera in sources:
    test_handler.add_source_model_mapping(source=camera, model=models[camera.id])

test_handler.run()

