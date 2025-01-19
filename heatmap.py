import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    salary_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx", engine="openpyxl")
    basket_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx", engine="openpyxl")
    rent_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx", engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx", engine="openpyxl")
    return salary_df, basket_df, rent_df, fuel_df

salary_df, basket_df, rent_df, fuel_df = load_data()

# Calculate growth rates
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0) * 100

salary_df["Salary Growth"] = calculate_growth_rate(salary_df, "salary")
basket_df["Basket Growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["Rent Growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["Fuel Growth"] = calculate_growth_rate(fuel_df, "price per liter")

# Combine data
growth_data = pd.DataFrame({
    "Year": salary_df["year"],
    "Salary Growth": salary_df["Salary Growth"],
    "Basket Growth": basket_df["Basket Growth"],
    "Rent Growth": rent_df["Rent Growth"],
    "Fuel Growth": fuel_df["Fuel Growth"]
})

# Calculate correlations between salary growth and each category
correlations = growth_data.corr().loc["Salary Growth", ["Basket Growth", "Rent Growth", "Fuel Growth"]]

# Streamlit UI
st.title("Heatmap of Correlation Between Salary Growth and Categories")

# Reshape data for heatmap
heatmap_data = pd.DataFrame({
    "Category": correlations.index,
    "Correlation with Salary Growth": correlations.values
})

# Create heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(heatmap_data.set_index("Category"), annot=True, cmap="coolwarm", fmt=".2f", cbar=True)
plt.title("Correlation of Categories with Salary Growth")
plt.ylabel("")
st.pyplot(plt)
