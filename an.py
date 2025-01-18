import streamlit as st
import pydeck as pdk
import pandas as pd
import random

# נתוני דוגמה
data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Latitude": [random.uniform(-90, 90) for _ in range(9)],
    "Longitude": [random.uniform(-180, 180) for _ in range(9)],
    "Category": ["Fuel", "Rent", "Food"] * 3,
    "Actual Price": [random.uniform(100, 500) for _ in range(9)],
    "Simulated Price": [random.uniform(80, 400) for _ in range(9)],
}

# יצירת DataFrame
df = pd.DataFrame(data)

# הגדרות תצוגה ב-Streamlit
st.title("גלובוס מחירים אינטראקטיבי")
st.sidebar.header("הגדרות")
selected_year = st.sidebar.selectbox("בחר שנה", options=df["Year"].unique())
selected_category = st.sidebar.multiselect(
    "בחר קטגוריות", options=df["Category"].unique(), default=df["Category"].unique()
)

# סינון הנתונים לפי השנה והקטגוריה שנבחרו
filtered_data = df[
    (df["Year"] == selected_year) & (df["Category"].isin(selected_category))
]

# הגדרות ל-Mapbox
st.write(f"מציג נתונים עבור השנה: {selected_year}")

# יצירת PyDeck Map
layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_data,
    get_position=["Longitude", "Latitude"],
    get_radius="Actual Price",  # רדיוס כגודל המחיר האמיתי
    get_fill_color=[255, 0, 0, 140],  # צבע אדום למחיר האמיתי
    pickable=True,
)

view_state = pdk.ViewState(latitude=0, longitude=0, zoom=1, pitch=50)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{Category}\nActual Price: {Actual Price}"},
)

st.pydeck_chart(r)

# הצגת נתונים
st.write("נתונים נבחרים:")
st.dataframe(filtered_data)
