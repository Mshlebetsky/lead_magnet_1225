# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY bot/ ./bot
COPY data/ ./data

# Создаем папку data, если ее нет
RUN mkdir -p /app/data

# Указываем команду запуска
CMD ["python", "bot/main.py"]
