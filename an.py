import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# נתוני דוגמה: שנים וכמות (או תדירות) ששייכת לכל שנה
data = {
    "2015": 10,
    "2016": 15,
    "2017": 20,
    "2018": 5,
    "2019": 25,
    "2020": 30,
    "2021": 40,
    "2022": 35,
    "2023": 50
}

# פונקציה ליצירת WordCloud
def create_wordcloud(data):
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white",
        colormap="viridis"
    ).generate_from_frequencies(data)
    return wordcloud

# כותרת לאפליקציה
st.title("השוואת שנים לפי תדירות הוספה לסל")

# בחירה של שנים להוספה
selected_years = st.multiselect(
    "בחר שנים להוספה לסל:",
    options=list(data.keys()),
    default=["2015", "2016"]
)

# חישוב סך הפרופורציה של השנים שנבחרו
filtered_data = {year: data[year] for year in selected_years}

# יצירת WordCloud
wordcloud = create_wordcloud(filtered_data)

# הצגת WordCloud
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# הצגת טבלה
st.subheader("תדירות השנים שנבחרו")
st.write(filtered_data)
