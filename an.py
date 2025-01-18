import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# נתוני מחירים (לדוגמה)
product_data = {
    "year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "product_price": [100, 110, 120, 125, 130, 140, 150, 160, 170]
}

rent_data = {
    "year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "rent_price": [4500, 4700, 4800, 4900, 5000, 5100, 5200, 5300, 5400]
}

# יצירת DataFrame אחוד
product_df = pd.DataFrame(product_data)
rent_df = pd.DataFrame(rent_data)

merged_df = pd.merge(product_df, rent_df, on="year")

# מחשבים את המחירים המדומים על פי קצב עליית השכר
st.title("Comparison of Real vs. Projected Prices")
wage_growth = st.slider("Select Wage Growth Rate (%)", min_value=0, max_value=10, value=2)

# חישוב מחירים מדומים
merged_df["projected_product_price"] = merged_df["product_price"] * (1 + wage_growth / 100) ** (merged_df["year"] - merged_df["year"].min())
merged_df["projected_rent_price"] = merged_df["rent_price"] * (1 + wage_growth / 100) ** (merged_df["year"] - merged_df["year"].min())

# תצוגת נתונים
st.dataframe(merged_df)

# ויזואליזציה
st.subheader("Product Prices Over Time")
plt.figure(figsize=(10, 6))
plt.plot(merged_df["year"], merged_df["product_price"], label="Real Product Price", marker="o")
plt.plot(merged_df["year"], merged_df["projected_product_price"], label="Projected Product Price", linestyle="--", marker="o")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Price")
plt.title("Real vs. Projected Product Prices")
st.pyplot(plt)

st.subheader("Rent Prices Over Time")
plt.figure(figsize=(10, 6))
plt.plot(merged_df["year"], merged_df["rent_price"], label="Real Rent Price", marker="o")
plt.plot(merged_df["year"], merged_df["projected_rent_price"], label="Projected Rent Price", linestyle="--", marker="o")
plt.legend()
plt.xlabel("Year")
plt.ylabel("Rent Price")
plt.title("Real vs. Projected Rent Prices")
st.pyplot(plt)
