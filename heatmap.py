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
    return data[column].pct_change().fillna(0) * 100

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
st.title("Correlation Between Categories Over Time")

# Dropdowns for selecting categories
category_x = st.selectbox("Select Category for X-Axis:", ["Basket Growth", "Rent Growth", "Fuel Growth"])
category_y = st.selectbox("Select Category for Y-Axis:", ["Basket Growth", "Rent Growth", "Fuel Growth"])

# Calculate correlation between the selected categories
correlation = np.corrcoef(growth_data[category_x], growth_data[category_y])[0, 1]

# Scatter plot
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(
    growth_data[category_x],
    growth_data[category_y],
    c=np.abs(growth_data[category_x] - growth_data[category_y]),  # Color based on differences
    cmap="coolwarm",
    s=100,  # Size of the points
    edgecolors="k",
    alpha=0.8,
)

# Add color bar
cbar = fig.colorbar(scatter, ax=ax, label="Difference Between Categories (%)")
ax.set_title(f"Scatter Plot: {category_x} vs {category_y}\nCorrelation: {correlation:.2f}")
ax.set_xlabel(category_x)
ax.set_ylabel(category_y)

# Add year labels to points
for i, year in enumerate(growth_data["year"]):
    ax.text(
        growth_data[category_x][i],
        growth_data[category_y][i],
        str(year),
        fontsize=9,
        ha="right",
        va="bottom",
    )

st.pyplot(fig)
