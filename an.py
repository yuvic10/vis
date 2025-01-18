import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# יצירת נתונים לדוגמה
data = {
    "Year": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    "Rent": [4650, 4825, 5000, 5300, 5300, 5300, 5300, 5300, 5571.75],
    "Products": [20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]
}

# המרת הנתונים ל-DataFrame
df = pd.DataFrame(data)

# כותרת האפליקציה
st.title("השוואת מחירי שכירות ומוצרים לאורך השנים")

# הצגת טווח בחירה לשנים
year_range = st.slider(
    "בחר את טווח השנים להצגה:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(2015, 2023)
)

# סינון נתונים לפי טווח השנים
filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

# יצירת גרף
fig, ax = plt.subplots()
ax.plot(filtered_df["Year"], filtered_df["Rent"], label="Rent", marker="o", color="blue")
ax.plot(filtered_df["Year"], filtered_df["Products"], label="Products", marker="o", color="green")
ax.set_xlabel("Year")
ax.set_ylabel("Price")
ax.set_title("Comparison of Rent and Product Prices Over Years")
ax.legend()

# הצגת הגרף
st.pyplot(fig)

# הצגת הנתונים בטבלה
st.subheader("נתונים מסוננים")
st.dataframe(filtered_df)
