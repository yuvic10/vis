import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# נתונים לדוגמה: הוצאות לפי מדינה ושנה
data = {
    "Country": ["Israel", "USA", "Germany", "France", "UK"],
    "Lat": [31.0461, 37.0902, 51.1657, 46.6034, 55.3781],
    "Lon": [34.8516, -95.7129, 10.4515, 1.8883, -3.4360],
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
selected_year = st.selectbox("Select a year", [str(year) for year in range(2015, 2021)])

# מינימום ומקסימום להוצאות באותה שנה
min_expense = df[selected_year].min()
max_expense = df[selected_year].max()

# יצירת מפה עם folium
m = folium.Map(location=[20, 0], zoom_start=2)

# הוספת מעגלים למפה
for _, row in df.iterrows():
    expense = row[selected_year]
    
    # Normalize the value for color scaling
    normalized_value = (expense - min_expense) / (max_expense - min_expense)
    
    # Map normalized value to color
    color = f"#{int(255 * (1 - normalized_value)):02x}{int(255 * normalized_value):02x}00"

    # הוספת מעגל
    folium.CircleMarker(
        location=[row["Lat"], row["Lon"]],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        tooltip=f"{row['Country']}: {expense} USD",
    ).add_to(m)

# הצגת המפה ב-Streamlit
folium_static(m)
