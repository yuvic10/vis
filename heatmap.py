import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# URLs של קבצי הנתונים
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"
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
st.title("Purchasing Power Analysis Without Normalization")
st.sidebar.title("Filters")

# בחירת קטגוריות להצגה
categories = st.sidebar.multiselect(
    "Select categories to display:",
    options=["basket_units", "rent_months", "fuel_liters"],
    default=["basket_units", "rent_months", "fuel_liters"]
)

# בחירת שנים להצגה
start_year, end_year = st.sidebar.slider(
    "Select Year Range:",
    int(salary_df["year"].min()),
    int(salary_df["year"].max()),
    (int(salary_df["year"].min()), int(salary_df["year"].max()))
)

# סינון נתונים לפי שנים
filtered_salary = salary_df[(salary_df["year"] >= start_year) & (salary_df["year"] <= end_year)]
filtered_basket = basket_df[(basket_df["year"] >= start_year) & (basket_df["year"] <= end_year)]
filtered_rent = rent_df[(rent_df["year"] >= start_year) & (rent_df["year"] <= end_year)]
filtered_fuel = fuel_df[(fuel_df["year"] >= start_year) & (fuel_df["year"] <= end_year)]

# הכנה לשרטוט הנתונים
data_to_plot = pd.DataFrame({"Year": filtered_salary["year"]})
if "basket_units" in categories:
    data_to_plot["Basket Units"] = filtered_basket["basket_units"]
if "rent_months" in categories:
    data_to_plot["Rent Months"] = filtered_rent["rent_months"]
if "fuel_liters" in categories:
    data_to_plot["Fuel Liters"] = filtered_fuel["fuel_liters"]

# גרף קווי להצגת הנתונים
fig, ax = plt.subplots(figsize=(10, 6))
for column in data_to_plot.columns[1:]:
    ax.plot(data_to_plot["Year"], data_to_plot[column], marker="o", label=column)
ax.set_title("Purchasing Power Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Units Affordable")
ax.legend()
ax.grid(True)

# הצגת הגרף
st.pyplot(fig)

# הצגת תובנות
st.subheader("Insights")
st.write("""
This graph displays the purchasing power over time without applying normalization. Each category reflects its actual units affordable based on the given salaries and prices.
""")
