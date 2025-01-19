import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# טעינת הנתונים
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, salary_df, rent_df, fuel_df

basket_df, salary_df, rent_df, fuel_df = load_data()

# חישוב התרומה היחסית

def calculate_relative_contribution(basket, rent, fuel):
    total_cost = basket["price for basic basket"] + rent["price for month"] + fuel["price per liter"]
    basket["relative_contribution"] = basket["price for basic basket"] / total_cost * 100
    rent["relative_contribution"] = rent["price for month"] / total_cost * 100
    fuel["relative_contribution"] = fuel["price per liter"] / total_cost * 100
    return basket, rent, fuel

basket_df, rent_df, fuel_df = calculate_relative_contribution(basket_df, rent_df, fuel_df)

# הכנת נתונים עבור גרף האזור המוערם
def prepare_stacked_area_data(basket, rent, fuel):
    data = pd.DataFrame({
        "Year": basket["year"],
        "Basket": basket["relative_contribution"],
        "Rent": rent["relative_contribution"],
        "Fuel": fuel["relative_contribution"]
    })
    return data

stacked_area_data = prepare_stacked_area_data(basket_df, rent_df, fuel_df)

# ממשק Streamlit
st.title("Relative Contribution to Cost of Living")

# בחירת טווח שנים
start_year, end_year = st.slider(
    "Select Year Range:",
    int(stacked_area_data["Year"].min()),
    int(stacked_area_data["Year"].max()),
    (int(stacked_area_data["Year"].min()), int(stacked_area_data["Year"].max()))
)

filtered_data = stacked_area_data[(stacked_area_data["Year"] >= start_year) & (stacked_area_data["Year"] <= end_year)]

# יצירת גרף אזור מוערם
fig, ax = plt.subplots(figsize=(10, 6))
ax.stackplot(
    filtered_data["Year"],
    filtered_data["Basket"],
    filtered_data["Rent"],
    filtered_data["Fuel"],
    labels=["Basket", "Rent", "Fuel"],
    alpha=0.8
)
ax.set_title("Stacked Area Chart: Contribution to Cost of Living")
ax.set_xlabel("Year")
ax.set_ylabel("Relative Contribution (%)")
ax.legend(loc="upper left")
ax.grid(True)

# הצגת הגרף
st.pyplot(fig)
