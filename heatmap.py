import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

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
    growth_rate = data[column].pct_change().fillna(0) * 100
    return growth_rate

# הוספת שיעורי גדילה לנתונים
salary_df["salary_growth"] = calculate_growth_rate(salary_df, "salary")
basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# פונקציה לחיזוי נתונים עד 2030
def forecast_growth(data, column, growth_column, start_year, end_year):
    avg_growth = data[growth_column].mean()
    forecasted_years = list(range(start_year, end_year + 1))
    last_value = data[column].iloc[-1]
    forecasted_values = [last_value]
    
    for _ in range(len(forecasted_years) - 1):
        forecasted_values.append(forecasted_values[-1] * (1 + avg_growth / 100))
    
    forecasted_df = pd.DataFrame({
        "year": forecasted_years,
        column: forecasted_values,
        growth_column: [avg_growth] * len(forecasted_years)
    })
    return forecasted_df

# חיזוי נתונים לשנים 2025–2030
forecasted_salary = forecast_growth(salary_df, "salary", "salary_growth", 2025, 2030)
forecasted_basket = forecast_growth(basket_df, "price for basic basket", "basket_growth", 2025, 2030)
forecasted_rent = forecast_growth(rent_df, "price for month", "rent_growth", 2025, 2030)
forecasted_fuel = forecast_growth(fuel_df, "price per liter", "fuel_growth", 2025, 2030)

# שילוב הנתונים המקוריים עם החיזויים
salary_df = pd.concat([salary_df, forecasted_salary], ignore_index=True)
basket_df = pd.concat([basket_df, forecasted_basket], ignore_index=True)
rent_df = pd.concat([rent_df, forecasted_rent], ignore_index=True)
fuel_df = pd.concat([fuel_df, forecasted_fuel], ignore_index=True)

# ממשק Streamlit
st.title("Growth Rate Comparison: Salaries vs Categories")
st.sidebar.title("Filters")

# בחירת שנים להצגה
start_year, end_year = st.sidebar.slider(
    "Select Year Range:",
    int(salary_df["year"].min()),
    int(salary_df["year"].max()),
    (int(salary_df["year"].min()), int(salary_df["year"].max()))
)

# סינון נתונים לפי שנים
filtered_salary = salary_df[(salary_df["year"] >= start_year) & (salary_df["year"] <= end_year)]
filtered_basket = basket_df[(basket_df["year"] >= start_year) & (basket_df["year"] <= end_year)]
filtered_rent = rent_df[(rent_df["year"] >= start_year) & (rent_df["year"] <= end_year)]
filtered_fuel = fuel_df[(fuel_df["year"] >= start_year) & (fuel_df["year"] <= end_year)]

# גרף השוואתי
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(filtered_salary["year"], filtered_salary["salary_growth"], label="Salary Growth", marker='o', color='blue')
ax.plot(filtered_basket["year"], filtered_basket["basket_growth"], label="Basket Growth", marker='o', color='orange')
ax.plot(filtered_rent["year"], filtered_rent["rent_growth"], label="Rent Growth", marker='o', color='green')
ax.plot(filtered_fuel["year"], filtered_fuel["fuel_growth"], label="Fuel Growth", marker='o', color='red')
ax.set_title("Growth Rate Comparison: Salaries vs Categories")
ax.set_xlabel("Year")
ax.set_ylabel("Growth Rate (%)")
ax.legend()
ax.grid(True)

# הצגת הגרף
st.pyplot(fig)
