import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתונים לדוגמה
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
salaries = [5000, 5200, 5400, 5600, 5800, 6000, 6200, 6400]  # משכורות
products_prices = [200, 220, 250, 270, 300, 320, 350, 370]  # מחירי מוצרים
fuel_prices = [6, 6.2, 6.5, 6.8, 7, 7.2, 7.5, 7.8]  # מחירי דלק
rent_prices = [3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700]  # מחירי שכירות

# חישוב אחוזי שינוי במשכורות
salary_growth = [0] + [((salaries[i] - salaries[i-1]) / salaries[i-1]) for i in range(1, len(salaries))]

# פונקציה לחישוב מחירים מדומים
def calculate_simulated_prices(prices, growth):
    simulated = [prices[0]]
    for i in range(1, len(prices)):
        simulated.append(simulated[-1] * (1 + growth[i]))
    return simulated

# מחירים מדומים לכל קטגוריה
simulated_products = calculate_simulated_prices(products_prices, salary_growth)
simulated_fuel = calculate_simulated_prices(fuel_prices, salary_growth)
simulated_rent = calculate_simulated_prices(rent_prices, salary_growth)

# Streamlit UI
st.title("Real vs Simulated Prices Based on Salary Growth")
category = st.selectbox("Choose a category", ["Products", "Fuel", "Rent"])

# בחר קטגוריה להצגה
if category == "Products":
    real_prices = products_prices
    simulated_prices = simulated_products
elif category == "Fuel":
    real_prices = fuel_prices
    simulated_prices = simulated_fuel
else:
    real_prices = rent_prices
    simulated_prices = simulated_rent

# יצירת גרף
fig, ax = plt.subplots()
ax.fill_between(years, real_prices, simulated_prices, color="red", alpha=0.3, label="Gap")
ax.plot(years, real_prices, label="Real Prices", color="blue")
ax.plot(years, simulated_prices, label="Simulated Prices", color="green")
ax.set_title(f"{category} Prices: Real vs Simulated")
ax.set_xlabel("Year")
ax.set_ylabel("Price")
ax.legend()

# הצגת הגרף
st.pyplot(fig)
