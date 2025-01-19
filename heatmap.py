import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
streamgraph_data = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"],
})

# Streamlit UI
st.title("Streamgraph: Percentage of Salary Spent on Selected Category Over Time")

# Dropdown menu to select a category
category = st.selectbox(
    "Select a Category:",
    options=["Basket", "Rent", "Fuel"]
)

# Create Streamgraph for the selected category
fig = go.Figure()

# Add trace for the selected category
fig.add_trace(go.Scatter(
    x=streamgraph_data["Year"], 
    y=streamgraph_data[category], 
    mode='lines',
    stackgroup='one', 
    name=category
))

# Customize the layout
fig.update_layout(
    title=f"Percentage of Salary Spent on {category} Over Time",
    xaxis_title="Year",
    yaxis_title="Percentage of Salary (%)",
    legend_title="Category",
    template="plotly_white"
)

# Display the Streamgraph
st.plotly_chart(fig)
