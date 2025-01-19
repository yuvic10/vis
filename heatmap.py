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
basket_df["basket_units"] = salary_df["salary"] / basket_df["price for basic basket"]
rent_df["rent_months"] = salary_df["salary"] / rent_df["price for month"]
fuel_df["fuel_liters"] = salary_df["salary"] / fuel_df["price per liter"]

# ממשק Streamlit
st.title("Purchasing Power Analysis")
st.sidebar.title("Select Categories to Display")

# בחירת קטגוריות להצגה
categories = st.sidebar.multiselect(
    "Select categories to display:",
    options=["basket_units", "rent_months", "fuel_liters"],
    default=["basket_units", "rent_months", "fuel_liters"]
)

# סינון נתונים לפי שנים
start_year, end_year = st.sidebar.slider(
    "Select Year Range:",
    int(salary_df["year"].min()),
    int(salary_df["year"].max()),
    (int(salary_df["year"].min()), int(salary_df["year"].max()))
)

filtered_basket = basket_df[(basket_df["year"] >= start_year) & (basket_df["year"] <= end_year)]
filtered_rent = rent_df[(rent_df["year"] >= start_year) & (rent_df["year"] <= end_year)]
filtered_fuel = fuel_df[(fuel_df["year"] >= start_year) & (fuel_df["year"] <= end_year)]

# גרף השוואתי
fig, ax = plt.subplots(figsize=(10, 6))

if "basket_units" in categories:
    ax.plot(filtered_basket["year"], filtered_basket["basket_units"], label="Basket Units", marker='o', color='blue')
if "rent_months" in categories:
    ax.plot(filtered_rent["year"], filtered_rent["rent_months"], label="Rent Months", marker='o', color='orange')
if "fuel_liters" in categories:
    ax.plot(filtered_fuel["year"], filtered_fuel["fuel_liters"], label="Fuel Liters", marker='o', color='green')

ax.set_title("Purchasing Power Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Units Affordable")
ax.legend()
ax.grid(True)

# הצגת הגרף
st.pyplot(fig)

# הסבר מילולי
st.write("### Insights")
st.write(
    "This graph shows how many units of each category (basket, rent, fuel) can be purchased with the monthly salary over time. "
    "It helps to understand which category contributes more to the erosion of purchasing power and how affordability changes over the years."
)
