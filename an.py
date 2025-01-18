import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# נתונים לדוגמה: מחירי מוצרים לאורך השנים
product_prices = {
    "Flour": {2015: 2, 2016: 2.2, 2017: 2.5, 2018: 2.7, 2019: 3, 2020: 3.5, 2021: 3.7, 2022: 4, 2023: 4.5},
    "Milk": {2015: 3, 2016: 3.2, 2017: 3.5, 2018: 3.7, 2019: 4, 2020: 4.5, 2021: 4.7, 2022: 5, 2023: 5.5},
    "Eggs": {2015: 5, 2016: 5.2, 2017: 5.5, 2018: 5.7, 2019: 6, 2020: 6.5, 2021: 6.7, 2022: 7, 2023: 7.5},
    "Chicken": {2015: 10, 2016: 10.5, 2017: 11, 2018: 11.5, 2019: 12, 2020: 12.5, 2021: 13, 2022: 13.5, 2023: 14},
    "Rice": {2015: 8, 2016: 8.2, 2017: 8.5, 2018: 8.7, 2019: 9, 2020: 9.5, 2021: 9.7, 2022: 10, 2023: 10.5},
}

# משכורת חודשית ממוצעת לאורך השנים
monthly_income = {2015: 5000, 2016: 5100, 2017: 5200, 2018: 5300, 2019: 5400, 2020: 5500, 2021: 5600, 2022: 5700, 2023: 5800}

# ממשק Streamlit
st.title("Interactive Word Cloud: Shopping Basket and Years")
st.write("Build your shopping basket and see how the years scale based on the basket's percentage of income.")

# בחירת מוצרים לסל
selected_products = st.multiselect("Select Products for Your Basket", options=list(product_prices.keys()))

# חישוב המחיר הכולל של הסל לאורך השנים
basket_prices = {year: 0 for year in range(2015, 2024)}
for product in selected_products:
    for year, price in product_prices[product].items():
        basket_prices[year] += price

# חישוב אחוז הסל מהמשכורת לכל שנה
basket_percentages = {year: (basket_prices[year] * 4 / monthly_income[year]) * 100 for year in basket_prices}  # 4 פעמים בחודש

# בחירת סף אחוזים
threshold = st.slider("Select Threshold Percentage", min_value=0, max_value=50, value=10)

# סינון שנים לפי סף
filtered_years = {str(year): percent for year, percent in basket_percentages.items() if percent >= threshold}

# הצגת השנים בענן מילים
if filtered_years:
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white'
    ).generate_from_frequencies(filtered_years)

    st.subheader("Filtered Word Cloud")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.warning("No years match the selected threshold.")

# הצגת טבלה עם המחירים והאחוזים
st.subheader("Yearly Basket Prices and Percentages")
table_data = {"Year": list(basket_prices.keys()), "Basket Price": list(basket_prices.values()), "Percentage of Income": list(basket_percentages.values())}
st.table(table_data)
