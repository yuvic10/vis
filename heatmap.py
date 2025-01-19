import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# URLs for the Excel files
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# Title of the app
st.title("Cost of Living vs Salaries Analysis")

try:
    # Load data
    basket_data = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_data = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_data = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_data = pd.read_excel(fuel_file_url, engine="openpyxl")

    # Round values for consistency
    basket_data["price for basic basket"] = basket_data["price for basic basket"].round(3)
    fuel_data["price per liter"] = fuel_data["price per liter"].round(3)

    # Calculate relative cost (percentage of salary)
    basket_data["relative_cost"] = basket_data["price for basic basket"] / salary_data["salary"] * 100
    rent_data["relative_cost"] = rent_data["price for month"] / salary_data["salary"] * 100
    fuel_data["relative_cost"] = fuel_data["price per liter"] / salary_data["salary"] * 100

    # Create a heatmap-ready DataFrame
    heatmap_data = {
        "Year": basket_data["year"],
        "Basket % of Salary": basket_data["relative_cost"],
        "Rent % of Salary": rent_data["relative_cost"],
        "Fuel % of Salary": fuel_data["relative_cost"],
    }
    heatmap_df = pd.DataFrame(heatmap_data).set_index("Year")

    # User selection for categories and years
    st.sidebar.header("Filters")
    categories = st.sidebar.multiselect(
        "Select categories to display:", ["Basket % of Salary", "Rent % of Salary", "Fuel % of Salary"],
        default=["Basket % of Salary", "Rent % of Salary", "Fuel % of Salary"]
    )
    year_range = st.sidebar.slider(
        "Select year range:",
        int(heatmap_df.index.min()),
        int(heatmap_df.index.max()),
        (int(heatmap_df.index.min()), int(heatmap_df.index.max()))
    )

    # Filter data based on user selections
    filtered_data = heatmap_df.loc[year_range[0]:year_range[1], categories]

    # Generate heatmap
    st.write("### Heatmap of Cost of Living as Percentage of Salary")
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        filtered_data.transpose(),
        annot=True, fmt=".2f", cmap="coolwarm", cbar=True,
        linewidths=.5, linecolor="gray"
    )
    plt.title("Cost of Living Relative to Salaries Over Time")
    plt.xlabel("Year")
    plt.ylabel("Categories")
    st.pyplot(plt)

except Exception as e:
    st.error(f"An error occurred: {e}")
