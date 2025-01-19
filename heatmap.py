import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"

# Load the data
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df, salary_df

basket_df, rent_df, fuel_df, salary_df = load_data()

# Calculate percentage of salary for each category
def calculate_percentage_of_salary(category_price, salary):
    return (category_price / salary) * 100

basket_df["basket_percentage"] = calculate_percentage_of_salary(basket_df["price for basic basket"], salary_df["salary"])
rent_df["rent_percentage"] = calculate_percentage_of_salary(rent_df["price for month"], salary_df["salary"])
fuel_df["fuel_percentage"] = calculate_percentage_of_salary(fuel_df["price per liter"], salary_df["salary"])

# Streamlit UI
st.title("Interactive Donut Chart: Percentage of Salary Spent")

# Select category
category_options = {
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"],
}
selected_category = st.selectbox("Select a category to display:", list(category_options.keys()))

# Select year
selected_year = st.selectbox("Select a year to display:", basket_df["year"].unique())

# Prepare data for the selected year
year_data = category_options[selected_category][basket_df["year"] == selected_year].values[0]
remaining_salary = 100 - year_data

# Create Donut chart
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    [year_data, remaining_salary],
    labels=[f"{selected_category} ({year_data:.1f}%)", f"Remaining Salary ({remaining_salary:.1f}%)"],
    autopct='%1.1f%%',
    startangle=90,
    colors=["#FF9999", "#66B2FF"],
    wedgeprops=dict(width=0.3, edgecolor='w')
)
plt.setp(autotexts, size=10, weight="bold")
ax.set_title(f"Salary Distribution in {selected_year}", fontsize=14, fontweight="bold")

# Display the chart
st.pyplot(fig)
