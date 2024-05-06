from classes import Handler, Source, Model
import os
import requests
import json

sources = []

url = 'localhost:5000'

getting_sources = requests.get(f'http://{url}/camera')
if getting_sources.ok:
    sources_json = json.loads(getting_sources.text)
    for camera in sources_json:
        print(camera)
        sources.append(Source(id=int(camera['id']), address=camera['ip'], description=camera['description']))
else:
    raise ConnectionError('Нет подключения к серверу')

print(os.path.abspath('./data/videos/test-video-1.mp4'))

models = {}

for camera in sources:
    getting_model = requests.get(f'http://{url}/camera/{camera.id}/model')
    if getting_model.ok:
        with open(f'model_{camera.id}.pt', 'wb') as f:
            f.write(getting_model.content)
        models[camera.id] = Model(path=os.path.abspath(f'model_{camera.id}.pt'), version='0.0.1')
        print("Модель сохранена успешно.")
    else:
        print("Ошибка при получении модели:", getting_model.status_code)

test_handler = Handler(url=url)
# Необходимо реализорвать через конфиг файл
test_handler.polling_interval = 2

# В дальнейшем такая настройка будет производиться в приложении
for camera in sources:
    test_handler.add_source_model_mapping(source=camera, model=models[camera.id])

test_handler.run()

