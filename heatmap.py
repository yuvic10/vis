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
st.title("Correlation Representation: Yearly Changes")

# Dropdown for category selection
categories = ["Basket Growth", "Rent Growth", "Fuel Growth"]
category_x = st.selectbox("Select first category:", categories)
category_y = st.selectbox("Select second category:", categories)

# Calculate correlation status for each year
growth_data["Correlation Status"] = np.where(
    (growth_data[category_x] > 0) & (growth_data[category_y] > 0), "Both Up",
    np.where((growth_data[category_x] < 0) & (growth_data[category_y] < 0), "Both Down", "Mixed")
)

# Map correlation status to colors
color_map = {"Both Up": "green", "Both Down": "red", "Mixed": "orange"}
growth_data["Color"] = growth_data["Correlation Status"].map(color_map)

# Plot the results
fig, ax = plt.subplots(figsize=(10, 6))
for i, row in growth_data.iterrows():
    ax.scatter(i, 0, color=row["Color"], s=100, label=row["Correlation Status"] if row["Correlation Status"] not in ax.get_legend_handles_labels()[1] else "")
    ax.text(i, 0, f'{row["year"]}', ha='center', va='center', fontsize=8, color='black')

# Formatting
ax.set_yticks([])
ax.set_xticks([])
ax.set_title(f"Correlation of {category_x} and {category_y} Over Time", fontsize=14)
ax.legend(title="Correlation Status", loc="upper left")
st.pyplot(fig)
