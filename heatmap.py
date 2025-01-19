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

# Calculate percentage of salary spent on each category
basket_df["basket_percent"] = (basket_df["price for basic basket"] / salary_df["salary"]) * 100
rent_df["rent_percent"] = (rent_df["price for month"] / salary_df["salary"]) * 100

# Streamlit UI
st.title("Correlation Between Two Categories")

# Select categories for comparison
category_x = st.selectbox("Select Category for X-axis:", ["Basket", "Rent"])
category_y = st.selectbox("Select Category for Y-axis:", ["Basket", "Rent"])

# Map selected categories to their data
category_data = {
    "Basket": basket_df["basket_percent"],
    "Rent": rent_df["rent_percent"],
}
x_data = category_data[category_x]
y_data = category_data[category_y]

# Create a scatter plot
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(x_data, y_data, c="blue", alpha=0.7, edgecolors="k")
ax.set_title(f"Correlation Between {category_x} and {category_y}", fontsize=14)
ax.set_xlabel(f"{category_x} (% of Salary)", fontsize=12)
ax.set_ylabel(f"{category_y} (% of Salary)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)
