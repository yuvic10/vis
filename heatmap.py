import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    salary_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx", engine="openpyxl")
    basket_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx", engine="openpyxl")
    rent_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx", engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx", engine="openpyxl")
    return salary_df, basket_df, rent_df, fuel_df

salary_df, basket_df, rent_df, fuel_df = load_data()

# Calculate growth rates
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0) * 100

salary_df["salary_growth"] = calculate_growth_rate(salary_df, "salary")
basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# Combine data
growth_data = pd.DataFrame({
    "Year": salary_df["year"],
    "Salary Growth": salary_df["salary_growth"],
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"]
})

# Streamlit UI
st.title("Correlation Between Salary Growth and Categories Over Years")

# Select category
category = st.selectbox("Select category to compare with salary growth:", ["Basket Growth", "Rent Growth", "Fuel Growth"])

# Calculate correlation for each year
growth_data["Same Trend"] = (growth_data["Salary Growth"] > 0) & (growth_data[category] > 0) | \
                            (growth_data["Salary Growth"] < 0) & (growth_data[category] < 0)

# Plot points
fig, ax = plt.subplots(figsize=(10, 6))
for i, row in growth_data.iterrows():
    color = "green" if row["Same Trend"] else "red"
    ax.scatter(row["Year"], 0, color=color, s=100)
ax.set_yticks([])
ax.set_xlabel("Year")
ax.set_title(f"Trend Alignment Between Salary Growth and {category}")
ax.axhline(0, color="black", linewidth=0.5)
plt.grid(axis="x", linestyle="--", alpha=0.6)
st.pyplot(fig)
