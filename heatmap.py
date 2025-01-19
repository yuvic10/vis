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

# חישוב כושר הקנייה
def calculate_buying_power(salary_df, basket_df, rent_df, fuel_df):
    combined_df = pd.DataFrame()
    combined_df["year"] = salary_df["year"]
    combined_df["salary"] = salary_df["salary"]
    combined_df["basket_ratio"] = salary_df["salary"] / basket_df["price for basic basket"]
    combined_df["rent_ratio"] = salary_df["salary"] / rent_df["price for month"]
    combined_df["fuel_ratio"] = salary_df["salary"] / fuel_df["price per liter"]
    return combined_df

buying_power_df = calculate_buying_power(salary_df, basket_df, rent_df, fuel_df)

# ממשק Streamlit
st.title("Can Salaries Keep Up with the Cost of Living?")
st.sidebar.title("Filters")

# בחירת שנים להצגה
start_year, end_year = st.sidebar.slider(
    "Select Year Range:",
    int(buying_power_df["year"].min()),
    int(buying_power_df["year"].max()),
    (int(buying_power_df["year"].min()), int(buying_power_df["year"].max()))
)

# סינון נתונים לפי שנים
filtered_data = buying_power_df[(buying_power_df["year"] >= start_year) & (buying_power_df["year"] <= end_year)]

# גרף כושר הקנייה
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(filtered_data["year"], filtered_data["basket_ratio"], label="Buying Power: Basket", marker='o', color='orange')
ax.plot(filtered_data["year"], filtered_data["rent_ratio"], label="Buying Power: Rent", marker='o', color='green')
ax.plot(filtered_data["year"], filtered_data["fuel_ratio"], label="Buying Power: Fuel", marker='o', color='red')
ax.set_title("Buying Power Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Buying Power (Salary / Cost)")
ax.legend()
ax.grid(True)

# הצגת הגרף
st.pyplot(fig)

# מסקנות
st.write("### Conclusions")
st.write("""
This graph demonstrates whether salaries are keeping up with the cost of living. 
If the buying power decreases over time, it indicates that the cost of living is outpacing salary growth.
""")
