import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# חישוב שיעור הגדילה לכל קטגוריה
def calculate_growth_rate(data, column):
    return data[column].pct_change().fillna(0) * 100

basket_df["basket_growth"] = calculate_growth_rate(basket_df, "price for basic basket")
rent_df["rent_growth"] = calculate_growth_rate(rent_df, "price for month")
fuel_df["fuel_growth"] = calculate_growth_rate(fuel_df, "price per liter")

# חישוב התרומה של כל קטגוריה לשינוי הכולל
combined_growth = basket_df[["year", "basket_growth"]].copy()
combined_growth["rent_growth"] = rent_df["rent_growth"]
combined_growth["fuel_growth"] = fuel_df["fuel_growth"]

combined_growth["total_growth"] = (
    combined_growth["basket_growth"]
    + combined_growth["rent_growth"]
    + combined_growth["fuel_growth"]
)

combined_growth["basket_contribution"] = (combined_growth["basket_growth"] / combined_growth["total_growth"]) * 100
combined_growth["rent_contribution"] = (combined_growth["rent_growth"] / combined_growth["total_growth"]) * 100
combined_growth["fuel_contribution"] = (combined_growth["fuel_growth"] / combined_growth["total_growth"]) * 100

# ממשק Streamlit
st.title("Category Contribution to Cost of Living Over Time")

# בחירת שנים להצגה
start_year, end_year = st.slider(
    "Select Year Range:",
    int(combined_growth["year"].min()),
    int(combined_growth["year"].max()),
    (int(combined_growth["year"].min()), int(combined_growth["year"].max()))
)

filtered_data = combined_growth[
    (combined_growth["year"] >= start_year) & (combined_growth["year"] <= end_year)
]

# Heatmap של תרומת הקטגוריות
st.write("### Contribution Heatmap")
plt.figure(figsize=(10, 6))
sns.heatmap(
    filtered_data[["basket_contribution", "rent_contribution", "fuel_contribution"]].transpose(),
    annot=True,
    fmt=".1f",
    cmap="coolwarm",
    xticklabels=filtered_data["year"],
    yticklabels=["Basket", "Rent", "Fuel"]
)
st.pyplot(plt)
