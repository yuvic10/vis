import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

# Combine the data for visualization
data = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"]
})

# Streamlit UI
st.title("Bubble Chart: Percentage of Salary Spent on Categories")

# Select categories to display
categories = ["Basket", "Rent", "Fuel"]
selected_categories = st.multiselect("Select categories to display:", categories, default=categories)

# Prepare data for visualization
x_positions = np.arange(len(data["Year"]))
bubble_scale = 30  # Scaling factor for bubble size

fig, ax = plt.subplots(figsize=(12, 8))

for category in selected_categories:
    values = data[category]
    ax.scatter(
        x_positions, 
        values, 
        s=[v * bubble_scale for v in values], 
        alpha=0.6, 
        label=category
    )

# Add labels and legend
ax.set_xticks(x_positions)
ax.set_xticklabels(data["Year"])
ax.set_xlabel("Year")
ax.set_ylabel("Percentage of Salary")
ax.set_title("Percentage of Salary Spent on Categories Over Time", fontsize=14)
ax.legend()

# Display chart
st.pyplot(fig)
