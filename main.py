import threading
from datetime import time, datetime
import streamlit as st
import pandas as pd
import time as sleep_time

from src.data_science.ProcessingData import ProcessingData
from src.parser_cian.ParsingPages import ParsingPages
from src.parser_cian.settings import PAGES_PARSE, URL_PAGE_1, URL_PAGE_2, DATA_PATH
from src.streamlit.dashboard import slide_bar_filter, show_price_distribution, \
    create_dashboard_streamlit, create_interactive_map


def init_session_state():
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'raw_data' not in st.session_state:
        st.session_state.raw_data = None
    if 'filter_params' not in st.session_state:
        st.session_state.filter_params = {}
    if 'auto_parse' not in st.session_state:
        st.session_state.auto_parse = False
    if 'parse_time' not in st.session_state:
        st.session_state.parse_time = time(0, 0)
    if 'last_parse' not in st.session_state:
        st.session_state.last_parse = "Никогда"


def run_parsing():
    """Функция для выполнения парсинга в фоновом режиме"""
    try:
        parsing = ParsingPages(base_urls=[URL_PAGE_1, URL_PAGE_2], max_pages=PAGES_PARSE)
        parsing.parse_all_pages()
        data = pd.read_csv(DATA_PATH)
        st.session_state.raw_data = data
        st.session_state.last_parse = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.toast("✅ Парсинг завершен!", icon="✅")
    except Exception as e:
        st.error(f"❌ Ошибка при автоматическом парсинге: {str(e)}")


def auto_parse_loop():
    """Фоновая задача для автоматического парсинга"""
    while st.session_state.auto_parse:
        now = datetime.now().time()
        if now.hour == st.session_state.parse_time.hour and now.minute == st.session_state.parse_time.minute:
            run_parsing()
            # Ждем 1 минуту чтобы избежать повторного срабатывания
            sleep_time.sleep(60)
        sleep_time.sleep(30)  # Проверяем каждые 30 секунд


def setup_auto_parse():
    """Настройка автоматического парсинга"""
    st.sidebar.subheader("Автоматический сбор данных")
    auto_parse = st.sidebar.checkbox(
        "Включить автоматический парсинг",
        value=st.session_state.auto_parse,
        key="auto_parse_checkbox"
    )

    parse_time = st.sidebar.time_input(
        "Время ежедневного парсинга",
        value=st.session_state.parse_time,
        key="parse_time_input"
    )

    if st.sidebar.button("Применить настройки"):
        st.session_state.auto_parse = auto_parse
        st.session_state.parse_time = parse_time

        if auto_parse:
            # Запускаем фоновый поток
            thread = threading.Thread(target=auto_parse_loop, daemon=True)
            thread.start()
            st.sidebar.success(f"✅ Автопарсинг включен на {parse_time.strftime('%H:%M')}")
        else:
            st.sidebar.warning("⚠️ Автопарсинг отключен")

    st.sidebar.markdown(f"**Последний парсинг:** {st.session_state.last_parse}")


def ensure_data_exists():
    try:
        data = pd.read_csv(DATA_PATH)
        st.session_state.raw_data = data
        return True
    except FileNotFoundError:
        if st.button("🕷️ Запустить парсинг данных", key="parse_button"):
            with st.status("🔍 Парсинг данных...", expanded=True) as status:
                try:
                    run_parsing()
                    status.update(label="✅ Парсинг завершен!", state="complete", expanded=False)
                    return True
                except Exception as e:
                    st.error(f"❌ Ошибка парсинга: {str(e)}")
                    return False
        return False


def process_data():
    """Обработка данных с сохранением состояния"""
    with st.spinner("Обработка данных..."):
        try:
            process_data_df = ProcessingData(st.session_state.raw_data.copy())
            process_data_df.clean_data()
            process_data_df.convert_columns()
            process_data_df.save_to_csv_df()

            # Сохраняем результат в session_state
            st.session_state.data_loaded = True
            st.success("✅ Данные успешно обработаны!")

        except Exception as e:
            st.error(f"❌ Ошибка обработки: {str(e)}")


def show_filters_and_results():
    if st.session_state.raw_data is not None:
        filtered_df = slide_bar_filter(st.session_state.raw_data)
        st.session_state.filter_params = {
            'filtered_df': filtered_df,
            'last_update': pd.Timestamp.now()
        }

        # Основное содержимое
        tab1, tab2, tab3 = st.tabs(["Дашборд", "Распределение цен", "Карта"])

        with tab1:
            create_dashboard_streamlit(filtered_df)

        with tab2:
            show_price_distribution(filtered_df)

        with tab3:
            create_interactive_map(filtered_df)


def main():
    st.set_page_config(layout="wide", page_icon="🏠")

    init_session_state()
    setup_auto_parse()

    # Проверка и загрузка данных
    if not ensure_data_exists():
        st.warning("⚠️ Данные не найдены. Нажмите кнопку для парсинга.")
        st.stop()

    # Основная кнопка обработки
    if not st.session_state.data_loaded:
        if st.button("🔄 Обработать данные", type="primary"):
            process_data()

    if st.session_state.data_loaded:
        show_filters_and_results()

        # Кнопка для повторной обработки
        if st.button("🔄 Обработать заново", type="secondary"):
            st.session_state.data_loaded = False
            st.rerun()


if __name__ == '__main__':
    main()

