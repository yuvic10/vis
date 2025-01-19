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
st.title("Interactive Pie Chart: Percentage of Salary Spent")

# Select years
selected_years = st.multiselect("Select years to include:", combined_data["Year"].unique(), default=combined_data["Year"].unique())

# Select categories to display
category_options = ["Basket", "Rent", "Fuel"]
selected_categories = st.multiselect("Select categories to include:", category_options, default=category_options)

# Filter data for the selected years and categories
filtered_data = combined_data[combined_data["Year"].isin(selected_years)]

# Calculate the average percentage for the selected years
average_values = filtered_data[selected_categories].mean()

# Create pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    average_values,
    labels=selected_categories,
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Set3.colors  # Using a color map for better visuals
)
ax.set_title(f"Average Percentage of Salary Spent ({', '.join(map(str, selected_years))})", fontsize=14)

# Display the chart
st.pyplot(fig)
