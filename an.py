import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# יצירת נתונים לדוגמה
data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Income": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75],
    "Rent": [2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800],
    "Products": [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800]
}

# המרת הנתונים ל-DataFrame
df = pd.DataFrame(data)

# חישוב החיסכון (הכנסה פחות סך ההוצאות)
df["Savings"] = df["Income"] - (df["Rent"] + df["Products"])

# כותרת האפליקציה
st.title("היסטוגרמה של החיסכון לאורך השנים")

# בחירת טווח שנים להצגה
year_range = st.slider(
    "בחר את טווח השנים להצגה:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2015, 2023)
)

# סינון הנתונים לפי טווח השנים
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# יצירת היסטוגרמה
fig, ax = plt.subplots()
ax.bar(filtered_df["Year"], filtered_df["Savings"], color="skyblue", edgecolor="black")
ax.set_xlabel("Year")
ax.set_ylabel("Savings (Income - Expenses)")
ax.set_title("Histogram of Savings Over the Years")

# הצגת ההיסטוגרמה
st.pyplot(fig)

# הצגת נתונים מסוננים
st.subheader("נתונים מסוננים")
st.dataframe(filtered_df)
