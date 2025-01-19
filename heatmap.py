import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
st.title("Artistic Shape Visualization for Category Percentages")

# Select category
category_options = {
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"],
}
selected_category = st.selectbox("Select a category to display:", list(category_options.keys()))

# Prepare data for the selected category
selected_data = category_options[selected_category]
years = basket_df["year"]

# Create artistic visualization
fig, ax = plt.subplots(figsize=(12, 8))

for i, value in enumerate(selected_data):
    # Create the curve-like shape for each year
    x = np.linspace(i - 0.4, i + 0.4, 100)
    y = value * np.sin((x - i) * np.pi) + value / 2  # Shape resembling a curve
    ax.fill_between(x, 0, y, color="teal", alpha=0.6)

    # Add a label at the peak of each curve
    ax.text(i, value + 1, f"{value:.1f}%", ha="center", fontsize=10, color="black", fontweight="bold")

# Set labels and styling
ax.set_xticks(range(len(years)))
ax.set_xticklabels(years, fontsize=10, rotation=45)
ax.set_yticks([])
ax.set_xlim(-0.5, len(years) - 0.5)
ax.set_ylim(0, max(selected_data) + 10)
ax.set_title(f"{selected_category} Percentage of Salary Over Time", fontsize=16, fontweight="bold")
ax.axis("off")  # Hide the axis for a cleaner look

# Display the chart
st.pyplot(fig)
