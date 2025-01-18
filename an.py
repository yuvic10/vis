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

# משכורת חודשית ממוצעת לאורך השנים
monthly_income = {2015: 5000, 2016: 5100, 2017: 5200, 2018: 5300, 2019: 5400, 2020: 5500, 2021: 5600, 2022: 5700, 2023: 5800}

# ממשק Streamlit
st.title("Shopping Basket Affordability")
st.write("Select products for your basket and set a maximum percentage of your salary to filter the years.")

# בחירת מוצרים לסל
selected_products = st.multiselect("Select Products for Your Basket", options=list(product_prices.keys()))

# חישוב המחיר הכולל של הסל לאורך השנים
basket_prices = {year: 0 for year in range(2015, 2024)}
for product in selected_products:
    for year, price in product_prices[product].items():
        basket_prices[year] += price

# בחירת אחוז מהמשכורת
max_percentage = st.slider("Set Maximum Percentage of Salary", min_value=1, max_value=50, value=10)

# חישוב אם הסל עומד בתנאי האחוז מהמשכורת
affordable_years = {year: basket_prices[year] / monthly_income[year] * 100 for year in basket_prices}

# סינון שנים לפי התנאי
filtered_years = {str(year): value for year, value in affordable_years.items() if value <= max_percentage}

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
    st.warning("No years match the selected criteria.")

# הצגת טבלה עם מחירי הסל
st.subheader("Basket Prices and Affordability")
st.write("The table below shows the total basket prices and their percentage of income for each year.")
st.table({"Year": list(affordable_years.keys()), "Basket Price": list(basket_prices.values()), "Percentage of Income": list(affordable_years.values())})
