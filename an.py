import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# נתונים לדוגמה
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
base_prices = np.array([1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600], dtype=float)
products = {
    "Flour": [1.0, 1.1, 1.2, 1.1, 1.3, 1.4, 1.5, 1.6, 1.7],
    "Rice": [2.0, 2.2, 2.4, 2.3, 2.5, 2.7, 2.8, 2.9, 3.0],
    "Milk": [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6],
    "Chicken": [5.0, 5.5, 6.0, 6.2, 6.5, 6.8, 7.0, 7.2, 7.5],
}

# כותרת ראשית
st.title("חלופה 1: שינוי פרופורציות הסל לאורך השנים")

# בחירת מוצרים לסל
selected_products = st.multiselect("בחר מוצרים להוסיף לסל", list(products.keys()), default=["Flour"])

# בדיקה אם נבחרו מוצרים
if not selected_products:
    st.error("בחר מוצר אחד לפחות כדי לראות את ההשפעה על הסל!")
else:
    # חישוב מחיר סל
    total_prices = base_prices.copy()
    for product in selected_products:
        total_prices += np.array(products[product], dtype=float)

    # התאמת פרופורציות השנים
    max_price = max(total_prices)
    sizes = (total_prices / max_price) * 5000  # התאמת גודל
    proportions = (total_prices / sum(total_prices)) * 100  # פרופורציה באחוזים

    # יצירת גרף
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = plt.cm.viridis(total_prices / max_price)  # צבעים משתנים לפי מחירים
    for i, year in enumerate(years):
        ax.scatter(year, 0, s=sizes[i], color=colors[i], alpha=0.8, label=f"{year}: {proportions[i]:.1f}% מהסל")

    # פרטי גרף
    ax.set_title("השפעת הוספת מוצרים על פרופורציות השנים בסל", fontsize=16)
    ax.set_xlabel("שנים", fontsize=14)
    ax.set_yticks([])  # אין צורך בציר Y
    ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1), title="שנה ואחוז מהסל")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    st.pyplot(fig)
