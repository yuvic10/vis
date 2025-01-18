import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# יצירת נתונים לדוגמה
np.random.seed(42)
years = np.arange(2000, 2023)
real_prices_fuel = np.cumsum(np.random.uniform(0.5, 1.5, len(years))) * 100
real_prices_rent = np.cumsum(np.random.uniform(1.0, 2.0, len(years))) * 100
real_prices_products = np.cumsum(np.random.uniform(0.3, 1.0, len(years))) * 100

min_wages = np.cumsum(np.random.uniform(1.0, 2.0, len(years))) * 100
avg_wage_growth = ((min_wages[-1] - min_wages[0]) / min_wages[0]) / len(years)

# אפליקציית Streamlit
st.title("Real vs. Simulated Prices with Wage Growth")

# בחירת קטגוריה
categories = {
    "Fuel": real_prices_fuel,
    "Rent": real_prices_rent,
    "Products": real_prices_products
}
category = st.selectbox("Select a category:", list(categories.keys()))

# אחוז שינוי מותאם אישית
custom_growth_rate = st.slider(
    "Select custom wage growth rate (%):", min_value=0.0, max_value=10.0, value=avg_wage_growth * 100.0
) / 100

# חישוב מחירים מדומים
real_prices = categories[category]
simulated_prices = [real_prices[0]]
for i in range(1, len(years)):
    simulated_prices.append(simulated_prices[-1] * (1 + custom_growth_rate))

simulated_prices = np.array(simulated_prices)

differences = simulated_prices - real_prices

# ציור דיאגרמת אזורים
fig, ax = plt.subplots(figsize=(10, 6))
ax.fill_between(years, real_prices, color="blue", alpha=0.6, label="Real Prices")
ax.fill_between(years, simulated_prices, color="green", alpha=0.4, label="Simulated Prices")
ax.fill_between(years, real_prices, simulated_prices, where=simulated_prices > real_prices,
                color="red", alpha=0.3, label="Gap (Overestimated)")
ax.fill_between(years, simulated_prices, real_prices, where=simulated_prices < real_prices,
                color="red", alpha=0.3, label="Gap (Underestimated)")

ax.set_title(f"Real vs. Simulated Prices: {category}", fontsize=16)
ax.set_xlabel("Years", fontsize=12)
ax.set_ylabel("Prices (in $)", fontsize=12)
ax.legend()

st.pyplot(fig)
