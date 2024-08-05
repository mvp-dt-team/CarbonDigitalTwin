import pyodbc

conn_str = (
    r"DRIVER={Driver do Microsoft Access (*.mdb)};" r"DBQ=D:\Twin14z\db\TWIN14Z_DB.mdb;"
)
cnxn = pyodbc.connect(conn_str)
crsr = cnxn.cursor()

# Получаем список таблиц
for table_info in crsr.tables(tableType="TABLE"):
    print(f"Таблица: {table_info.table_name}")
    crsr_inner = cnxn.cursor()  # Создание нового курсора для запроса столбцов
    try:
        for column_info in crsr_inner.columns(table=table_info.table_name):
            print(
                f"  Столбец: {column_info.column_name}, Тип: {column_info.type_name}, Размер: {column_info.column_size}"
            )
    except Exception as e:
        print(f"Ошибка при получении столбцов для таблицы {table_info.table_name}: {e}")
    crsr_inner.close()

# SQL запрос для выбора всех строк из таблицы 'TwinScrew'
query = """SELECT * FROM TwinScrew
            WHERE YEAR(DT) = 2024
            ORDER BY DT ASC;"""
crsr.execute(query)

# Получаем заголовки столбцов
columns = [desc[0] for desc in crsr.description]

# Определяем максимальную ширину каждого столбца
column_widths = [len(column) for column in columns]
rows = crsr.fetchall()

for row in rows:
    for i, item in enumerate(row):
        item_length = len(str(item))
        if item_length > column_widths[i]:
            column_widths[i] = item_length

# Форматируем заголовки столбцов
formatted_headers = [column.ljust(column_widths[i]) for i, column in enumerate(columns)]
print(" | ".join(formatted_headers))

# Выводим данные
for row in rows:
    formatted_row = [str(item).ljust(column_widths[i]) for i, item in enumerate(row)]
    print(" | ".join(formatted_row))

# Закрываем курсор и соединение
crsr.close()
cnxn.close()
