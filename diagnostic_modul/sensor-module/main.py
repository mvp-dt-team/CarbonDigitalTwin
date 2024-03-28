from classes import Handler, Source, Model, create_database
import os

sources = [
    Source(id=0, unit=1, number=1, address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")),
    Source(id=1, unit=1, number=1, address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")),
    Source(id=2, unit=1, number=1, address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")),
    Source(id=3, unit=1, number=1, address=os.path.abspath("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4"))
]

print(os.path.abspath('./data/videos/test-video-1.mp4'))

models = [
    Model(version='0.0.1', path="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\models\\model_YOLO8s.pt")
]
create_database()
test_handler = Handler()
test_handler.polling_interval = 2
test_handler.add_source_model_mapping(source=sources[0], model=models[0])
test_handler.add_source_model_mapping(source=sources[1], model=models[0])
test_handler.add_source_model_mapping(source=sources[2], model=models[0])
test_handler.add_source_model_mapping(source=sources[3], model=models[0])
test_handler.run()

