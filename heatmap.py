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
        ratios = [1]  # The first year ratio is always 1
        for i in range(1, len(df)):
            ratios.append(df["salary"].iloc[i] / df["salary"].iloc[i - 1])
        df["ratio"] = ratios
        return df

    salary_data = calculate_salary_ratios(salary_data)

    # Calculate predicted prices based on salary ratios
    def calculate_predicted_prices(real_prices, salary_ratios):
        predicted_prices = [real_prices.iloc[0]]  # Start with the first real price
        for i in range(1, len(real_prices)):
            predicted = predicted_prices[-1] * salary_ratios[i]
            predicted_prices.append(predicted)
        return predicted_prices

    # Prepare data for visualization
    def prepare_data(real_df, salary_df, value_column):
        real_prices = real_df.set_index("year")[value_column]
        salary_ratios = salary_df.set_index("year")["ratio"].tolist()
        predicted_prices = calculate_predicted_prices(real_prices, salary_ratios)
        return real_prices, predicted_prices

    # Calculate real and predicted prices for each category
    basket_real, basket_predicted = prepare_data(basket_data, salary_data, "price for basic basket")
    rent_real, rent_predicted = prepare_data(rent_data, salary_data, "price for month")
    fuel_real, fuel_predicted = prepare_data(fuel_data, salary_data, "price per liter")

    # Create a heatmap-ready DataFrame
    heatmap_data = {
        "Year": basket_data["year"],
        "Basket Difference": [p - r for p, r in zip(basket_predicted, basket_real)],
        "Rent Difference": [p - r for p, r in zip(rent_predicted, rent_real)],
        "Fuel Difference": [p - r for p, r in zip(fuel_predicted, fuel_real)],
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
