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

    # Calculate year-over-year growth rates for salaries
    salary_data["growth rate"] = salary_data["salary"].pct_change().fillna(0)

    # Compute simulated prices based on the previous year's simulated price and growth rate
    def compute_simulated_prices(real_prices, growth_rates):
        simulated_prices = [real_prices.iloc[0]]
        for i in range(1, len(real_prices)):
            simulated_price = simulated_prices[-1] * (1 + growth_rates.iloc[i])
            simulated_prices.append(simulated_price)
        return simulated_prices

    basket_data["simulated price for basket"] = compute_simulated_prices(
        basket_data["price for basic basket"], salary_data["growth rate"]
    )
    rent_data["simulated price for month"] = compute_simulated_prices(
        rent_data["price for month"], salary_data["growth rate"]
    )
    fuel_data["simulated price per liter"] = compute_simulated_prices(
        fuel_data["price per liter"], salary_data["growth rate"]
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
