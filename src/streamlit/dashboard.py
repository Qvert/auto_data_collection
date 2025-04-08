import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick


def create_dashboard_streamlit(filtered_df):
    st.title("🏡 Информационная панель Циан.ру")
    st.write("Анализируйте данные об арендах квартир с помощью интерактивных визуализаций.")
    st.subheader(f"📊 {len(filtered_df)} Найденные объявления")

    selected_rows = st.data_editor(
        filtered_df[["Price", "Address", "Link", "Description"]]
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

        min_price_value = max(1000, df["Price"].min())
        max_price_value = np.ceil(df["Price"].max() / 100_000) * 100_000

        min_price, max_price = st.sidebar.slider(
            "Выберите диапазон цен (₽)",
            min_value=int(min_price_value),
            max_value=int(max_price_value),
            value=(int(min_price_value), int(max_price_value)),
            format="₽%d"
        )

        filtered_df = df[
            (df["Price"] >= min_price) & (df["Price"] <= max_price)
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