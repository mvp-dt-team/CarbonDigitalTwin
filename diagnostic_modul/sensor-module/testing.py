import unittest
from queue import Queue
from unittest.mock import MagicMock
from classes import Handler, Source, Model, create_database
from PIL import Image

create_database()

class TestHandler(unittest.TestCase):
    def setUp(self):
        self.handler = Handler()
        

    def test_add_source_model_mapping(self):
        source = Source(id=1, unit="camera", number=1, address="video.mp4")
        model = Model(version="v1", path="model.pt")

        self.handler.add_source_model_mapping(source, model)
        self.assertIn(source, self.handler.sources)
        self.assertIn(model, self.handler.models)
        self.assertEqual(self.handler.source_model_mapping[source.id], model)

    def test_polling_sensors(self):
        source = Source(id=1, unit="camera", number=1, address="video.mp4")
        source.get_value = MagicMock(return_value="test_image")

        self.handler.add_source_model_mapping(source, None)
        data = self.handler.polling_sensors()
        self.assertIsInstance(data, dict)
        self.assertEqual(data[source.id], "C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\images\\test_image.png")

    def test_value_predict(self):
        source = Source(id=1, unit="camera", number=1, address="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\videos\\test-video.mp4")
        model = Model(version="v1", path="C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\\models\\model_YOLO8s.pt")
        image = Image("C:\\Users\\boiko.k.v\\Desktop\\Carbon-Digital-Twin\\diagnostic_modul\\sensor-module\\data\images\\test_image.png")

        self.handler.add_source_model_mapping(source, model)
        result = self.handler.value_predict(source.id, image)
        self.assertIsInstance(result, dict)

    def test_write_db_request(self):
        source_id = 1
        prediction = 0.5

        result = self.handler.write_db_request(source_id, prediction)
        self.assertEqual(result, 0)

    def test_processing_values(self):
        defects = [{'class_': 0, 'confidence_': 0.9}, {'class_': 0, 'confidence_': 0.8}]
        result = self.handler.processing_values(defects)
        self.assertAlmostEqual(result, 0.0425, places=4)

    # def test_run(self):
    #     # Тестирование выполнения без ошибок
    #     self.handler.queue.put({1: "test_data"})
    #     self.handler.run()

if __name__ == '__main__':
    unittest.main()
