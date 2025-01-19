import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# קישורים לנתוני ה-Excel
basket_url = "https://github.com/yuvic10/vis/blob/main/basic_basket.xlsx?raw=true"
rent_url = "https://github.com/yuvic10/vis/blob/main/rent.xlsx?raw=true"
fuel_url = "https://github.com/yuvic10/vis/blob/main/fuel.xlsx?raw=true"
salary_url = "https://github.com/yuvic10/vis/blob/main/salary.xlsx?raw=true"

# קריאת הנתונים
basket_data = pd.read_excel(basket_url, engine="openpyxl")
rent_data = pd.read_excel(rent_url, engine="openpyxl")
fuel_data = pd.read_excel(fuel_url, engine="openpyxl")
salary_data = pd.read_excel(salary_url, engine="openpyxl")

# עיגול ערכים לשלוש ספרות אחרי הנקודה
basket_data["price for basic basket"] = basket_data["price for basic basket"].round(3)
fuel_data["price per liter"] = fuel_data["price per liter"].round(3)

# חישוב אחוז גדילה במשכורות
salary_data["growth_rate"] = salary_data["salary"].pct_change() * 100
salary_data["growth_rate"] = salary_data["growth_rate"].fillna(0).round(2)

# חישוב מחירים מדומים לכל מוצר בהתבסס על אחוז הגדילה במשכורות
basket_data["simulated price"] = basket_data["price for basic basket"]
rent_data["simulated price for month"] = rent_data["price for month"]
fuel_data["simulated price per liter"] = fuel_data["price per liter"]

for year in range(1, len(salary_data)):
    growth_rate = salary_data.iloc[year]["growth_rate"] / 100 + 1
    basket_data.loc[year, "simulated price"] = basket_data.loc[year - 1, "simulated price"] * growth_rate
    rent_data.loc[year, "simulated price for month"] = rent_data.loc[year - 1, "simulated price for month"] * growth_rate
    fuel_data.loc[year, "simulated price per liter"] = fuel_data.loc[year - 1, "simulated price per liter"] * growth_rate

# הצגת כותרת האפליקציה
st.title("Real vs Simulated Prices Comparison (2015-2024)")

# הצגת טבלאות
st.subheader("Basic Basket Prices")
st.dataframe(basket_data)

st.subheader("Rent Prices")
st.dataframe(rent_data)

st.subheader("Fuel Prices")
st.dataframe(fuel_data)

st.subheader("Salaries and Growth Rates")
st.dataframe(salary_data)

# יצירת Heatmap של ההבדלים בין מחירים אמיתיים למדומים
heatmap_data = pd.DataFrame({
    "Year": basket_data["year"],
    "Basic Basket Difference": basket_data["simulated price"] - basket_data["price for basic basket"],
    "Rent Difference": rent_data["simulated price for month"] - rent_data["price for month"],
    "Fuel Difference": fuel_data["simulated price per liter"] - fuel_data["price per liter"]
}).set_index("Year")

st.subheader("Heatmap of Real vs Simulated Prices")
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", fmt=".2f")
st.pyplot(plt)
