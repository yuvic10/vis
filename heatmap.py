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
fuel_df["fuel_percent"] = (fuel_df["price per liter"] / salary_df["salary"]) * 100

categories = {
    "Basket": basket_df["basket_percent"],
    "Rent": rent_df["rent_percent"],
    "Fuel": fuel_df["fuel_percent"],
}
years = basket_df["year"]

# Streamlit UI
st.title("Percentage of Salary Spent on Each Category")

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

for ax, (category, data) in zip(axes, categories.items()):
    scatter = ax.scatter(
        years,
        [category] * len(years),
        s=data * 10,  # Size of the circles
        c=data,  # Color intensity
        cmap="Greens",
        alpha=0.7,
        edgecolors="k"
    )
    ax.set_title(category)
    ax.set_xticks(years)
    ax.set_yticks([])
    ax.set_xlabel("Year")

fig.colorbar(scatter, ax=axes, orientation="horizontal", label="Percentage of Salary")
st.pyplot(fig)
