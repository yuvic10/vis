import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# העלאת קובץ אקסל
uploaded_file = st.file_uploader("Upload an Excel file with product data", type="xlsx")

if uploaded_file:
    # קריאת קובץ האקסל
    data = pd.read_excel(uploaded_file)

    # בדיקת מבנה הנתונים
    if {'product', 'year', 'yearly average price'}.issubset(data.columns):
        st.write("Data loaded successfully!")

        # בחירת מוצרים להרכבת סל
        products = st.multiselect("Select products to add to the basket", options=data['product'].unique())

        if products:
            # פילטר על המוצרים שנבחרו
            filtered_data = data[data['product'].isin(products)]

            # חישוב עלות שנתית של הסל
            yearly_cost = filtered_data.groupby('year')['yearly average price'].sum()

            # בחירת סף מחיר
            max_cost = st.slider("Set maximum cost for the basket", min_value=0, max_value=int(yearly_cost.max()), value=50)

            # סינון שנים שמתאימות לתקציב
            affordable_years = yearly_cost[yearly_cost <= max_cost]

            if not affordable_years.empty:
                st.write("Years that fit within the budget:", affordable_years.index.tolist())

                # יצירת ענן מילים
                wordcloud = WordCloud(
                    width=800, height=400, background_color='white'
                ).generate_from_frequencies(affordable_years.to_dict())

                # הצגת ענן המילים
                st.subheader("Word Cloud of Affordable Years")
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.warning("No years match the selected budget.")
    else:
        st.error("The uploaded file does not have the required columns: 'product', 'year', 'yearly average price'")
