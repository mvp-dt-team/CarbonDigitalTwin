import pyodbc
import time
import random
from datetime import datetime


# Функция для генерации случайных значений в зависимости от типа данных
def generate_random_value(data_type):
    if data_type == "DOUBLE":
        return random.uniform(0.0, 100.0)  # Примерный диапазон для вещественных чисел
    elif data_type == "INTEGER":
        return random.randint(0, 100)  # Примерный диапазон для целых чисел
    elif data_type == "DATETIME":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif data_type == "SMALLINT":
        return random.randint(0, 10)
    return None


# Словарь с описанием типов данных для каждого столбца
data_types = {
    "DT": "DATETIME",
    "TM": "DATETIME",
    "Pressure1": "DOUBLE",
    "MELT12": "DOUBLE",
    "TP14": "SMALLINT",
    "TP13": "DOUBLE",
    "TP12": "DOUBLE",
    "TP11": "DOUBLE",
    "MELT10": "DOUBLE",
    "TP10": "DOUBLE",
    "TP9": "DOUBLE",
    "MELT8": "DOUBLE",
    "TP8": "DOUBLE",
    "TP7": "DOUBLE",
    "MELT6": "DOUBLE",
    "TP6": "DOUBLE",
    "TP5": "DOUBLE",
    "MELT4": "DOUBLE",
    "TP4": "DOUBLE",
    "TP3": "DOUBLE",
    "MELT2": "DOUBLE",
    "TP2": "DOUBLE",
    "TP1": "DOUBLE",
    "I1": "DOUBLE",
    "RPM8": "DOUBLE",
    "RPM7": "DOUBLE",
    "RPM6": "DOUBLE",
    "RPM5": "DOUBLE",
    "RPM4": "DOUBLE",
    "RPM3": "DOUBLE",
    "RPM2": "DOUBLE",
    "RPM1": "DOUBLE",
    "Feeder1": "INTEGER",
    "Feeder2": "INTEGER",
    "Feeder3": "INTEGER",
    "Feeder4": "INTEGER",
    "MELT14": "DOUBLE",
    "TP15": "DOUBLE",
    "GP_T": "DOUBLE",
    "GP_RPM": "DOUBLE",
    "TEMP_IN": "DOUBLE",
    "TEMP_GP": "DOUBLE",
    "TEMP_OUT": "DOUBLE",
    "TEMP_MELT_IN": "DOUBLE",
    "TEMP_MELT_OUT": "DOUBLE",
    "P_IN": "DOUBLE",
    "P_OUT": "DOUBLE",
}

conn_str = (
    r"DRIVER={Driver do Microsoft Access (*.mdb)};" r"DBQ=D:\Twin14z\db\TWIN14Z_DB.mdb;"
)

cnxn = pyodbc.connect(conn_str)
crsr = cnxn.cursor()

try:
    while True:
        # Собираем случайные данные для всех столбцов
        columns = ", ".join(data_types.keys())
        placeholders = ", ".join("?" for _ in data_types)
        values = [generate_random_value(data_types[col]) for col in data_types]

        # SQL запрос для вставки данных
        query = f"INSERT INTO TwinScrew ({columns}) VALUES ({placeholders})"
        crsr.execute(query, values)
        cnxn.commit()
        print("Отправлено.")

        time.sleep(10)  # Пауза в 10 секунд
except KeyboardInterrupt:
    print("Программа была остановлена пользователем.")
finally:
    # Закрываем курсор и соединение
    crsr.close()
    cnxn.close()
    print("Соединение с базой данных закрыто.")
