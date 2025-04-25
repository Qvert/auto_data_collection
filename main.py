from src.streamlit.dashboard import slide_bar_filter, show_price_distribution, \
    create_dashboard_streamlit, create_button_parse, create_interactive_map
from src.streamlit.load_data import load_data


def main():
    create_button_parse()
    load_data_frame = load_data()
    filtered_data_frame = slide_bar_filter(load_data_frame)
    create_dashboard_streamlit(filtered_data_frame)
    show_price_distribution(filtered_data_frame)
    create_interactive_map(filtered_data_frame)

if __name__ == '__main__':
    main()

