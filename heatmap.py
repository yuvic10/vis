import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

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

# איסוף הנתונים לנורמליזציה
data = pd.DataFrame({
    "year": salary_df["year"],
    "Basket Units": basket_df["basket_units"],
    "Rent Months": rent_df["rent_months"],
    "Fuel Liters": fuel_df["fuel_liters"]
})

# נורמליזציה
scaler = MinMaxScaler()
data_normalized = pd.DataFrame(scaler.fit_transform(data.iloc[:, 1:]), columns=data.columns[1:])
data_normalized.insert(0, "Year", data["year"])

# ממשק Streamlit
st.title("Normalized Purchasing Power Analysis")
st.sidebar.title("Select Categories")

# בחירת קטגוריות
categories = st.sidebar.multiselect(
    "Select categories to display:",
    options=["Basket Units", "Rent Months", "Fuel Liters"],
    default=["Basket Units", "Rent Months", "Fuel Liters"]
)

# גרף
fig, ax = plt.subplots(figsize=(10, 6))
for category in categories:
    ax.plot(data_normalized["Year"], data_normalized[category], label=category, marker='o')

ax.set_title("Normalized Purchasing Power Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("Normalized Units (0-1)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# תובנות
st.subheader("Insights")
st.write("The graph shows normalized purchasing power for each category, allowing for direct comparison between them, regardless of scale differences.")
