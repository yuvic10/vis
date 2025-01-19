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
fuel_df["fuel_percent"] = (fuel_df["price per liter"] * 100) / salary_df["salary"]

# Prepare data for visualization
percent_data = pd.DataFrame({
    "year": salary_df["year"],
    "Basket": basket_df["basket_percent"],
    "Rent": rent_df["rent_percent"],
    "Fuel": fuel_df["fuel_percent"],
})

# Streamlit UI
st.title("Percentage of Salary Spent on Each Category Over Time")

# Create a plot
fig, ax = plt.subplots(figsize=(10, 8))
categories = ["Basket", "Rent", "Fuel"]

for i, category in enumerate(categories):
    ax.scatter(
        percent_data["year"], 
        [i + 1] * len(percent_data), 
        s=100,  # Fixed size for all points
        c="green", 
        label=category,
        alpha=0.7,
    )

# Customization
ax.set_yticks(range(1, len(categories) + 1))
ax.set_yticklabels(categories)
ax.set_xticks(percent_data["year"])
ax.set_title("Percentage of Salary Spent on Each Category Over Time", fontsize=14)
ax.set_xlabel("Year")
ax.set_ylabel("Category")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.legend()

st.pyplot(fig)
