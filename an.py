import streamlit as st
import folium
from streamlit_folium import folium_static

# רשימת שנים ומספר מוצרים שנוספו בכל שנה
years = list(range(2015, 2025))
products_per_year = [0] * len(years)  # התחל עם 0 מוצרים לכל שנה

# ממשק Streamlit
st.title("Map with Changing Colors Over Years")
st.write("Add products for each year and see the color intensity change on the map.")

# מחוון לבחירת שנה
selected_year_index = st.slider("Select a year", 0, len(years) - 1, 0)
selected_year = years[selected_year_index]

# הוספת מוצרים לשנה הנוכחית
products_to_add = st.number_input(
    f"Add products for {selected_year}", min_value=0, value=0, step=1
)
products_per_year[selected_year_index] += products_to_add

# צביעת המפה בהתאם למספר המוצרים
max_products = max(products_per_year)
min_products = min(products_per_year)

# יצירת מפה עם Folium
m = folium.Map(location=[31.0461, 34.8516], zoom_start=6)  # מרכז את המפה לישראל

# מחזור דרך השנים ליצירת מעגלים
for i, year in enumerate(years):
    normalized_value = (
        (products_per_year[i] - min_products) / (max_products - min_products)
        if max_products > 0
        else 0
    )
    color = f"#{int(255 * (1 - normalized_value)):02x}{int(255 * normalized_value):02x}00"

    folium.CircleMarker(
        location=[31.0461, 34.8516],  # ישראל
        radius=15,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        tooltip=f"Year: {year}, Products: {products_per_year[i]}",
    ).add_to(m)

# הצגת המפה
folium_static(m)

# הצגת נתוני המוצרים
st.write("Products added per year:")
st.table({"Year": years, "Products": products_per_year})
