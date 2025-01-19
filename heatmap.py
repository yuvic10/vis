import streamlit as st
import pandas as pd
import numpy as np
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

# Combine data into a single DataFrame for Stream Graph
stream_data = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"]
})
stream_data.set_index("Year", inplace=True)

# Streamlit UI
st.title("Stream Graph: Percentage of Salary Over Time")

# Plot Stream Graph
fig, ax = plt.subplots(figsize=(12, 8))
categories = ["Basket", "Rent", "Fuel"]
colors = ["#FF9999", "#66B2FF", "#99FF99"]

ax.stackplot(
    stream_data.index,
    [stream_data[cat] for cat in categories],
    labels=categories,
    colors=colors,
    alpha=0.8
)

# Add titles and legend
ax.set_title("Percentage of Salary by Category Over Time", fontsize=16, fontweight="bold")
ax.set_xlabel("Year", fontsize=14)
ax.set_ylabel("Percentage of Salary", fontsize=14)
ax.legend(loc="upper left", fontsize=12, title="Categories")

# Display chart
st.pyplot(fig)
