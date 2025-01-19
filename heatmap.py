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
st.title("Percentage of Salary Spent on Each Category Per Year")

# Plot grouped bar chart
fig, ax = plt.subplots(figsize=(10, 6))
width = 0.25  # Bar width
x = combined_data["Year"]

ax.bar(x - width, combined_data["Basket"], width=width, label="Basket", color="skyblue")
ax.bar(x, combined_data["Rent"], width=width, label="Rent", color="salmon")
ax.bar(x + width, combined_data["Fuel"], width=width, label="Fuel", color="lightgreen")

ax.set_title("Percentage of Salary Spent on Each Category Over Time", fontsize=14)
ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel("Percentage of Salary (%)", fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(x, rotation=45, fontsize=10)
ax.legend(title="Categories", fontsize=10)
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Display the plot in Streamlit
st.pyplot(fig)
