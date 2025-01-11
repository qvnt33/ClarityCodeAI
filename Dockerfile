# Використання базового образу Python
FROM python:3.13-slim

# Створення робочої директорії
WORKDIR /app

# Копіювання залежності
COPY requirements.txt .

# Встановлення залежностей
RUN pip install --no-cache-dir -r requirements.txt

# Копіювання всього коду проєкта в робочу директорію контейнера
COPY . .

# Вимикання буферизації для зручності читання логів
ENV PYTHONUNBUFFERED=1

# Відкриття порту
EXPOSE 8000

# Запуск сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]