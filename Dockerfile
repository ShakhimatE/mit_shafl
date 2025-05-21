# Используем официальный Python образ
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файлы проекта внутрь контейнера
COPY . /app

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт, который будет слушать Streamlit
EXPOSE 8501

# Команда запуска Streamlit приложения
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
