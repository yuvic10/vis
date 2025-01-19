import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# URLs של קבצי ה-Excel
basket_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/basic_basket.xlsx"
salary_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/salary.xlsx"
rent_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/rent.xlsx"
fuel_file_url = "https://raw.githubusercontent.com/yuvic10/vis/main/fuel.xlsx"

# כותרת האפליקציה
st.title("Real vs Simulated Prices Line Chart")

try:
    # קריאת נתוני הסל הבסיסי
    basket_data = pd.read_excel(basket_file_url, engine="openpyxl")
    basket_data["price for basic basket"] = basket_data["price for basic basket"].round(3)

    # קריאת נתוני המשכורות
    salary_data = pd.read_excel(salary_file_url, engine="openpyxl")

    # קריאת נתוני השכירות (מתוך Sheet 2)
    rent_data = pd.read_excel(rent_file_url, engine="openpyxl", sheet_name="Sheet2")

    # קריאת נתוני הדלק
    fuel_data = pd.read_excel(fuel_file_url, engine="openpyxl")
    fuel_data["price per liter"] = fuel_data["price per liter"].round(3)

    # חישוב אחוזי השינוי במשכורות
    salary_data["growth rate"] = salary_data["salary"].pct_change().fillna(0)

    # יישום השינוי על הנתונים האחרים
    basket_data["simulated price for basket"] = basket_data["price for basic basket"].iloc[0] * (
        1 + salary_data["growth rate"].cumsum()
    )
    rent_data["simulated price for month"] = rent_data["price for month"].iloc[0] * (
        1 + salary_data["growth rate"].cumsum()
    )
    fuel_data["simulated price per liter"] = fuel_data["price per liter"].iloc[0] * (
        1 + salary_data["growth rate"].cumsum()
    )

    # מיזוג הנתונים ליצירת גרף קווי
    line_chart_data = pd.DataFrame({
        "Year": basket_data["year"],
        "Real Basket Price": basket_data["price for basic basket"],
        "Simulated Basket Price": basket_data["simulated price for basket"],
        "Real Rent Price": rent_data["price for month"],
        "Simulated Rent Price": rent_data["simulated price for month"],
        "Real Fuel Price": fuel_data["price per liter"],
        "Simulated Fuel Price": fuel_data["simulated price per liter"],
    })

    # יצירת ממשק לבחירת נתונים להצגה
    st.write("### Select Data to Display")
    options = list(line_chart_data.columns[1:])
    selected_options = st.multiselect("Select data to include in the line chart:", options, default=options)

    # הצגת גרף קווי
    if selected_options:
        st.write("### Line Chart of Real vs Simulated Prices")
        plt.figure(figsize=(12, 6))
        for option in selected_options:
            plt.plot(line_chart_data["Year"], line_chart_data[option], label=option)
        plt.xlabel("Year")
        plt.ylabel("Price")
        plt.title("Real vs Simulated Prices Over Time")
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.warning("Please select at least one data series to display.")

except Exception as e:
    st.error(f"An error occurred: {e}")
