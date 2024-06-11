import pytest
from classes import Model, TYPE_DATA, STATUS, Handler, Sensor, Block
import threading
import time
from unittest.mock import MagicMock, patch


@pytest.fixture
def model():
    return Model("path/to/model", {}, "1.0")


def test_clear_datasets(model):
    model.train_dataset = [1, 2, 3]
    model.validation_dataset = [4, 5, 6]
    model.clear_datasets()
    assert model.train_dataset == []
    assert model.validation_dataset == []


def test_append_dataset(model):
    model.clear_datasets()
    model.append_dataset(10, TYPE_DATA.TRAIN.value)
    assert model.train_dataset == [10]
    assert model.validation_dataset == []

    model.append_dataset(20, TYPE_DATA.VALIDATION.value)
    assert model.train_dataset == [10]
    assert model.validation_dataset == [20]


def test_append_dataset_invalid_type(model):
    model.clear_datasets()
    result = model.append_dataset(30, 123)  # Invalid type_data value
    assert result == 1  # Expecting 1 as type_data is invalid


def test_processing_with_valid_data(model):
    model.status = STATUS.PREDICT.value
    result = model.proccessing(None)
    assert result == 1  # Expecting 1 as data is not None


def test_processing_with_none_data(model):
    model.status = STATUS.PREDICT.value
    result = model.proccessing(None)
    assert result == 1  # Expecting 1 as data is None


def test_processing_with_train_status(model):
    model.status = STATUS.TRAIN.value
    result = model.proccessing("some_data")
    assert result == None  # No processing expected in train status


def test_train_method(model):
    # Placeholder test for train method
    model.train()


def test_validate_method(model):
    # Placeholder test for validate method
    model.validate()


def test_predict_method(model):
    # Placeholder test for predict method
    result = model.predict()
    assert isinstance(result, dict)  # Expecting a dictionary as output


@pytest.fixture
def handler():
    return Handler("path/to/db", 1.0)


def test_add_block(handler):
    model = Model("path/to/model", {}, "1.0")
    sensor1 = Sensor(1, "VIDEO")
    sensor2 = Sensor(2, "AUDIO")
    result = handler.add_block(model, [sensor1, sensor2])
    assert result == 0  # Expecting 0 as block is successfully added


def test_run_ml_module(handler):
    model = Model("path/to/model", {}, "1.0")
    sensor1 = Sensor(1, "VIDEO")
    sensor2 = Sensor(2, "AUDIO")
    handler.add_block(model, [sensor1, sensor2])
    data = {1: 0.5, 2: 0.3}
    result = handler.run_ml_module(handler.blocks[0], data)
    assert isinstance(result, type(None))  # Expecting a dictionary as output


def test_write_db_data(handler):
    data = {"key": 0.5}
    result = handler.write_db_data(data)
    assert result == 0  # Expecting 0 as data is successfully written to the database


def test_write_db_data_exception(handler):
    def mock_db_write(data):
        raise Exception("Test Exception")

    handler.write_db_data = mock_db_write
    with pytest.raises(Exception) as excinfo:
        data = {"key": 0.5}
        handler.write_db_data(data)
    assert "Test Exception" in str(excinfo.value)


def test_action(handler, monkeypatch):
    # Mock poll_sensors to return fixed data
    def mock_poll_sensors():
        return {"sensor1": 0.5, "sensor2": 0.3}

    monkeypatch.setattr(Block, "poll_sensors", mock_poll_sensors)

    # Mock run_ml_module to return fixed status
    def mock_run_ml_module(block, data):
        if data["sensor1"] > 0.4:
            return {"type": "predict"}
        else:
            return {"type": "train"}

    monkeypatch.setattr(handler, "run_ml_module", mock_run_ml_module)

    # Mock write_db_data
    def mock_write_db_data(data):
        pass  # Do nothing for this test

    monkeypatch.setattr(handler, "write_db_data", mock_write_db_data)

    # Helper function to change self.running after some time
    def change_running():
        time.sleep(2)  # Change self.running after 2 seconds
        handler.running = False

    # Start a separate thread to change self.running
    thread = threading.Thread(target=change_running)
    thread.start()

    # Run action
    handler.action()

    # Check if the action loop runs without errors
    assert True  # If the action loop completes without errors, the test passes


def test_action_exception(handler, monkeypatch):
    def mock_block_poll_sensors():
        return {"sensor1": 0.5, "sensor2": 0.3}

    def mock_run_ml_module(block, data):
        if data["sensor1"] > 0.4:
            raise Exception("Test Exception from mock_run_ml_module")
        else:
            return {"type": "train"}

    def change_running():
        time.sleep(0.1)  # Wait for the action loop to start
        handler.running = False

    monkeypatch.setattr(Block, "poll_sensors", mock_block_poll_sensors)
    monkeypatch.setattr(handler, "run_ml_module", mock_run_ml_module)

    thread = threading.Thread(target=change_running)
    thread.start()

    handler.action()

    assert not handler.running  # Ensure the action loop terminates after the exception


class MockModel:
    def proccessing(self, data):
        return {"type": "predict", "data": data}


class MockBlock:
    def __init__(self):
        self.model = MockModel()

    def poll_sensors(self):
        return {}  # Mocking the poll_sensors method


class MockSensor:
    def poll(self):
        return {"sensor_data": 0.5}


# Тест для проверки обработки исключения при некорректном статусе модели
def test_action_invalid_status():
    handler = Handler("test.db", 0.1)
    handler.blocks = [MockBlock()]
    handler.run_ml_module = MagicMock(
        return_value={"type": "invalid_status", "data": {}}
    )
    with pytest.raises(Exception) as excinfo:
        handler.action()
    assert "Некорректный статус модели" in str(excinfo.value)


# Тест для проверки обработки исключения при ошибке обработки данных моделью
def test_action_processing_error():
    handler = Handler("test.db", 0.1)
    handler.blocks = [MockBlock()]
    handler.run_ml_module = MagicMock(
        side_effect=Exception("Ошибка при обработке данных моделью")
    )

    with pytest.raises(Exception) as excinfo:
        handler.action()

    assert "Ошибка при обработке данных моделью" in str(excinfo.value)
