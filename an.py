import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# נתוני דוגמה ליצירת היסטוגרמה
st.title("Histogram of Category Prices Over the Years")

# העלאת נתונים
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    # קריאה של הקובץ שהמשתמש מעלה
    df = pd.read_csv(uploaded_file)

    # וידוא שהעמודות הדרושות קיימות
    required_columns = ["Year", "Category", "Price"]
    if all(col in df.columns for col in required_columns):
        st.success("Dataset successfully loaded!")

        # בחירת קטגוריות להצגה
        categories = df["Category"].unique()
        selected_category = st.selectbox("Select Category", categories)

        # סינון נתונים לקטגוריה שנבחרה
        filtered_data = df[df["Category"] == selected_category]

        # יצירת ההיסטוגרמה
        plt.figure(figsize=(10, 6))
        plt.hist(filtered_data["Price"], bins=10, color="skyblue", edgecolor="black")
        plt.title(f"Histogram of Prices for {selected_category}")
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        plt.grid(axis="y", alpha=0.75)

        # הצגת הגרף ב-Streamlit
        st.pyplot(plt)

        # הצגת נתונים סטטיסטיים
        st.write("## Summary Statistics")
        st.write(filtered_data["Price"].describe())

    else:
        st.error(f"Dataset must include the following columns: {', '.join(required_columns)}")
else:
    st.info("Please upload a dataset to generate the histogram.")
