import mysql.connector
import sqlite3
from config import config

def download_all_tables_from_mysql(host, user, password, database):
    # Подключение к MySQL серверу
    mysql_conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Создание курсора для выполнения SQL запросов
    mysql_cursor = mysql_conn.cursor()

    # Получение списка всех таблиц в базе данных MySQL
    mysql_cursor.execute("SHOW TABLES")
    tables = [table[0] for table in mysql_cursor.fetchall()]

    # Создание словаря для хранения данных всех таблиц
    all_tables_data = {}

    # Загрузка данных из всех таблиц
    for table in tables:
        mysql_cursor.execute(f"SELECT * FROM {table}")
        columns = [column[0] for column in mysql_cursor.description]
        rows = mysql_cursor.fetchall()
        all_tables_data[table] = (columns, rows)

    # Закрытие курсора и соединения с MySQL сервером
    mysql_cursor.close()
    mysql_conn.close()

    return all_tables_data

def save_all_tables_to_sqlite(all_tables_data, sqlite_file):
    # Подключение к базе данных SQLite
    sqlite_conn = sqlite3.connect(sqlite_file)

    # Сохранение данных всех таблиц в SQLite
    for table, (columns, rows) in all_tables_data.items():
        sqlite_cursor = sqlite_conn.cursor()

        # Создание таблицы в базе данных SQLite с такой же структурой как и в MySQL
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"
        sqlite_cursor.execute(create_table_query)

        # Вставка данных в таблицу SQLite
        for row in rows:
            placeholders = ', '.join(['?' for _ in range(len(row))])
            insert_query = f"INSERT INTO {table} VALUES ({placeholders})"
            sqlite_cursor.execute(insert_query, row)

        # Сохранение изменений в базе данных SQLite
        sqlite_conn.commit()

    # Закрытие соединения с базой данных SQLite
    sqlite_conn.close()

if __name__ == "__main__":
    # Параметры подключения к MySQL серверу
    mysql_host = config.url
    mysql_user = config.login.get_secret_value()
    mysql_password = config.password.get_secret_value()
    mysql_database = config.db_name

    # Параметры для сохранения в SQLite базу данных
    sqlite_file = 'data.db'

    # Загрузка данных из всех таблиц MySQL и сохранение их в SQLite
    all_tables_data = download_all_tables_from_mysql(mysql_host, mysql_user, mysql_password, mysql_database)
    save_all_tables_to_sqlite(all_tables_data, sqlite_file)
