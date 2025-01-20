import streamlit as st
import pandas as pd
import plotly.express as px

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"
sd
# Load the data
@st.cache_data
def load_data():
    basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df, salary_df

basket_df, rent_df, fuel_df, salary_df = load_data()

# Adjust data: multiply fuel by 100 and basket by 4
basket_df["price for basic basket"] *= 4  # Assuming 4 baskets per month
fuel_df["price per liter"] *= 100        # Assuming 100 liters per month

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

# Fill missing years with NaN values
all_years = pd.DataFrame({"Year": range(combined_data["Year"].min(), combined_data["Year"].max() + 1)})
combined_data = pd.merge(all_years, combined_data, on="Year", how="left")

# Streamlit UI
st.title("Ribbon Chart: Salary Percentage by Category Over Time")

# Select category
selected_category = st.selectbox("Choose a category:", ["Basket", "Rent", "Fuel"])

# Prepare data for selected category
selected_data = combined_data[["Year", selected_category]].rename(columns={selected_category: "Percentage"})

# Calculate the min and max for a smaller Y-axis range
min_y = selected_data["Percentage"].min() * 0.9 if not selected_data["Percentage"].isnull().all() else 0
max_y = selected_data["Percentage"].max() * 1.1 if not selected_data["Percentage"].isnull().all() else 1

# Create Ribbon Chart
fig = px.area(
    selected_data,
    x="Year",
    y="Percentage",
    title=f"{selected_category} Percentage of Salary Over Time",
    labels={"Percentage": "Percentage of Salary (%)", "Year": "Year"},
    color_discrete_sequence=["teal"]
)

fig.update_layout(
    xaxis=dict(title="Year", dtick=1, showgrid=False),  # Show all years with dtick=1
    yaxis=dict(title="Percentage of Salary (%)", range=[min_y, max_y], showgrid=True),
    plot_bgcolor="white",
    title=dict(x=0.5),  # Center the title
)

# Display the chart
st.plotly_chart(fig)
