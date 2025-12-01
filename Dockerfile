FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Создаем папку data, если нужно
RUN mkdir -p /app/data

CMD ["python", "main.py"]
