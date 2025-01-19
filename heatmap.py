import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"],
})

# Streamlit UI
st.title("Scatter Plot Matrix: Category Correlations")

# Plot pairplot
scatter_plot = sns.pairplot(growth_data)
st.pyplot(scatter_plot)
