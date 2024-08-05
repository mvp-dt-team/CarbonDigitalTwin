# Digital_Twin_Carbon
Модуль машинного обучения для MVP программного обеспечения цифрового двойника ПАН

Используется Python версии 1.12.4

_Предварительно должен быть запущен модуль хранения данных_

## Установка

pip install -r requirements

## Запуск

python main.py

## Документация

Для тестрования создан ноутбук, который генерирует данные и модель для предсказания этих данных simulating_data.ipynb

## Доработка

1. Файл запуска содержит лишние принты, которые использовались для отладки
2. Нет тестов модуля, которые необходимы для валидации модуля
3. Нет корректной обработки ошибок при запуске модуля и дальнейшей работе (При возникновении модуль автоматически выключается)
4. Не дописана документация для описания алгоритма работы