import streamlit as st
import pandas as pd
import numpy as np
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
st.title("Coxcomb Chart: Percentage of Salary Spent on Categories")

# Select category
category_options = {
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"],
}
selected_category = st.selectbox("Select a category to display:", list(category_options.keys()))

# Prepare data for the selected category
selected_data = category_options[selected_category]
years = basket_df["year"]  # Assuming all datasets have the same years

# Create polar area chart
angles = np.linspace(0, 2 * np.pi, len(years), endpoint=False).tolist()
values = selected_data.tolist()
angles += angles[:1]  # Closing the circle
values += values[:1]

# Define colors for each year
colors = plt.cm.viridis(np.linspace(0, 1, len(years)))

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
bars = ax.bar(
    angles[:-1],  # Angles for the bars
    selected_data,  # Values for the bars
    width=2 * np.pi / len(years),  # Width of each bar
    color=colors,  # Assign colors for each bar
    edgecolor="black",
    alpha=0.8,
)

# Add text in the center
total_percentage = selected_data.sum()
ax.text(
    0,
    0,
    f"{total_percentage:.1f}%",
    ha="center",
    va="center",
    fontsize=20,
    color="black",
    fontweight="bold",
)

# Remove the circular frame
ax.spines["polar"].set_visible(False)
ax.set_yticks([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(years)
ax.set_title(f"{selected_category} Percentage of Salary Over Time", va="bottom", fontsize=14)

# Display the chart
st.pyplot(fig)
