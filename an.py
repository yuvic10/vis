import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# נתונים לדוגמה
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
base_prices = {
    "Flour": [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8],
    "Rice": [8.0, 8.1, 8.3, 8.5, 8.6, 8.8, 9.0, 9.2, 9.3],
    "Milk": [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8],
    "Chicken": [15.0, 15.2, 15.5, 15.8, 16.0, 16.3, 16.6, 16.8, 17.0]
}

# יצירת DataFrame לנתונים
data = []
for product, prices in base_prices.items():
    for year, price in zip(years, prices):
        data.append({"Product": product, "Year": year, "Price": price})

df = pd.DataFrame(data)

# כותרת ראשית
st.title("Boxplot: טווח מחירים והשפעת הוספת מוצרים")

# בחירת מוצרים לסל
selected_products = st.multiselect("בחר מוצרים להוסיף לסל", list(base_prices.keys()), default=list(base_prices.keys()))

# סינון נתונים לפי בחירת המשתמש
filtered_df = df[df["Product"].isin(selected_products)]

if filtered_df.empty:
    st.error("בחר לפחות מוצר אחד כדי להציג את הנתונים!")
else:
    # יצירת Boxplot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x="Year", y="Price", data=filtered_df, ax=ax, palette="Set2")
    
    # פרטי גרף
    ax.set_title("השפעת הוספת מוצרים על טווח המחירים לאורך השנים", fontsize=16)
    ax.set_xlabel("שנים", fontsize=14)
    ax.set_ylabel("מחיר", fontsize=14)

    st.pyplot(fig)
