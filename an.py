import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני דוגמה (החלף בנתונים שלך)
data = {
    "product": ["Flour", "Pasta", "Rice", "Chicken", "Oil"],
    "2018": [4.0, 5.3, 9.5, 33.3, 10.7],
    "2019": [4.2, 5.4, 9.7, 34.0, 11.0],
    "2020": [4.4, 5.5, 10.0, 35.0, 11.5],
    "2021": [4.5, 5.6, 10.3, 36.0, 12.0],
    "2022": [4.6, 5.8, 10.5, 37.0, 12.5],
    "2023": [4.8, 6.0, 10.7, 38.0, 13.0],
}

df = pd.DataFrame(data)

# פונקציה לחשב את הסל
def calculate_basket(selected_products):
    selected_data = df[df["product"].isin(selected_products)].iloc[:, 1:]
    yearly_totals = selected_data.sum().to_dict()
    return yearly_totals

# כותרת האפליקציה
st.title("Build Your Basket Over the Years")

# בחירת מוצרים
selected_products = st.multiselect(
    "Select products to add to your basket:",
    options=df["product"].tolist(),
    default=[]
)

# חישוב מחירי הסל
if selected_products:
    basket_prices = calculate_basket(selected_products)

    # יצירת גרף
    st.subheader("Basket Prices Over the Years")
    fig, ax = plt.subplots()
    years = list(basket_prices.keys())
    prices = list(basket_prices.values())

    ax.plot(years, prices, marker="o", label="Basket Price")
    ax.set_title("Basket Price Evolution")
    ax.set_xlabel("Year")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)

    # הצגת טבלה
    st.subheader("Basket Details")
    st.write(pd.DataFrame({"Year": years, "Basket Price": prices}))
else:
    st.write("Please select products to see the basket price over the years.")
