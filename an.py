import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני בסיס
data = {
    'Year': [2020],
    'Minimum Wage': [5000],  # הכנסות
    'Total Expenses': [6000]  # הוצאות
}
df = pd.DataFrame(data)

# כותרת
st.title("Impact of Expense Distribution on Income Balance")

# מחוונים לחלוקה (דלק, שכירות, מוצרים)
st.sidebar.header("Adjust Expense Distribution")
fuel_percent = st.sidebar.slider("Fuel (%)", 0, 100, 30)
rent_percent = st.sidebar.slider("Rent (%)", 0, 100, 50)
products_percent = st.sidebar.slider("Basic Products (%)", 0, 100, 20)

# וידוא שהאחוזים מסתכמים ל-100
total_percent = fuel_percent + rent_percent + products_percent
if total_percent != 100:
    st.error("The total percentage must equal 100%!")
else:
    # חישוב הוצאות לפי החלוקה
    total_expenses = (
        (df['Total Expenses'][0] * fuel_percent / 100) +
        (df['Total Expenses'][0] * rent_percent / 100) +
        (df['Total Expenses'][0] * products_percent / 100)
    )

    # חישוב הפער
    balance = df['Minimum Wage'][0] - total_expenses

    # גרף עוגה (Pie Chart)
    labels = ['Fuel', 'Rent', 'Basic Products']
    sizes = [fuel_percent, rent_percent, products_percent]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title("Expense Distribution")
    st.pyplot(fig1)

    # תצוגה של הפער
    st.metric("Balance (Surplus/Deficit)", f"{balance:.2f} NIS")

    # גרף קווי המציג את הפער
    fig2, ax2 = plt.subplots()
    ax2.axhline(0, color='black', linestyle='--')  # קו בסיס
    ax2.bar(['Balance'], [balance], color='green' if balance > 0 else 'red')
    ax2.set_title("Income vs. Expenses Balance")
    ax2.set_ylabel("NIS")
    st.pyplot(fig2)
