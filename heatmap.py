import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
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

# חישוב אחוזי שינוי לכל קטגוריה
basket_df["basket_growth"] = basket_df["price for basic basket"].pct_change() * 100
rent_df["rent_growth"] = rent_df["price for month"].pct_change() * 100
fuel_df["fuel_growth"] = fuel_df["price per liter"].pct_change() * 100
salary_df["salary_growth"] = salary_df["salary"].pct_change() * 100

# יצירת DataFrame עבור הקורלציות
merged_df = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket Growth": basket_df["basket_growth"],
    "Rent Growth": rent_df["rent_growth"],
    "Fuel Growth": fuel_df["fuel_growth"],
    "Salary Growth": salary_df["salary_growth"]
}).dropna()

correlation_matrix = merged_df.drop(columns=["Year"]).corr()

# ממשק Streamlit
st.title("Correlation Analysis of Economic Categories")

# הצגת Heatmap של הקורלציות
st.write("### Heatmap of Correlations Between Categories")
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
st.pyplot(plt)

# בחירת קטגוריות להשוואה פרטנית
st.sidebar.title("Scatter Plot Selection")
category_x = st.sidebar.selectbox("Select X-axis category:", correlation_matrix.columns)
category_y = st.sidebar.selectbox("Select Y-axis category:", correlation_matrix.columns)

# הצגת Scatter Plot
st.write(f"### Scatter Plot: {category_x} vs {category_y}")
plt.figure(figsize=(8, 6))
sns.scatterplot(data=merged_df, x=category_x, y=category_y, hue="Year", palette="viridis", s=100)
plt.title(f"{category_x} vs {category_y} Over Time")
plt.xlabel(category_x)
plt.ylabel(category_y)
st.pyplot(plt)
