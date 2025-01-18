import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# URL של קובץ ה-Excel שהועלה ל-GitHub
file_url = "https://raw.githubusercontent.com/username/repository/branch/basic_products.xlsx"

# כותרת האפליקציה
st.title("Product Basket Analysis")

try:
    # קריאת הנתונים מתוך הקובץ
    data = pd.read_excel(file_url, engine="openpyxl")
    st.write("### Data Preview")
    st.dataframe(data)

    # יצירת ממשק לבחירת מוצרים
    selected_products = st.multiselect("Select products to include in your basket:", options=data["product"].unique())

    # סינון הנתונים על סמך המוצרים שנבחרו
    if selected_products:
        filtered_data = data[data["product"].isin(selected_products)]

        # חישוב המחירים הכוללים לכל שנה
        yearly_totals = filtered_data.groupby("year")["yearly average price"].sum()

        # הצגת המחירים הכוללים
        st.write("### Total Basket Cost Per Year")
        st.line_chart(yearly_totals)

        # יצירת ענן מילים המבוסס על המחירים השנתיים
        word_frequencies = yearly_totals.to_dict()
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(word_frequencies)

        # הצגת ענן המילים
        st.write("### Word Cloud of Years Based on Basket Cost")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("Please select products to see the analysis.")

except Exception as e:
    st.error(f"Failed to load or process the file: {e}")
