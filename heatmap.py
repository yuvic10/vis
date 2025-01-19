import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    salary_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx")
    rent_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx", sheet_name="Sheet2")
    fuel_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx")
    basket_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx")
    return salary_df, rent_df, fuel_df, basket_df

salary_df, rent_df, fuel_df, basket_df = load_data()

# Calculate yearly ratios (slopes) for salaries
def calculate_salary_ratios(df):
    df["ratio"] = df["salary"] / df["salary"].shift(1)
    df["ratio"].iloc[0] = 1  # Set the first year ratio to 1
    return df

salary_df = calculate_salary_ratios(salary_df)

# Calculate predicted prices based on salary ratios
def calculate_predicted_prices(real_prices, salary_ratios):
    predicted_prices = [real_prices.iloc[0]]  # Start with the first real price
    for i in range(1, len(real_prices)):
        predicted = predicted_prices[-1] * salary_ratios.iloc[i]
        predicted_prices.append(predicted)
    return predicted_prices

# Prepare data for Heatmap
def prepare_heatmap_data(real_df, salary_df, value_column, label):
    real_prices = real_df.set_index("year")[value_column]
    salary_ratios = salary_df.set_index("year")["ratio"].fillna(1)
    predicted_prices = calculate_predicted_prices(real_prices, salary_ratios)
    differences = [pred - real for pred, real in zip(predicted_prices, real_prices)]
    return pd.DataFrame({
        "Year": real_prices.index,
        f"{label} Difference": differences
    }).set_index("Year")

# Prepare data for each category
basket_diff = prepare_heatmap_data(basket_df, salary_df, "price for basic basket", "Basket")
rent_diff = prepare_heatmap_data(rent_df, salary_df, "price for month", "Rent")
fuel_diff = prepare_heatmap_data(fuel_df, salary_df, "price per liter", "Fuel")

# Combine all differences into a single DataFrame
heatmap_data = pd.concat([basket_diff, rent_diff, fuel_diff], axis=1)

# Streamlit UI
st.title("Real vs Simulated Prices Heatmap")
st.sidebar.title("Filter Options")

# User selections for categories and years
categories = st.sidebar.multiselect(
    "Select categories to display:",
    heatmap_data.columns.tolist(),
    default=heatmap_data.columns.tolist()
)
year_range = st.sidebar.slider(
    "Select year range:",
    int(heatmap_data.index.min()),
    int(heatmap_data.index.max()),
    (int(heatmap_data.index.min()), int(heatmap_data.index.max()))
)

# Filter data based on user selections
filtered_data = heatmap_data.loc[year_range[0]:year_range[1], categories]

# Generate Heatmap
st.write("### Heatmap of Real vs Simulated Price Differences")
plt.figure(figsize=(12, 6))
sns.heatmap(
    filtered_data.transpose(),
    annot=True, fmt=".2f", cmap="coolwarm", cbar=True,
    linewidths=.5, linecolor="gray"
)
st.pyplot(plt)
