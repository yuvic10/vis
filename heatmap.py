import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"

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

# Combine data for Sankey diagram
sankey_data = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket": basket_df["basket_percentage"],
    "Rent": rent_df["rent_percentage"],
    "Fuel": fuel_df["fuel_percentage"]
})

# Streamlit UI
st.title("Sankey Diagram: Percentage of Salary by Categories Over Time")

# Sort years chronologically
selected_years = sorted(st.multiselect("Select years to display:", sankey_data["Year"].unique(), default=sankey_data["Year"].unique()[:3]))
selected_categories = st.multiselect("Select categories to display:", ["Basket", "Rent", "Fuel"], default=["Basket", "Rent"])

# Filter data
filtered_data = sankey_data[sankey_data["Year"].isin(selected_years)]

# Create Sankey diagram inputs
labels = ["Salary"] + [f"{category} ({year})" for year in selected_years for category in selected_categories]
sources = []
targets = []
values = []

for year in selected_years:
    for category in selected_categories:
        sources.append(0)  # Salary is the source
        targets.append(labels.index(f"{category} ({year})"))
        category_values = filtered_data.loc[filtered_data["Year"] == year, category].values
        if len(category_values) > 0:
            values.append(category_values[0])  # Use the exact percentage value

# Scale values to improve visibility in Sankey
max_value = max(values)
scaled_values = [value / max_value for value in values]  # Scale values proportionally

# Create Sankey diagram
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color="lightblue"
    ),
    link=dict(
        source=sources,
        target=targets,
        value=scaled_values,  # Use scaled values here
        color="gray"
    )
))

fig.update_layout(
    title_text="Sankey Diagram: Salary Breakdown by Categories Over Time",
    font_size=10
)

st.plotly_chart(fig)
