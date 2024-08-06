# Используем официальный образ Python 3.12.4 в качестве базового образа  
FROM python:3.12.4-slim-bullseye  
  
# Устанавливаем рабочую директорию в контейнере  
WORKDIR /app  
  
# Копируем файл зависимостей в рабочую директорию  
COPY requirements.txt .  
  
# Устанавливаем зависимости  
RUN pip install --no-cache-dir -r requirements.txt  
  
# Копируем исходный код микросервиса в рабочую директорию  
COPY . .  

# Открываем порт
EXPOSE 3005

# Определяем команду для запуска микросервиса  
CMD ["uvicorn", "uvicorn use_sensor_module:app", "--reload", "--port", "3005"]