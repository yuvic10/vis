import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"

# Load the data
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df, salary_df

basket_df, rent_df, fuel_df, salary_df = load_data()

# Calculate percentage of salary for each category
def calculate_percentage_of_salary(category_price, salary):
    return (category_price / salary) * 100

basket_df["basket_percentage"] = calculate_percentage_of_salary(basket_df["price for basic basket"], salary_df["salary"])
rent_df["rent_percentage"] = calculate_percentage_of_salary(rent_df["price for month"], salary_df["salary"])
fuel_df["fuel_percentage"] = calculate_percentage_of_salary(fuel_df["price per liter"], salary_df["salary"])

# Combine data into a single DataFrame
combined_data = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"]
})

# Streamlit UI
st.title("Pie Charts: Percentage of Salary Spent on Each Category")

# Select year
selected_year = st.selectbox("Select a year:", combined_data["Year"])

# Filter data for the selected year
year_data = combined_data[combined_data["Year"] == selected_year].iloc[0]
categories = ["Basket", "Rent", "Fuel"]
values = [year_data["Basket"], year_data["Rent"], year_data["Fuel"]]

# Create pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    values,
    labels=categories,
    autopct="%1.1f%%",
    startangle=90,
    colors=["skyblue", "salmon", "lightgreen"],
    wedgeprops={"edgecolor": "black"}
)
ax.set_title(f"Percentage of Salary Spent in {selected_year}", fontsize=14)

# Display the chart
st.pyplot(fig)
