import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# יצירת נתונים לדוגמה
data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Income": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75],
    "Rent": [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800],
    "Products": [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
}

# המרת הנתונים ל-DataFrame
df = pd.DataFrame(data)

# כותרת לאפליקציה
st.title("היסטוגרמה של הכנסות, הוצאות וחיסכון")

# בחירת טווח שנים להצגה
year_range = st.slider(
    "בחר טווח שנים להצגה:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2015, 2023),
)

# סינון הנתונים לפי טווח השנים
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# יצירת גרף היסטוגרמה
fig, ax = plt.subplots(figsize=(10, 6))

# שכבת הכנסות
ax.bar(
    filtered_df["Year"],
    filtered_df["Income"],
    label="Income",
    color="skyblue",
    edgecolor="black",
)

# שכבת הוצאות (שכירות + מוצרים)
ax.bar(
    filtered_df["Year"],
    filtered_df["Rent"] + filtered_df["Products"],
    label="Expenses (Rent + Products)",
    color="orange",
    edgecolor="black",
    alpha=0.7,
)

# הוספת תוויות
ax.set_xlabel("Year")
ax.set_ylabel("Amount (₪)")
ax.set_title("Income vs. Expenses Histogram")
ax.legend()

# הצגת הגרף ב-Streamlit
st.pyplot(fig)

# הצגת טבלה
st.subheader("נתונים מסוננים")
st.dataframe(filtered_df)
