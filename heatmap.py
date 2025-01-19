import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"

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
st.title("Yearly Pie Charts: Percentage of Salary Spent")

# Select category
category_options = {
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"],
}
selected_category = st.selectbox("Select a category to display:", list(category_options.keys()))

# Select years to display
selected_years = st.multiselect("Select years to display:", basket_df["year"].unique(), default=basket_df["year"].unique())

# Create a pie chart for each selected year
fig, axes = plt.subplots(1, len(selected_years), figsize=(len(selected_years) * 5, 5))

if len(selected_years) == 1:
    axes = [axes]  # Ensure axes is always iterable for a single chart

for i, year in enumerate(selected_years):
    year_data = category_options[selected_category][basket_df["year"] == year].values[0]
    salary_data = 100 - year_data  # Remaining salary percentage
    labels = [f"{selected_category} ({year})", "Remaining Salary"]
    values = [year_data, salary_data]

    axes[i].pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#FF9999", "#66B2FF"])
    axes[i].set_title(f"{selected_category} in {year}")

plt.tight_layout()
st.pyplot(fig)
