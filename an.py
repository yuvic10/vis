import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# נתוני המוצרים
product_data = {
    'product': ['קמח לבן', 'פסטה', 'אורז רגיל', 'חזה עוף', 'טחינה גולמית'],
    '2015': [4.088, 5.343, 9.596, 33.313, 14.568],
    '2016': [4.062, 5.483, 9.568, 32.648, 13.226],
    '2017': [3.978, 5.305, 9.426, 31.876, 12.112],
    '2018': [3.888, 5.337, 9.928, 31.750, 11.696],
    '2019': [3.798, 5.303, 10.119, 33.245, 12.471],
    '2020': [3.781, 5.541, 10.224, 32.949, 13.184],
    '2021': [4.032, 5.470, 10.515, 31.502, 13.444],
    '2022': [4.516, 5.828, 11.038, 33.887, 13.576],
    '2023': [4.730, 6.193, 11.178, 39.168, 14.132],
}

# יצירת DataFrame
df = pd.DataFrame(product_data)

# סל מוצרים שנבחר על ידי המשתמש
st.sidebar.title("בחירת מוצרים לסל")
selected_products = st.sidebar.multiselect("בחר מוצרים להוספה לסל:", options=df['product'].tolist())

# חישוב מחירי הסל לכל שנה
if selected_products:
    filtered_df = df[df['product'].isin(selected_products)]
    total_prices = filtered_df.iloc[:, 1:].sum()
else:
    total_prices = pd.Series({year: 0 for year in product_data.keys() if year != 'product'})

# יצירת Word Cloud
year_prices = {str(year): price for year, price in total_prices.items()}
max_price = max(year_prices.values()) if year_prices else 1
scaled_prices = {year: (price / max_price) * 100 for year, price in year_prices.items()}  # קנה מידה

wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(scaled_prices)

# הצגת Word Cloud
st.title("Word Cloud - גודל השנים לפי מחירי הסל")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# הצגת המחירים
st.sidebar.subheader("מחירי הסל לפי שנים")
st.sidebar.write(pd.DataFrame(year_prices.items(), columns=["שנה", "מחיר"]))
