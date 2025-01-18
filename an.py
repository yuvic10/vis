import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# נתונים לדוגמה: אחוזי סל הקניות מהמשכורת לאורך השנים
year_data = {
    2015: 2,
    2016: 3,
    2017: 4,
    2018: 3,
    2019: 5,
    2020: 6,
    2021: 4,
    2022: 5,
    2023: 7
}

# ממשק Streamlit
st.title("Word Cloud of Years Based on Shopping Basket Percentage")
st.write("Select a threshold percentage to filter the years shown.")

# בחירת סף אחוזים
threshold = st.slider("Select Threshold Percentage", min_value=1, max_value=10, value=3)

# סינון שנים לפי סף
filtered_years = {str(year): value for year, value in year_data.items() if value >= threshold}

# בדיקה אם יש שנים להצגה
if filtered_years:
    # יצירת ענן מילים
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white'
    ).generate_from_frequencies(filtered_years)

    # הצגת ענן המילים
    st.subheader("Filtered Word Cloud")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.warning("No years match the selected threshold.")
