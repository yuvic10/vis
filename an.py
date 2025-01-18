import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# נתונים לדוגמה
data = {
    "Year": list(range(2010, 2024)),
    "Salary": [5000, 5200, 5400, 5600, 5900, 6200, 6500, 6700, 6900, 7200, 7500, 7800, 8000, 8200],
    "Fuel": [5000, 5300, 5600, 5800, 6000, 6200, 6500, 6700, 7000, 7300, 7600, 7900, 8200, 8500],
    "Rent": [7000, 7300, 7600, 7900, 8200, 8500, 8800, 9000, 9300, 9600, 9900, 10200, 10500, 10800],
    "Goods": [3000, 3200, 3400, 3500, 3700, 3900, 4100, 4300, 4500, 4700, 4900, 5100, 5300, 5500],
}
df = pd.DataFrame(data)

# ממשק Streamlit
st.title("Area Chart: Real vs Modeled Prices")
st.sidebar.header("Customize the Visualization")

# בחירת קטגוריה
categories = ["Fuel", "Rent", "Goods"]
selected_categories = st.sidebar.multiselect("Choose categories to display", categories, default=categories)

# מחוון לאחוז השינוי
default_increase = (np.mean(np.diff(df["Salary"]) / df["Salary"][:-1]) * 100).round(2)
growth_rate = st.sidebar.slider("Adjust the annual salary growth rate (%)", min_value=0.0, max_value=10.0, value=default_increase)

# חישוב המחירים המדומים
df["Growth Factor"] = 1 + (growth_rate / 100)
df["Modeled Salary"] = df["Salary"].iloc[0] * np.cumprod(df["Growth Factor"])
for category in categories:
    df[f"Modeled {category}"] = df[category].iloc[0] * np.cumprod(df["Growth Factor"])

# יצירת דיאגרמת האזורים
plt.figure(figsize=(10, 6))
for category in selected_categories:
    plt.fill_between(df["Year"], df[category], color="blue", alpha=0.3, label=f"Actual {category}")
    plt.fill_between(df["Year"], df[f"Modeled {category}"], df[category], color="red", alpha=0.3, label=f"Gap {category}")

plt.title("Real vs Modeled Prices Based on Salary Growth")
plt.xlabel("Year")
plt.ylabel("Price")
plt.legend()
plt.grid()
st.pyplot(plt)
