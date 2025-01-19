import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    salary_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx")
    basket_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx")
    rent_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx", sheet_name="Sheet2")
    fuel_df = pd.read_excel("https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx")
    return salary_df, basket_df, rent_df, fuel_df

salary_df, basket_df, rent_df, fuel_df = load_data()

# Normalize the expenses as percentages of salary
def calculate_optimal_allocation(salary_df, basket_df, rent_df, fuel_df, basket_pct, rent_pct, fuel_pct):
    merged_df = pd.merge(salary_df, basket_df, on="year")
    merged_df = pd.merge(merged_df, rent_df, on="year")
    merged_df = pd.merge(merged_df, fuel_df, on="year")
    
    merged_df["Basket Actual (%)"] = (merged_df["price for basic basket"] / merged_df["salary"]) * 100
    merged_df["Rent Actual (%)"] = (merged_df["price for month"] / merged_df["salary"]) * 100
    merged_df["Fuel Actual (%)"] = (merged_df["price per liter"] * 100 / merged_df["salary"]) * 100
    
    merged_df["Basket Optimal (%)"] = basket_pct
    merged_df["Rent Optimal (%)"] = rent_pct
    merged_df["Fuel Optimal (%)"] = fuel_pct
    
    return merged_df

# User inputs for optimal allocation
st.sidebar.title("Set Optimal Allocation Percentages")
basket_pct = st.sidebar.slider("Basket (%)", 0, 100, 30)
rent_pct = st.sidebar.slider("Rent (%)", 0, 100, 40)
fuel_pct = st.sidebar.slider("Fuel (%)", 0, 100, 30)

# Ensure the percentages sum up to 100
if basket_pct + rent_pct + fuel_pct != 100:
    st.error("The total percentage must equal 100!")
else:
    allocation_df = calculate_optimal_allocation(salary_df, basket_df, rent_df, fuel_df, basket_pct, rent_pct, fuel_pct)
    
    # Stacked Area Chart
    st.title("Optimal vs Actual Allocation Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.stackplot(
        allocation_df["year"],
        allocation_df["Basket Actual (%)"],
        allocation_df["Rent Actual (%)"],
        allocation_df["Fuel Actual (%)"],
        labels=["Basket (Actual)", "Rent (Actual)", "Fuel (Actual)"]
    )
    ax.plot(allocation_df["year"], allocation_df["Basket Optimal (%)"], label="Basket (Optimal)", color="blue", linestyle="--")
    ax.plot(allocation_df["year"], allocation_df["Rent Optimal (%)"], label="Rent (Optimal)", color="orange", linestyle="--")
    ax.plot(allocation_df["year"], allocation_df["Fuel Optimal (%)"], label="Fuel (Optimal)", color="green", linestyle="--")
    
    ax.set_title("Actual vs Optimal Allocation")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percentage of Salary (%)")
    ax.legend()
    st.pyplot(fig)
