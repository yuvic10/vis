import streamlit as st
import matplotlib.pyplot as plt

# נתונים בסיסיים: מוצרים ומחיריהם לאורך השנים
products = {
    "Milk": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    "Bread": [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5],
    "Eggs": [10, 12, 14, 16, 18, 20, 22, 24, 26, 28],
    "Rice": [8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5],
    "Oil": [15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
}
years = list(range(2015, 2025))

# ממשק Streamlit
st.title("Shopping Basket Visualization Over Time")
st.write("Choose products to add to your basket. The colors of the years will change based on the basket's price.")

# בחירת מוצרים
selected_products = st.multiselect("Select products for your basket:", products.keys())

# חישוב מחיר הסל לכל שנה
basket_prices = [0] * len(years)
for product in selected_products:
    prices = products[product]
    basket_prices = [basket_prices[i] + prices[i] for i in range(len(years))]

# חישוב מקסימום לנורמליזציה של הצבעים
max_price = max(basket_prices)

# יצירת הפאזל
fig, ax = plt.subplots(figsize=(10, 2))

for i, year in enumerate(years):
    # חישוב הצבע על בסיס מחיר הסל
    normalized_value = basket_prices[i] / max_price if max_price > 0 else 0
    color = (1 - normalized_value, normalized_value, 0)  # צבע משתנה מירוק לאדום

    # ציור ריבוע לכל שנה
    rect = plt.Rectangle((i, 0), 1, 1, color=color, ec="black")
    ax.add_patch(rect)

    # הוספת טקסט (שנה ומחיר הסל)
    ax.text(
        i + 0.5,
        0.5,
        f"{year}\n${basket_prices[i]:.2f}",
        ha="center",
        va="center",
        fontsize=10,
        color="white",
    )

# התאמת הצירים
ax.set_xlim(0, len(years))
ax.set_ylim(0, 1)
ax.axis("off")  # הסתרת הצירים

# הצגת הפאזל
st.pyplot(fig)

# הצגת נתונים
st.write("Basket prices per year:")
st.table({"Year": years, "Basket Price": basket_prices})
