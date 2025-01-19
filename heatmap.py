import streamlit as st
import pandas as pd
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
    rent_df = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")
    fuel_df = pd.read_excel(fuel_file_url, engine="openpyxl")
    return basket_df, rent_df, fuel_df

basket_df, rent_df, fuel_df = load_data()

# פונקציה לחישוב תנודתיות (סטיית תקן)
def calculate_volatility(data, column):
    return data[column].rolling(window=2).std()

# חישוב תנודתיות עבור כל קטגוריה
basket_volatility = calculate_volatility(basket_df, "price for basic basket")
rent_volatility = calculate_volatility(rent_df, "price for month")
fuel_volatility = calculate_volatility(fuel_df, "price per liter")

# יצירת DataFrame לסטיית התקן
volatility_df = pd.DataFrame({
    "Year": basket_df["year"],
    "Basket Volatility": basket_volatility,
    "Rent Volatility": rent_volatility,
    "Fuel Volatility": fuel_volatility
}).dropna()

# ממשק Streamlit
st.title("Volatility Heatmap by Category")

# בחירת שנים להצגה
start_year, end_year = st.slider(
    "Select Year Range:",
    int(volatility_df["Year"].min()),
    int(volatility_df["Year"].max()),
    (int(volatility_df["Year"].min()), int(volatility_df["Year"].max()))
)

# סינון נתונים לפי שנים
filtered_volatility = volatility_df[(volatility_df["Year"] >= start_year) & (volatility_df["Year"] <= end_year)]

# יצירת Heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(
    filtered_volatility.set_index("Year").transpose(),
    annot=True, fmt=".2f", cmap="coolwarm", cbar=True
)
plt.title("Volatility Heatmap by Category")
plt.xlabel("Year")
plt.ylabel("Category")

# הצגת Heatmap
st.pyplot(plt)
