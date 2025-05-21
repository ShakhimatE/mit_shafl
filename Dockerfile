# Используем официальный Python образ
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /mit_shafl

# Копируем файлы проекта внутрь контейнера
COPY . /mit_shafl

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт, который будет слушать Streamlit
EXPOSE 8501

# Команда запуска Streamlit приложения
CMD ["streamlit", "run", "shafl.py", "--server.port=8501", "--server.address=0.0.0.0"]
