import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# Load the data
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df

basket_df, rent_df, fuel_df = load_data()

# Calculate growth rates for each category
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0)

basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# Combine growth data into a single DataFrame
growth_data = pd.DataFrame({
    "year": basket_df["year"],
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"],
})

# Streamlit UI
st.title("Category Correlation: Same vs Opposite Trends")

# Dropdown for category selection
categories = ["Basket Growth", "Rent Growth", "Fuel Growth"]
category_x = st.selectbox("Select first category:", categories)
category_y = st.selectbox("Select second category:", categories)

# Determine correlation status
growth_data["Correlation Status"] = np.where(
    (growth_data[category_x] > 0) & (growth_data[category_y] > 0) |
    (growth_data[category_x] < 0) & (growth_data[category_y] < 0), "Same Trend", "Opposite Trend"
)

# Map correlation status to colors
color_map = {"Same Trend": "green", "Opposite Trend": "red"}
growth_data["Color"] = growth_data["Correlation Status"].map(color_map)

# Plot the results
fig, ax = plt.subplots(figsize=(10, 2))

for i, row in growth_data.iterrows():
    ax.scatter(i, 0, color=row["Color"], s=200)

# Formatting
ax.set_yticks([])
ax.set_xticks([])
ax.set_title(f"Correlation of {category_x} and {category_y}: Same vs Opposite Trends", fontsize=14)
st.pyplot(fig)
