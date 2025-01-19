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

# חישוב כוח הקנייה
def calculate_purchasing_power(salary_df, basket_df, rent_df, fuel_df):
    result = pd.DataFrame({"year": salary_df["year"]})
    result["basket_units"] = salary_df["salary"] / basket_df["price for basic basket"]
    result["rent_months"] = salary_df["salary"] / rent_df["price for month"]
    result["fuel_liters"] = salary_df["salary"] / fuel_df["price per liter"]
    return result

purchasing_power_df = calculate_purchasing_power(salary_df, basket_df, rent_df, fuel_df)

# בחירת קטגוריות להצגה
categories = st.multiselect(
    "Select categories to display:",
    options=["basket_units", "rent_months", "fuel_liters"],
    default=["basket_units", "rent_months", "fuel_liters"]
)

# הצגת הגרף
if categories:
    fig, ax = plt.subplots(figsize=(10, 6))
    for category in categories:
        ax.plot(purchasing_power_df["year"], purchasing_power_df[category], marker='o', label=category.replace("_", " ").title())
    ax.set_title("Purchasing Power Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Units Affordable")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.warning("Please select at least one category to display.")
