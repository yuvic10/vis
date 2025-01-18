import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# נתונים לדוגמה: מחירי מוצרים לאורך השנים
product_prices = {
    "Flour": {2015: 10, 2016: 12, 2017: 14, 2018: 15, 2019: 16, 2020: 18, 2021: 20, 2022: 22, 2023: 25},
    "Milk": {2015: 20, 2016: 22, 2017: 24, 2018: 26, 2019: 28, 2020: 30, 2021: 32, 2022: 35, 2023: 38},
    "Eggs": {2015: 15, 2016: 16, 2017: 18, 2018: 19, 2019: 20, 2020: 22, 2021: 24, 2022: 26, 2023: 28},
    "Chicken": {2015: 50, 2016: 55, 2017: 60, 2018: 65, 2019: 70, 2020: 75, 2021: 80, 2022: 85, 2023: 90},
    "Rice": {2015: 30, 2016: 32, 2017: 35, 2018: 37, 2019: 40, 2020: 42, 2021: 45, 2022: 48, 2023: 50},
}

# ממשק Streamlit
st.title("Shopping Basket Affordability by Year")
st.write("Select products for your basket and set a maximum price to filter the years.")

# בחירת מוצרים לסל
selected_products = st.multiselect("Select Products for Your Basket", options=list(product_prices.keys()))

# חישוב המחיר הכולל של הסל לאורך השנים
basket_prices = {year: 0 for year in range(2015, 2024)}
for product in selected_products:
    for year, price in product_prices[product].items():
        basket_prices[year] += price

# בחירת תקרת מחיר
max_price = st.slider("Set Maximum Basket Price", min_value=10, max_value=200, value=50)

# סינון שנים לפי תקרת המחיר
filtered_years = {str(year): price for year, price in basket_prices.items() if price <= max_price}

# בדיקה אם יש שנים להצגה
if filtered_years:
    # יצירת ענן מילים
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white'
    ).generate_from_frequencies(filtered_years)

    # הצגת ענן המילים
    st.subheader("Years Where the Basket is Affordable")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.warning("No years match the selected basket and price criteria.")

# הצגת טבלה עם מחירי הסל
st.subheader("Basket Prices by Year")
st.write("The table below shows the total basket prices for each year.")
st.table({"Year": list(basket_prices.keys()), "Basket Price": list(basket_prices.values())})
