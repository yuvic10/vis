import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני בסיס
data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020],
    'Minimum Wage': [5000, 5200, 5400, 5500, 5700, 6000],  # הכנסות
    'Total Expenses': [4800, 5100, 5300, 5600, 5800, 6100],  # הוצאות כוללות
}
df = pd.DataFrame(data)

# מחוונים לחלוקת הוצאות
st.sidebar.header("Adjust Expense Proportions")
fuel_percent = st.sidebar.slider("Fuel (%)", 0, 100, 30)
rent_percent = st.sidebar.slider("Rent (%)", 0, 100, 50)
products_percent = st.sidebar.slider("Basic Products (%)", 0, 100, 20)

# וידוא שהאחוזים מסתכמים ל-100
total_percent = fuel_percent + rent_percent + products_percent
if total_percent != 100:
    st.error("The total percentage must equal 100%!")
else:
    # חישוב הוצאות מותאמות
    df['Adjusted Expenses'] = df['Total Expenses'] * (
        (fuel_percent / 100) + (rent_percent / 100) + (products_percent / 100)
    )

    # חישוב חיסכון
    df['Savings'] = df['Minimum Wage'] - df['Adjusted Expenses']

    # גרף קווי עם אזורים צבעוניים
    st.title("Income vs. Expenses with Savings/Deficit Visualization")
    fig, ax = plt.subplots()

    # קווים
    ax.plot(df['Year'], df['Minimum Wage'], label='Minimum Wage', color='blue', linewidth=2)
    ax.plot(df['Year'], df['Adjusted Expenses'], label='Adjusted Expenses', color='red', linewidth=2)

    # אזורים ירוקים ואדומים
    ax.fill_between(
        df['Year'],
        df['Minimum Wage'],
        df['Adjusted Expenses'],
        where=(df['Minimum Wage'] >= df['Adjusted Expenses']),
        color='lightgreen',
        alpha=0.5,
        label='Savings (Surplus)'
    )
    ax.fill_between(
        df['Year'],
        df['Minimum Wage'],
        df['Adjusted Expenses'],
        where=(df['Minimum Wage'] < df['Adjusted Expenses']),
        color='pink',
        alpha=0.5,
        label='Deficit'
    )

    # כותרות וצירים
    ax.set_title("Income vs. Expenses Over Time", fontsize=16)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Amount (NIS)", fontsize=12)
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    ax.legend()

    # הצגת הגרף
    st.pyplot(fig)

    # טבלה אינטראקטיבית להצגת הנתונים
    st.subheader("Data Table")
    st.dataframe(df)

    # הצגת surplus/deficit של שנה מסוימת
    st.subheader("Surplus/Deficit by Year")
    selected_year = st.selectbox("Select a Year:", df['Year'])
    selected_data = df[df['Year'] == selected_year]
    st.metric(
        f"Savings in {selected_year}",
        f"{selected_data['Savings'].values[0]:.2f} NIS",
        delta=f"{selected_data['Savings'].values[0]:.2f} NIS"
    )
