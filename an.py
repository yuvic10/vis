import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני דוגמה
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
salary = [5000, 5100, 5200, 5300, 5400, 5500, 5600]  # משכורת חודשית

products = {
    "Flour": [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
    "Milk": [5.0, 5.8, 6.6, 7.5, 8.5, 9.5, 10.5],
    "Eggs": [10.0, 11.5, 13.0, 14.5, 16.0, 17.5, 19.0],
    "Cheese": [15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0],
}

# חישוב משכורת שנתית
annual_salaries = [sal * 12 for sal in salary]

# ממשק Streamlit
st.title("Interactive Shopping Basket Over the Years")
st.write("Select products to see their cumulative effect on basket cost and salary percentage.")

# בחירת מוצרים
selected_products = st.multiselect(
    "Select products to add to the basket:",
    options=list(products.keys()),
    default=[]
)

# חישוב סל קניות
if selected_products:
    basket_prices = [sum([products[prod][i] for prod in selected_products]) for i in range(len(years))]
    annual_basket_prices = [price * 4 * 12 for price in basket_prices]  # עלות שנתית
    percentage_of_salary = [round((basket / salary) * 100, 2) for basket, salary in zip(annual_basket_prices, annual_salaries)]

    # יצירת DataFrame
    data = pd.DataFrame({
        "Year": years,
        "Annual Basket Price": annual_basket_prices,
        "Annual Salary": annual_salaries,
        "Percentage of Salary": percentage_of_salary
    })

    # גרף מגמה
    st.subheader("Trend: Annual Basket Cost vs Salary")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data["Year"], data["Annual Basket Price"], marker="o", label="Basket Price", color="blue")
    ax.plot(data["Year"], data["Annual Salary"], marker="o", label="Salary", color="green")
    ax.fill_between(data["Year"], data["Annual Basket Price"], data["Annual Salary"], where=(data["Annual Basket Price"] <= data["Annual Salary"]), interpolate=True, color='lightgreen', alpha=0.5, label="Savings")
    ax.fill_between(data["Year"], data["Annual Basket Price"], data["Annual Salary"], where=(data["Annual Basket Price"] > data["Annual Salary"]), interpolate=True, color='red', alpha=0.5, label="Deficit")
    ax.set_title("Comparison of Basket Price and Salary Over the Years")
    ax.set_ylabel("Amount (₪)")
    ax.set_xlabel("Year")
    ax.legend()
    st.pyplot(fig)

    # הצגת אחוזים מהמשכורת
    st.subheader("Basket Cost as Percentage of Salary")
    st.table(data[["Year", "Percentage of Salary"]])
else:
    st.warning("Please select at least one product to see the results.")
