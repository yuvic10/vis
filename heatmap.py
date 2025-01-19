import streamlit as st
import pandas as pd
import plotly.express as px

# URLs of the datasets
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary1.xlsx"

# Load the data
@st.cache_data
def load_data():
    try:
        basket_df = pd.read_excel(basket_file_url, engine="openpyxl")
        rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
        fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
        salary_df = pd.read_excel(salary_file_url, engine="openpyxl")
        return basket_df, rent_df, fuel_df, salary_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

basket_df, rent_df, fuel_df, salary_df = load_data()

# Validate data
if basket_df is not None and rent_df is not None and fuel_df is not None and salary_df is not None:
    try:
        # Calculate percentage of salary for each category
        def calculate_percentage_of_salary(category_price, salary):
            if len(category_price) != len(salary):
                raise ValueError("Mismatch in lengths of category prices and salaries.")
            return (category_price / salary) * 100

        basket_df["basket_percentage"] = calculate_percentage_of_salary(basket_df["price for basic basket"], salary_df["salary"])
        rent_df["rent_percentage"] = calculate_percentage_of_salary(rent_df["price for month"], salary_df["salary"])
        fuel_df["fuel_percentage"] = calculate_percentage_of_salary(fuel_df["price per liter"], salary_df["salary"])

        # Combine data into a single DataFrame
        basket_data = pd.DataFrame({"Year": basket_df["year"], "Percentage": basket_df["basket_percentage"], "Category": "Basket"})
        rent_data = pd.DataFrame({"Year": rent_df["year"], "Percentage": rent_df["rent_percentage"], "Category": "Rent"})
        fuel_data = pd.DataFrame({"Year": fuel_df["year"], "Percentage": fuel_df["fuel_percentage"], "Category": "Fuel"})
        combined_data = pd.concat([basket_data, rent_data, fuel_data], ignore_index=True)

        # Streamlit UI
        st.title("Sunburst Chart: Percentage of Salary Spent on Categories")

        # Add category selection
        selected_category = st.selectbox("Select a category:", ["Basket", "Rent", "Fuel"])
        
        # Filter data by selected category
        filtered_data = combined_data[combined_data["Category"] == selected_category]

        # Create and display Sunburst chart
        fig = px.sunburst(
            filtered_data,
            path=["Category", "Year"],
            values="Percentage",
            title=f"Percentage of Salary Spent on {selected_category} Over Time",
            color="Percentage",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error processing data: {e}")
else:
    st.warning("One or more datasets could not be loaded. Please check the file URLs.")
