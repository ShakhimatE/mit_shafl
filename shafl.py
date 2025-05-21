import streamlit as st
import random
import pandas as pd
import os
import json
from datetime import date

# Функция для отображения таблицы участников
def render_table(player_list, table_number):
    # Обрезаем слишком длинные имена
    max_length = 20
    shortened_players = [
        name if len(name) <= max_length else name[:max_length - 1] + "…" for name in player_list
    ]

    df = pd.DataFrame({"№": range(1, len(player_list) + 1), "Игроки": shortened_players})
    st.markdown(f"### Стол {table_number}")
    
    # Используем Streamlit native таблицу с обрезкой по ширине
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Игроки": st.column_config.TextColumn("Игроки", width="medium")
        }
    )



# Функция для генерации и отображения страницы с генерацией турнира
def generate_tournament_page():
    st.title("Формирование рассадки")

    # Поля для ввода данных турнира
    tournament_name = st.text_input("Название турнира")
    tournament_date = st.date_input("Дата турнира", value=date.today())
    input_text = st.text_area(
        "Введите список участников (в формате: '1. Имя 🎉')",
        height=180,
    )
    num_games = st.number_input("Количество игр", min_value=1, max_value=20, value=5, step=1)

    if st.button("Сгенерировать столы"):
        # Обрабатываем входной список участников
        input_list = [line.split('. ', 1)[1] for line in input_text.split('\n') if line]
        if not input_list:
            st.warning("Список участников пуст. Проверьте ввод.")
            return

        # Генерация столов
        random_lists = []
        history = {name: list() for name in input_list}  # Храним историю мест для каждого игрока

        # random_lists = []
        # history = {name: set() for name in input_list}  # Запоминаем позиции игроков

        for game in range(num_games):
                shuffled_list = input_list[:]
                new_table = []
                for i in range(len(input_list)):
                    # Исключаем игроков, которые сидели на этой позиции в последних `history_limit` играх
                    # Защищаемся от повторного попадания на ту же позицию в прошлой игре
                    last_game = random_lists[-1] if random_lists else []
                    candidates = [player for player in shuffled_list if not (last_game and last_game[i] == player)]


                    if not candidates:
                        # Если нет кандидатов, сбрасываем историю и выбираем снова
                        for player in input_list:
                            if len(history[player]) >= 6:
                                history[player].pop(0)  # Удаляем старые записи
                        candidates = shuffled_list

                    selected = random.choice(candidates)
                    new_table.append(selected)
                    shuffled_list.remove(selected)
                    history[selected].append(i)  # Запоминаем место игрока за столом

                    # Ограничиваем размер истории
                    if len(history[selected]) > 6:
                        history[selected].pop(0)

                random_lists.append(new_table)


        # Вывод сгенерированных столов
        st.subheader(f"Турнир: {tournament_name} ({tournament_date})")
        tables_per_row = 5
        for i in range(0, len(random_lists), tables_per_row):
            cols = st.columns(tables_per_row)
            for col, table_index in zip(cols, range(i, i + tables_per_row)):
                if table_index < len(random_lists):
                    with col:
                        render_table(random_lists[table_index], table_index + 1)

        # Сохранение данных турнира
        tournament_data = {
            "name": tournament_name,
            "date": str(tournament_date),
            "tables": random_lists,
        }

        tournament_filename = f"{tournament_name}_{tournament_date}.json".replace(" ", "_").replace(":", "-")
        if not os.path.exists("tournaments"):
            os.makedirs("tournaments")
        file_path = os.path.join("tournaments", tournament_filename)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(tournament_data, f, ensure_ascii=False, indent=4)

        st.success(f"Рассадка успешно сохранена: {file_path}")


# Функция для отображения страницы просмотра сохранённых турниров
def view_tournaments_page():
    st.title("Просмотр сохранённых турниров")

    if not os.path.exists("tournaments"):
        st.warning("Пока нет сохранённых турниров. Перейдите на страницу генерации, чтобы создать турнир.")
        return

    tournament_files = [f for f in os.listdir("tournaments") if f.endswith(".json")]
    if not tournament_files:
        st.warning("Пока нет сохранённых турниров. Перейдите на страницу генерации, чтобы создать турнир.")
        return

    selected_file = st.selectbox("Выберите турнир для просмотра", tournament_files)

    if selected_file:
        file_path = os.path.join("tournaments", selected_file)
        with open(file_path, "r", encoding="utf-8") as f:
            tournament_data = json.load(f)

        st.subheader(f"Турнир: {tournament_data['name']}")
        st.write(f"Дата: {tournament_data['date']}")

        # Получаем таблицы из данных турнира
        random_lists = tournament_data["tables"]

        # Вывод сгенерированных столов по три на строку
        
        tables_per_row = 5
        for i in range(0, len(random_lists), tables_per_row):
            cols = st.columns(tables_per_row)
            for col, table_index in zip(cols, range(i, i + tables_per_row)):
                if table_index < len(random_lists):
                    with col:
                        render_table(random_lists[table_index], table_index + 1)



# Путь к логотипу
logo_path = r'C:\Users\elya\mit\shafl\МИТ_лого.png' # Замените на путь к вашему файлу логотипа

def main():
    # Отображаем логотип в заголовке
    st.sidebar.image(logo_path, use_column_width=True)  # Логотип в боковой панели
    st.title("Турнирная рассадка")  # Заголовок приложения
    
    st.sidebar.title("Меню")
    page = st.sidebar.radio("Выберите страницу", ["Генерация столов", "Просмотр турниров"])

    if page == "Генерация столов":
        generate_tournament_page()
    elif page == "Просмотр турниров":
        view_tournaments_page()

if __name__ == "__main__":
    if not os.path.exists(r"C:\Users\elya\mit\shafl\МИТ_лого.png"):
        st.error("Логотип не найден. Убедитесь, что файл 'logo' находится в директории проекта.")
    else:
        main()

