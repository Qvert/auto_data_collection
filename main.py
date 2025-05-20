
import streamlit as st
import pandas as pd

from src.data_science.ProcessingData import ProcessingData
from src.parser_cian.ParsingPages import ParsingPages
from src.parser_cian.settings import PAGES_PARSE, URL_PAGE_1, URL_PAGE_2
from src.streamlit.dashboard import slide_bar_filter, show_price_distribution, \
    create_dashboard_streamlit, create_interactive_map
from src.streamlit.load_data import load_data


def init_session_state():
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'raw_data' not in st.session_state:
        st.session_state.raw_data = None
    if 'filter_params' not in st.session_state:
        st.session_state.filter_params = {}


def ensure_data_exists():
    try:
        data = pd.read_csv("src/utils_/hata.csv")
        st.session_state.raw_data = data
        return True
    except FileNotFoundError:
        if st.button("🕷️ Запустить парсинг данных", key="parse_button"):
            with st.status("🔍 Парсинг данных...", expanded=True) as status:
                try:
                    st.write("⏳ Инициализация парсера...")
                    parsing = ParsingPages(url=[URL_PAGE_1, URL_PAGE_2], pages=PAGES_PARSE)

                    st.write("🌐 Сбор данных с сайтов...")
                    parsing.parsing_pages()

                    data = pd.read_csv("src/utils_/hata.csv")
                    st.session_state.raw_data = data
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
            process_data = ProcessingData(st.session_state.raw_data.copy())
            process_data.clean_data()
            process_data.convert_columns()
            process_data.save_to_csv_df()

            # Сохраняем результат в session_state
            st.session_state.data_loaded = True
            st.success("✅ Данные успешно обработаны!")

        except Exception as e:
            st.error(f"❌ Ошибка обработки: {str(e)}")


def show_filters_and_results():
    """Отображение фильтров и результатов"""
    if st.session_state.raw_data is not None:
        # Фильтры всегда отображаются в сайдбаре
        filtered_df = slide_bar_filter(st.session_state.raw_data)

        # Сохраняем параметры фильтрации
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

    # Проверка и загрузка данных
    if not ensure_data_exists():
        st.warning("⚠️ Данные не найдены. Нажмите кнопку для парсинга.")
        st.stop()

    # Основная кнопка обработки
    if not st.session_state.data_loaded:
        if st.button("🔄 Обработать данные", type="primary"):
            process_data()

    # Показываем фильтры и результаты если данные загружены
    if st.session_state.data_loaded:
        show_filters_and_results()

        # Кнопка для повторной обработки
        if st.button("🔄 Обработать заново", type="secondary"):
            st.session_state.data_loaded = False
            st.rerun()




if __name__ == '__main__':
    main()

