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
@st.cache_data
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0) * 100

# הוספת שיעורי גדילה לנתונים
salary_df["salary_growth"] = calculate_growth_rate(salary_df, "salary")
basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# מיזוג הנתונים
merged_data = pd.DataFrame({
    "Year": salary_df["year"],
    "Salary Growth": salary_df["salary_growth"],
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"]
})

# ממשק Streamlit
st.title("Correlation Between Salary Growth and Categories")

# בחירת קטגוריות להשוואה
categories = st.multiselect(
    "Select Categories to Compare with Salary Growth:",
    ["Basket Growth", "Rent Growth", "Fuel Growth"],
    default=["Basket Growth", "Rent Growth", "Fuel Growth"]
)

# סינון נתונים לקטגוריות שנבחרו
filtered_data = merged_data[["Year", "Salary Growth"] + categories]

# יצירת Scatter Plot
fig, ax = plt.subplots(figsize=(10, 6))
for category in categories:
    ax.scatter(
        filtered_data["Salary Growth"],
        filtered_data[category],
        label=category
    )
ax.set_title("Scatter Plot: Salary Growth vs Category Growth")
ax.set_xlabel("Salary Growth (%)")
ax.set_ylabel("Category Growth (%)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# יצירת Bubble Chart
fig, ax = plt.subplots(figsize=(10, 6))
for category in categories:
    size = (filtered_data[category].abs() + 1) * 10  # קוטר הבועה
    ax.scatter(
        filtered_data["Year"],
        filtered_data[category],
        s=size,
        label=category,
        alpha=0.6
    )
ax.set_title("Bubble Chart: Category Growth Over Years")
ax.set_xlabel("Year")
ax.set_ylabel("Category Growth (%)")
ax.legend()
ax.grid(True)

st.pyplot(fig)
