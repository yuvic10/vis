import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני בסיס
data = {
    'Year': [2015, 2016, 2017, 2018, 2019, 2020],
    'Minimum Wage': [5000, 5200, 5400, 5500, 5700, 6000],  # הכנסה
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

    # חישוב Surplus Index
    df['Surplus Index (%)'] = ((df['Minimum Wage'] - df['Adjusted Expenses']) / df['Minimum Wage']) * 100

    # גרף קווי: Surplus Index
    st.title("Surplus Index Over Time")
    fig, ax = plt.subplots()
    ax.plot(df['Year'], df['Surplus Index (%)'], label='Surplus Index (%)', color='green', marker='o')

    # כותרות וצירים
    ax.set_title("Surplus Index Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Surplus Index (%)")
    ax.axhline(0, color='red', linestyle='--', label='Break-Even Point')
    ax.legend()

    # הצגת הגרף
    st.pyplot(fig)

    # הצגת טבלה עם הנתונים
    st.subheader("Data Table")
    st.dataframe(df)

    # הצגת surplus של שנה מסוימת
    st.subheader("Surplus Comparison by Year")
    selected_year = st.selectbox("Select a Year:", df['Year'])
    selected_data = df[df['Year'] == selected_year]
    st.metric(f"Surplus Index in {selected_year}", f"{selected_data['Surplus Index (%)'].values[0]:.2f}%")
