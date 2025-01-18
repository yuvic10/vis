import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני דוגמה
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]

products = {
    "Flour": [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
    "Milk": [5.0, 5.8, 6.6, 7.5, 8.5, 9.5, 10.5],
    "Eggs": [10.0, 11.5, 13.0, 14.5, 16.0, 17.5, 19.0],
    "Cheese": [15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0],
}

# ממשק Streamlit
st.title("Shopping Basket Trends Over the Years")
st.write("Select products to see their cumulative price trends over the years.")

# בחירת מוצרים
selected_products = st.multiselect(
    "Select products to add to the basket:",
    options=list(products.keys()),
    default=[]
)

# חישוב עלויות סל הקניות
if selected_products:
    basket_prices = [sum([products[prod][i] for prod in selected_products]) for i in range(len(years))]

    # יצירת DataFrame
    data = pd.DataFrame({
        "Year": years,
        "Basket Price": basket_prices
    })

    # גרף מגמה
    st.subheader("Trend: Basket Price Over the Years")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data["Year"], data["Basket Price"], marker="o", label="Basket Price", color="blue")
    ax.set_title("Basket Price Trends Over the Years")
    ax.set_ylabel("Price (₪)")
    ax.set_xlabel("Year")
    ax.legend()
    st.pyplot(fig)

    # הצגת טבלה
    st.subheader("Basket Price Details")
    st.table(data)
else:
    st.warning("Please select at least one product to see the results.")
