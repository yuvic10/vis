import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# URLs for the Excel files
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# Load data
@st.cache_data
def load_data():
    basket_data = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_data = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_data = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_data = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_data, salary_data, rent_data, fuel_data

basket_data, salary_data, rent_data, fuel_data = load_data()

# Calculate yearly ratios for salaries
salary_data["growth rate"] = salary_data["salary"].pct_change().fillna(0)

# Calculate simulated prices based on salary ratios
def calculate_predicted_prices(real_prices, salary_ratios):
    predicted_prices = [real_prices.iloc[0]]  # Start with the first real price
    for i in range(1, len(real_prices)):
        predicted = predicted_prices[-1] * (1 + salary_ratios.iloc[i])
        predicted_prices.append(predicted)
    return predicted_prices

# Calculate predicted prices for all categories
basket_data["predicted price"] = calculate_predicted_prices(
    basket_data["price for basic basket"], salary_data["growth rate"]
)
rent_data["predicted price"] = calculate_predicted_prices(
    rent_data["price for month"], salary_data["growth rate"]
)
fuel_data["predicted price"] = calculate_predicted_prices(
    fuel_data["price per liter"], salary_data["growth rate"]
)

# Calculate percentage difference between real and predicted prices
basket_data["percentage difference"] = (
    (basket_data["price for basic basket"] - basket_data["predicted price"])
    / basket_data["predicted price"]
) * 100
rent_data["percentage difference"] = (
    (rent_data["price for month"] - rent_data["predicted price"])
    / rent_data["predicted price"]
) * 100
fuel_data["percentage difference"] = (
    (fuel_data["price per liter"] - fuel_data["predicted price"])
    / fuel_data["predicted price"]
) * 100

# Create a heatmap-ready DataFrame
heatmap_data = pd.DataFrame({
    "Year": basket_data["year"],
    "Basket Difference (%)": basket_data["percentage difference"],
    "Rent Difference (%)": rent_data["percentage difference"],
    "Fuel Difference (%)": fuel_data["percentage difference"],
}).set_index("Year")

# User selection for categories and years
st.sidebar.header("Filters")
categories = st.sidebar.multiselect(
    "Select categories to display:", ["Basket Difference (%)", "Rent Difference (%)", "Fuel Difference (%)"],
    default=["Basket Difference (%)", "Rent Difference (%)", "Fuel Difference (%)"]
)
year_range = st.sidebar.slider(
    "Select year range:",
    int(heatmap_data.index.min()),
    int(heatmap_data.index.max()),
    (int(heatmap_data.index.min()), int(heatmap_data.index.max()))
)

# Filter data based on user selections
filtered_data = heatmap_data.loc[year_range[0]:year_range[1], categories]

# Generate heatmap
st.write("### Heatmap of Percentage Difference Between Real and Predicted Prices")
plt.figure(figsize=(12, 6))
sns.heatmap(
    filtered_data.transpose(),
    annot=True, fmt=".1f", cmap="coolwarm", cbar=True,
    linewidths=.5, linecolor="gray"
)
st.pyplot(plt)
