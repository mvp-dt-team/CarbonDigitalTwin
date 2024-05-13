import pytest
from queue import Queue
from unittest.mock import MagicMock
from classes import Handler, Source, Model, create_database
from PIL import Image
from threading import Thread
import time

create_database()

def test_add_source_model_mapping():
    handler = Handler()
    source = Source(id=1, unit="camera", number=1, address="video.mp4")
    model = Model(version="v1", path="model.pt")

    handler.add_source_model_mapping(source, model)
    assert source in handler.sources
    assert model in handler.models
    assert handler.source_model_mapping[source.id] == model

def test_polling_sensors():
    handler = Handler()
    source = Source(id=1, unit="camera", number=1, address="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\images\\test_image.png")
    model = Model(version="v1", path="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\models\\model_YOLO8s.pt")
    source.get_value = MagicMock(return_value="test_image")

    handler.add_source_model_mapping(source, model)
    data = handler.polling_sensors()
    assert isinstance(data, dict)
    assert data[source.id] == "test_image"

def test_value_predict():
    handler = Handler()
    source = Source(id=2, unit="camera", number=2, address="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")
    model = Model(version="v1", path="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\models\\model_YOLO8s.pt")
    image = Image.open("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\images\\test_image.png")

    handler.add_source_model_mapping(source, model)
    result = handler.value_predict(source.id, image)
    assert isinstance(result, dict)

def test_write_db_request():
    handler = Handler()
    source_id = 1
    prediction = 0.5

    result = handler.write_db_request(source_id, prediction)
    assert result == 0

def test_processing_values():
    handler = Handler()
    defects = [{'class_': 0, 'confidence_': 0.9}, {'class_': 0, 'confidence_': 0.8}]
    result = handler.processing_values(defects)
    assert result == pytest.approx(0.0425, abs=1e-4)

def test_run():
    handler = Handler()
    def stop_handler():
        time.sleep(5)
        handler.stop()

    sources = [
        Source(id=0, unit=1, number=1, address="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4"),
    ]

    models = [
        Model(version='0.0.1', path="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\models\\model_YOLO8s.pt")
    ]

    stop_thread = Thread(target=stop_handler)
    stop_thread.start()

    handler.polling_interval = 2
    handler.add_source_model_mapping(source=sources[0], model=models[0])

    handler_thread = Thread(target=handler.run)
    handler_thread.start()

    handler_thread.join()

    assert not handler_thread.is_alive()

def test_run_err_1():
    with pytest.raises(Exception):
        handler = Handler()
        def stop_handler():
            time.sleep(5)
            handler.stop()

        sources = [
            Source(id=0, unit=1, number=1, address="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4"),
        ]

        stop_thread = Thread(target=stop_handler)
        stop_thread.start()

        handler.polling_interval = 2
        handler.add_source_model_mapping(source=sources[0], model=None)
        handler_thread = Thread(target=handler.run)
        handler_thread.start()

        handler_thread.join()

        assert not handler_thread.is_alive()

def test_run_err_2():
    with pytest.raises(Exception):
        handler = Handler()
        def stop_handler():
            time.sleep(5)
            handler.stop()

        stop_thread = Thread(target=stop_handler)
        stop_thread.start()

        handler.polling_interval = 2
        handler.add_source_model_mapping(source=None, model=None)

        handler_thread = Thread(target=handler.run)
        handler_thread.start()

        handler_thread.join()

        assert not handler_thread.is_alive()
