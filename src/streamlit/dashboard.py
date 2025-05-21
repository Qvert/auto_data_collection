import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import folium
import requests

from streamlit_folium import st_folium

from src.parser_cian.settings import URL_PAGE_1, URL_PAGE_2, API_KEY, PAGES_PARSE


def create_dashboard_streamlit(filtered_df):
    st.title("🏡 Информационная панель Циан.ру")
    st.write("Анализируйте данные об арендах квартир с помощью интерактивных визуализаций.")
    st.subheader(f"📊 {len(filtered_df)} Найденные объявления")

    selected_rows = st.data_editor(
        filtered_df[["Price", "Address", "Link", "Description", "Square (м²)"]]
        .sort_values(by="Price", ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
        height=400,
        num_rows="dynamic",
        hide_index=True,
        column_config={"Link": st.column_config.LinkColumn()},
        key="table_selection"
    )


def slide_bar_filter(df):
    show_all = st.sidebar.checkbox("Показать все объекты", value=False)
    if show_all:
        filtered_df = df
    else:

        min_price_value = df["Price"].min()
        max_price_value = df["Price"].max()

        min_price, max_price = st.sidebar.slider(
            "Выберите диапазон цен (₽)",
            min_value=int(min_price_value),
            max_value=int(max_price_value),
            value=(int(min_price_value), int(max_price_value)),
            format="₽%d"
        )
        min_square_value = df["Square (м²)"].min()
        max_square_value = df["Square (м²)"].max()
        min_square, max_square = st.sidebar.slider(
            "Выберите диапазон площади (м²)",
            min_value=int(min_square_value),
            max_value=int(max_square_value),
            value=(int(min_square_value), int(max_square_value)),
            format="₽%d"
        )

        filtered_df = df[
            (df["Price"] >= min_price) & (df["Price"] <= max_price)
            ]
        filtered_df = df[
            (df["Square (м²)"] >= min_square) & (df["Square (м²)"] <= max_square)
        ]
    return filtered_df


def show_price_distribution(filtered_df):
    st.subheader("💰 Распределение цен")
    with st.container():
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(filtered_df["Price"], bins=30, kde=True, ax=ax)
        ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'₽{x:.0f}тыс.'))
        ax.set_xlabel("Цена (₽)")
        ax.set_ylabel("Кол-во")
        st.pyplot(fig)


def create_interactive_map(filtered_df):
    st.subheader("📍 Расположение недвижимости")
    m = folium.Map(location=[56.01, 92.86], zoom_start=12)
    for _, row in filtered_df.iterrows():
        popup_info = f"""
        <b>{row['Address']}</b><br>
        Price: ₽{row['Price']:,.0f}<br>
        <a href="{row['Link']}" target="_blank">View Listing</a>
        """
        address = row["Address"]
        base_url = "https://geocode-maps.yandex.ru/1.x"
        params = {
            "geocode": address,
            "apikey": API_KEY,
            "format": "json"
        }
        response = requests.get(base_url, params=params).json()
        pos = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        pos_lat, pos_lon = tuple(map(float, pos.split()))
        icon_color = "red"

        folium.Marker(
            location=[pos_lon, pos_lat],
            popup=popup_info,
            icon=folium.Icon(color=icon_color, icon="home"),
        ).add_to(m)
    st_folium(m, width=800, height=500)
    st.write("Data Source: Redfin Scraper")