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
st.title("Real vs Simulated Prices Heatmap")

try:
    # Load data
    basket_data = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_data = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_data = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_data = pd.read_excel(fuel_file_url, engine="openpyxl")

    # Round values for consistency
    basket_data["price for basic basket"] = basket_data["price for basic basket"].round(3)
    fuel_data["price per liter"] = fuel_data["price per liter"].round(3)

    # Calculate yearly ratios (slopes) for salaries
    def calculate_salary_ratios(df):
        ratios = [1]  # Start with a ratio of 1 for the first year
        for i in range(1, len(df)):
            ratio = df["salary"].iloc[i] / df["salary"].iloc[i - 1]
            ratios.append(ratio)
        return ratios

    salary_ratios = calculate_salary_ratios(salary_data)

    # Calculate predicted prices based on salary ratios
    def calculate_predicted_prices(real_prices, salary_ratios):
        predicted_prices = [real_prices.iloc[0]]  # Start with the first real price
        for i in range(1, len(real_prices)):
            predicted = predicted_prices[-1] * salary_ratios[i]
            predicted_prices.append(predicted)
        return predicted_prices

    basket_data["simulated price for basket"] = calculate_predicted_prices(
        basket_data["price for basic basket"], salary_ratios
    )
    rent_data["simulated price for month"] = calculate_predicted_prices(
        rent_data["price for month"], salary_ratios
    )
    fuel_data["simulated price per liter"] = calculate_predicted_prices(
        fuel_data["price per liter"], salary_ratios
    )

    # Create a heatmap-ready DataFrame
    heatmap_data = {
        "Year": basket_data["year"],
        "Basket Difference": basket_data["simulated price for basket"] - basket_data["price for basic basket"],
        "Rent Difference": rent_data["simulated price for month"] - rent_data["price for month"],
        "Fuel Difference": fuel_data["simulated price per liter"] - fuel_data["price per liter"],
    }
    heatmap_df = pd.DataFrame(heatmap_data).set_index("Year")

    # User selection for categories and years
    st.sidebar.header("Filters")
    categories = st.sidebar.multiselect(
        "Select categories to display:", ["Basket Difference", "Rent Difference", "Fuel Difference"],
        default=["Basket Difference", "Rent Difference", "Fuel Difference"]
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
    st.write("### Heatmap of Real vs Simulated Price Differences")
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        filtered_data.transpose(),
        annot=True, fmt=".3f", cmap="coolwarm", cbar=True,
        linewidths=.5, linecolor="gray"
    )
    st.pyplot(plt)

except Exception as e:
    st.error(f"An error occurred: {e}")
