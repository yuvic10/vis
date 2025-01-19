import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# טעינת הנתונים
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, salary_df, rent_df, fuel_df

basket_df, salary_df, rent_df, fuel_df = load_data()

# פונקציה לחישוב שיעור הגדילה
def calculate_growth_rate(data, column):
    growth_rate = data[column].pct_change().fillna(0) + 1
    return growth_rate

# חישוב שיעורי הגדילה
basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# יצירת משכורות מדומות
salary_df["simulated_basket_salary"] = salary_df["salary"].iloc[0]
salary_df["simulated_rent_salary"] = salary_df["salary"].iloc[0]
salary_df["simulated_fuel_salary"] = salary_df["salary"].iloc[0]

for i in range(1, len(salary_df)):
    salary_df.loc[i, "simulated_basket_salary"] = salary_df.loc[i - 1, "simulated_basket_salary"] * basket_df.loc[i, "basket_growth"]
    salary_df.loc[i, "simulated_rent_salary"] = salary_df.loc[i - 1, "simulated_rent_salary"] * rent_df.loc[i, "rent_growth"]
    salary_df.loc[i, "simulated_fuel_salary"] = salary_df.loc[i - 1, "simulated_fuel_salary"] * fuel_df.loc[i, "fuel_growth"]

# ממשק Streamlit
st.title("Simulated Salaries Based on Category Growth")

# גרף השוואתי
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(salary_df["year"], salary_df["salary"], label="Actual Salary", marker='o', color='blue')
ax.plot(salary_df["year"], salary_df["simulated_basket_salary"], label="Simulated Salary (Basket)", marker='o', linestyle='--', color='orange')
ax.plot(salary_df["year"], salary_df["simulated_rent_salary"], label="Simulated Salary (Rent)", marker='o', linestyle='--', color='green')
ax.plot(salary_df["year"], salary_df["simulated_fuel_salary"], label="Simulated Salary (Fuel)", marker='o', linestyle='--', color='red')

ax.set_title("Simulated Salaries vs. Actual Salary", fontsize=16)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Salary", fontsize=12)
ax.legend()
ax.grid(True)

# הצגת הגרף
st.pyplot(fig)
