# Модуль компьютерного зрения

## Сущности проекта

### Handler

#### Внутренние переменные
1. logger: logging.logger
2. models: List[Model]
3. sources: List[Source]
4. queue: Queue
5. source_model_mapping: dict
6. polling_interval: int
7. running: bool
8. url: str
9. frequency_archivating: int

#### Функционал
1. Связывание модели с камерой ```add_source_model_mapping(self, source, model) -> None```. связка заносится в переменную ```source_model_mapping```
2. Опрос датчиков для получения изображения с камеры ```polling_sensors(self) -> dict```
3. Получение результат предсказания модели по переданному изображению ```value_predict(self, source_id: int, source_value: Image) -> dict```
4. Отправка данных в модуль хранения данных ```write_db_request(self, source_id: int, prediction: float) -> int```, возвращает код ошибки (0 - успех, 1 - ошибка).
5. Отправка изображение в модуль хранения данных ```archiving_images(self, source_id: int, image: Image) -> int```, возвращает код ошибки (0 - успех, 1 - ошибка).
6. Вычисление показателя дефектности по результатам прогноза ```processing_values(self, defects: List[dict]) -> float```
7. Основаная функция работы модуля ```def run(self) -> None```
8. Функция остановки работы модуля ```def stop(self) -> None```

- Формат словаря, отправляемый моделью (результат работы): {source_id(int): result(float)}
- Эндпоинт rest api для отправки результата в модуль хранения: POST http://storage-module-address/camera/\<camera_id\> -H "Content-Type: application/json" -d '{"value": 12.34}
- Формат словаря при опросе сенсоров: {source_id(int): image(PIL.Image)}
- Эндпоинт rest api для отправки изображения в модуль хранения: POST http://storage-module-address/camera/\<camera_id\>/archivate -F "image=@/path/to/your/image.jpg"

### Source

#### Внутренние переменные
1. id: int
2. description: str
3. address: str

#### Функционал
1. Получение изображения с камеры ```get_value(self) -> Image```

### Model
#### Внутренние переменные
1. path: str

#### Функционал
1. Прогноз модели по изображению ```predict(self, frame: Image) -> Tensor```