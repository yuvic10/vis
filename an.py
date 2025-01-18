import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# יצירת נתונים לדוגמה
data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Income": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75],
    "Rent": [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800],
    "Products": [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800]
}

# המרת הנתונים ל-DataFrame
df = pd.DataFrame(data)

# חישוב הוצאות כלליות וחיסכון
df["Total Expenses"] = df["Rent"] + df["Products"]
df["Savings"] = df["Income"] - df["Total Expenses"]

# כותרת האפליקציה
st.title("היסטוגרמה של הכנסות, הוצאות וחיסכון לאורך השנים")

# בחירת טווח שנים להצגה
year_range = st.slider(
    "בחר את טווח השנים להצגה:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2015, 2023)
)

# סינון הנתונים לפי טווח השנים
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# יצירת גרף היסטוגרמה
fig, ax = plt.subplots()

bar_width = 0.4
x = np.arange(len(filtered_df["Year"]))

# גרף הכנסות
ax.bar(x - bar_width / 2, filtered_df["Income"], bar_width, label="Income", color="skyblue", edgecolor="black")

# גרף הוצאות
ax.bar(x + bar_width / 2, filtered_df["Total Expenses"], bar_width, label="Expenses", color="orange", edgecolor="black")

# הוספת תוויות וטקסט
ax.set_xlabel("Year")
ax.set_ylabel("Amount (₪)")
ax.set_title("Income vs. Expenses (and Savings)")
ax.set_xticks(x)
ax.set_xticklabels(filtered_df["Year"])
ax.legend()

# הצגת החיסכון כטקסט מעל העמודות
for i in range(len(filtered_df)):
    savings = filtered_df.iloc[i]["Savings"]
    ax.text(
        x[i], max(filtered_df.iloc[i]["Income"], filtered_df.iloc[i]["Total Expenses"]) + 100,
        f"Saving: {savings:.2f}", ha="center", fontsize=8
    )

# הצגת הגרף באפליקציה
st.pyplot(fig)

# הצגת טבלה מסוננת
st.subheader("נתונים מסוננים")
st.dataframe(filtered_df)
