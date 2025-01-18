import streamlit as st
import matplotlib.pyplot as plt

# נתוני שנים והוצאות (נתון בסיסי להמחשה)
years = list(range(2015, 2025))
basket_prices = [1000, 1200, 1500, 2000, 2300, 2500, 2700, 3000, 3500, 4000]
max_price = max(basket_prices)

# ממשק Streamlit
st.title("Dynamic Year Visualization")
st.write("Each bubble represents a year. The size of the bubble changes based on the basket price. Add items to the basket to see the impact.")

# הוספת מוצרים
products = {
    "Milk": 5,
    "Bread": 3,
    "Eggs": 10,
    "Rice": 8,
    "Oil": 15
}

selected_products = st.multiselect("Select products to add to your basket:", products.keys())

# חישוב סל קניות
additional_cost = sum([products[product] for product in selected_products])
adjusted_prices = [price + additional_cost for price in basket_prices]

# יצירת Bubble Chart
fig, ax = plt.subplots(figsize=(10, 6))

for i, year in enumerate(years):
    size = (adjusted_prices[i] / max_price) * 2000  # שינוי גודל הבועות
    ax.scatter(year, 1, s=size, alpha=0.6, label=f"{year}: ${adjusted_prices[i]}")
    ax.text(year, 1.1, str(year), fontsize=10, ha='center')

ax.set_xlim(min(years) - 1, max(years) + 1)
ax.set_ylim(0.5, 1.5)
ax.axis("off")
ax.set_title("Bubble Chart of Years Based on Basket Price", fontsize=14)

# הצגת הגרף
st.pyplot(fig)

# הצגת טבלה להמחשה
st.write("Adjusted Basket Prices:")
st.table({"Year": years, "Price": adjusted_prices})
