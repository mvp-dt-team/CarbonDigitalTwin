import pytest
import aiomysql
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.orm import Base, MeasurementModel, PredictionModel
from yaml import load
from yaml.loader import SafeLoader
from sqlalchemy.future import select
from sqlalchemy import update, delete

with open("config.yaml", "r") as config_file:
    config = load(config_file, Loader=SafeLoader)
                  
DATABASE_URL = f"mysql+aiomysql://{config['USER']}:{config['PASSWORD']}@{config['HOST']}:3306/{config['DB']}"
# Создание асинхронного движка и фабрики сессий
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# @pytest.fixture(scope="function")
# async def async_db_session():
#     # async with engine.begin() as conn:
#     #     # Удаляем все таблицы
#     #     # await conn.run_sync(Base.metadata.drop_all)
#     #     print("Я тут!")
#     #     # Создаем таблицы
#     #     await conn.run_sync(Base.metadata.create_all)
#     #     # Наполняем таблицы тестовыми данными
#     #     await initialize_data(AsyncSessionLocal())
#     # return AsyncSessionLocal()

#     async with AsyncSessionLocal() as session:
#         # await session.execute(delete(MeasurementModel))
#         # await session.execute(delete(PredictionModel))
#         # await session.commit()
#         yield session
#         # await session.close()

#     # await engine.dispose()

# async def initialize_data(session):
#     # Здесь ваш алгоритм для добавления тестовых данных в базу
#     pass
#     # new_user = User(id=1, name="John Doe")
#     # session.add(new_user)
#     # await session.commit()

# def pytest_html_results_table_header(cells):
#     cells.insert(2, "<th>Description</th>")
#     cells.insert(1, '<th class="sortable time" data-column-type="time">Time</th>')


# def pytest_html_results_table_row(report, cells):
#     cells.insert(2, f"<td>{report.description}</td>")
#     cells.insert(1, f'<td class="col-time">{datetime.utcnow()}</td>')


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     report.description = str(item.function.__doc__)
