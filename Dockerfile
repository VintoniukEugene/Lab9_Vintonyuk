# Використовуємо офіційний Python образ
FROM python:3.10

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності та встановлюємо їх
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проекту
COPY . .

# Команда за замовчуванням (запуск сервера)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]