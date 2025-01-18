import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
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

# חישוב סל קניות חודשי
monthly_basket_prices = [sum([products[prod][i] for prod in products]) for i in range(len(years))]
# חישוב עלות שנתית של סל הקניות (4 פעמים בחודש)
annual_basket_prices = [price * 4 * 12 for price in monthly_basket_prices]

# חישוב אחוז מהמשכורת
annual_salaries = [sal * 12 for sal in salary]
percentage_of_salary = [round((basket / salary) * 100, 2) for basket, salary in zip(annual_basket_prices, annual_salaries)]

# יצירת DataFrame
data = pd.DataFrame({
    "Year": years,
    "Annual Basket Price": annual_basket_prices,
    "Annual Salary": annual_salaries,
    "Percentage of Salary": percentage_of_salary
})

# כותרת
st.title("Impact of Shopping Basket Costs on Salaries Over the Years")

# גרף Boxplot
st.subheader("Boxplot: Comparison of Annual Basket Price and Salary")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=pd.melt(data, id_vars=["Year"], value_vars=["Annual Basket Price", "Annual Salary"]),
            x="Year", y="value", hue="variable", ax=ax)
ax.set_title("Boxplot of Annual Basket Price and Salary", fontsize=14)
ax.set_ylabel("Value")
ax.set_xlabel("Year")
st.pyplot(fig)

# טבלת אחוזים
st.subheader("Yearly Basket Cost as Percentage of Salary")
st.table(data[["Year", "Percentage of Salary"]])

# גרף מגמה
st.subheader("Trend: Basket Costs as Percentage of Salary")
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(data["Year"], data["Percentage of Salary"], marker="o", label="Percentage of Salary")
ax2.set_title("Basket Costs as Percentage of Salary Over the Years", fontsize=14)
ax2.set_ylabel("Percentage (%)")
ax2.set_xlabel("Year")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)
