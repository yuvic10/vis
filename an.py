import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# נתונים לדוגמה: הוצאות לפי מדינה ושנה
data = {
    "Country": ["Israel", "USA", "Germany", "France", "UK"],
    "2015": [5000, 10000, 12000, 11000, 11500],
    "2016": [5200, 10500, 12300, 11300, 11700],
    "2017": [5500, 11000, 12600, 11500, 12000],
    "2018": [5800, 11500, 13000, 11800, 12200],
    "2019": [6000, 12000, 13500, 12200, 12500],
    "2020": [6200, 12500, 14000, 12500, 12800],
}

# המרת הנתונים ל-DataFrame
df = pd.DataFrame(data)

# יצירת תפריט בחירה לשנה
st.title("Dynamic Expense Map")
selected_year = st.selectbox("Select a year", ["2015", "2016", "2017", "2018", "2019", "2020"])

# הגדרת ערכים לצביעה (Normalize)
def normalize(values, min_val, max_val):
    return [(value - min_val) / (max_val - min_val) for value in values]

# יצירת מפה עם folium
m = folium.Map(location=[20, 0], zoom_start=2)

# מינימום ומקסימום להוצאות באותה שנה
min_expense = df[selected_year].min()
max_expense = df[selected_year].max()

# הוספת שכבות למפה
for _, row in df.iterrows():
    country = row["Country"]
    expense = row[selected_year]
    normalized_value = normalize([expense], min_expense, max_expense)[0]

    # צבע המבוסס על הערך המנורמל
    color = folium.colors.LinearColormap(["green", "yellow", "red"], vmin=0, vmax=1)(normalized_value)

    # הוספת מעגל למפה
    folium.CircleMarker(
        location=[
            31.0461 if country == "Israel" else 0,  # קו רוחב לדוגמה
            34.8516 if country == "Israel" else 0,  # קו אורך לדוגמה
        ],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        tooltip=f"{country}: {expense} USD",
    ).add_to(m)

# הצגת המפה ב-Streamlit
folium_static(m)
