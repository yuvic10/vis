import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני בסיס
products = {
    "Milk": [5, 5.5, 6, 6.5, 7, 7.5],
    "Bread": [10, 10.5, 11, 11.5, 12, 12.5],
    "Eggs": [15, 15.5, 16, 16.5, 17, 17.5],
    "Rice": [8, 8.5, 9, 9.5, 10, 10.5]
}
years = [2015, 2016, 2017, 2018, 2019, 2020]
minimum_wage = [5000, 5200, 5400, 5500, 5700, 6000]

# יצירת DataFrame
df_products = pd.DataFrame(products, index=years)
df_products["Total Basket"] = df_products.sum(axis=1)
df_products["Minimum Wage"] = minimum_wage
df_products["Percentage of Wage"] = (df_products["Total Basket"] / df_products["Minimum Wage"]) * 100

# ממשק משתמש לבחירת מוצרים
st.sidebar.header("Choose Products for the Basket")
selected_products = st.sidebar.multiselect(
    "Select Products:", options=df_products.columns[:-3], default=df_products.columns[:-3]
)

df_selected = df_products[selected_products]
df_selected["Total Basket"] = df_selected.sum(axis=1)
df_selected["Percentage of Wage"] = (df_selected["Total Basket"] / df_products["Minimum Wage"]) * 100

# כותרת
st.title("Shopping Basket Over the Years")

# גרף קווי להצגת מחיר סל הקניות לאורך השנים
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(years, df_selected["Total Basket"], label="Total Basket Price", color="blue", marker="o")
ax.plot(years, df_products["Minimum Wage"], label="Minimum Wage", color="green", linestyle="--")

# כותרות וצירים
ax.set_title("Basket Price vs Minimum Wage", fontsize=20)
ax.set_xlabel("Year", fontsize=16)
ax.set_ylabel("Price (NIS)", fontsize=16)
ax.legend(fontsize=14)

# הצגת הגרף
st.pyplot(fig)

# אינדיקטור של אחוז מהשכר
st.subheader("Basket as Percentage of Minimum Wage")
st.line_chart(df_selected["Percentage of Wage"])

# הצגת טבלה
st.subheader("Data Table")
st.dataframe(df_selected)
