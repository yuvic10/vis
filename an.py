import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# נתונים לדוגמה
years = np.arange(2010, 2023)
wages = [4500, 4700, 4900, 5100, 5300, 5600, 5900, 6200, 6500, 6700, 6900, 7100, 7300]
fuel_prices = [6, 6.2, 6.5, 6.7, 7, 7.2, 7.5, 7.8, 8, 8.2, 8.5, 8.8, 9]
rent_prices = [3000, 3100, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200]
product_prices = [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160]

# הכנת DataFrame
data = pd.DataFrame({
    "Year": years,
    "Wages": wages,
    "Fuel": fuel_prices,
    "Rent": rent_prices,
    "Products": product_prices
})

# חישוב אחוז השינוי האמיתי במשכורות
data["Wage Growth (%)"] = data["Wages"].pct_change().fillna(0) * 100

# ממשק Streamlit
st.title("Real vs. Simulated Prices Based on Wage Growth (Area Chart)")
st.sidebar.header("Interactive Controls")

# מחוון לשינוי אחוזי עלייה
custom_growth = st.sidebar.slider("Set Custom Wage Growth (%)", min_value=-5.0, max_value=10.0, step=0.1, value=2.0)

# הוספת נתונים מדומים עם אחוז העלייה שנבחר
categories = ["Fuel", "Rent", "Products"]
for category in categories:
    initial_value = data[category].iloc[0]
    data[f"{category}_Simulated"] = [initial_value * ((1 + custom_growth / 100) ** i) for i in range(len(data))]
    data[f"{category}_Gap"] = data[f"{category}_Simulated"] - data[category]

# גרף שטחים
fig, ax = plt.subplots(figsize=(10, 6))
for category in categories:
    # אזור אמיתי
    ax.fill_between(data["Year"], 0, data[category], color="blue", alpha=0.3, label=f"{category} (Real)")
    # אזור מדומה
    ax.fill_between(data["Year"], data[category], data[f"{category}_Simulated"], 
                    where=(data[f"{category}_Simulated"] >= data[category]),
                    interpolate=True, color="green", alpha=0.3, label=f"{category} Surplus")
    ax.fill_between(data["Year"], data[category], data[f"{category}_Simulated"], 
                    where=(data[f"{category}_Simulated"] < data[category]),
                    interpolate=True, color="red", alpha=0.3, label=f"{category} Deficit")

ax.set_title("Real vs. Simulated Prices with Gaps")
ax.set_xlabel("Year")
ax.set_ylabel("Price")
ax.legend()
ax.grid()

st.pyplot(fig)

# הצגת טבלה
st.subheader("Data Table")
st.dataframe(data)
