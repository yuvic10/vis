import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# נתונים לדוגמה
years = list(range(2010, 2021))
real_prices = {
    "Fuel": [6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11],
    "Rent": [3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000],
    "Products": [500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700],
}
salary_growth_rates = [2.5, 3, 2, 2.5, 3, 2, 1.5, 2.5, 3, 2, 2.5]  # אחוזי שינוי של המשכורות

# פונקציה לחישוב מחירים מדומים על סמך אחוזי שינוי השכר
def calculate_projected_prices(base_prices, growth_rates):
    projected_prices = [base_prices[0]]
    for i in range(1, len(base_prices)):
        projected_price = projected_prices[-1] * (1 + growth_rates[i - 1] / 100)
        projected_prices.append(projected_price)
    return projected_prices

# יצירת מחירים מדומים
projected_prices = {
    category: calculate_projected_prices(prices, salary_growth_rates)
    for category, prices in real_prices.items()
}

# אפליקציה ב-Streamlit
st.title("Real vs. Projected Prices Based on Salary Growth")

# בחירת קטגוריה
category = st.selectbox("Select a category:", ["Fuel", "Rent", "Products"])

# הצגת מחוון לאחוז עלייה נוסף
additional_growth = st.slider("Additional salary growth (%)", min_value=0.0, max_value=5.0, value=0.0, step=0.1)

# עדכון המחירים המדומים לפי אחוז עלייה נוסף
def adjust_projected_prices(base_projected_prices, additional_growth):
    adjusted_prices = []
    for price in base_projected_prices:
        adjusted_prices.append(price * (1 + additional_growth / 100))
    return adjusted_prices

adjusted_projected_prices = adjust_projected_prices(projected_prices[category], additional_growth)

# יצירת הגרף
fig, ax = plt.subplots(figsize=(10, 6))

ax.fill_between(years, real_prices[category], adjusted_projected_prices, where=np.array(adjusted_projected_prices) > np.array(real_prices[category]), 
                facecolor='green', alpha=0.3, label='Surplus (Projected > Real)')
ax.fill_between(years, real_prices[category], adjusted_projected_prices, where=np.array(adjusted_projected_prices) <= np.array(real_prices[category]), 
                facecolor='red', alpha=0.3, label='Deficit (Projected <= Real)')

ax.plot(years, real_prices[category], label="Real Prices", color="blue", linewidth=2)
ax.plot(years, adjusted_projected_prices, label="Projected Prices", color="orange", linestyle="--", linewidth=2)

ax.set_title(f"{category}: Real vs. Projected Prices", fontsize=16)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Price (NIS)", fontsize=12)
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)

# הצגת הגרף ב-Streamlit
st.pyplot(fig)
