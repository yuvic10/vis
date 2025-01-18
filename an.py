import streamlit as st
import matplotlib.pyplot as plt

# נתונים לדוגמה
years = list(range(2015, 2024))
base_prices = [100, 120, 140, 150, 170, 200, 230, 250, 270]
products = {
    "Flour": 5,
    "Rice": 8,
    "Chicken": 20,
    "Oil": 10,
    "Milk": 6,
    "Bread": 4,
    "Eggs": 10,
    "Tomatoes": 7,
}

# פונקציה לחשב את המחירים
def calculate_prices(selected_products):
    total_prices = []
    for i, base_price in enumerate(base_prices):
        total_price = base_price + sum([products[prod] for prod in selected_products])
        total_prices.append(total_price)
    return total_prices

# ממשק Streamlit
st.sidebar.write("### Select products to add to the basket")
selected_products = st.sidebar.multiselect("Products", list(products.keys()))

# חישוב מחירים
total_prices = calculate_prices(selected_products)

# יצירת הגרף
fig, ax = plt.subplots(figsize=(8, 6))
sizes = np.array(total_prices) * 5  # שינוי לגודל ריבועים
colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

for i, year in enumerate(years):
    ax.scatter(i, 1, s=sizes[i], color=colors[i], label=f"{year}: ${total_prices[i]:.2f}")

ax.set_xticks(range(len(years)))
ax.set_xticklabels(years)
ax.set_yticks([])
ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
ax.set_title("Yearly Basket Price Change")
st.pyplot(fig)
