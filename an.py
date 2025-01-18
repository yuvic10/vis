import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני דוגמה
data = {
    'שנה': [2000, 2005, 2010, 2015, 2020],
    'מחיר אמיתי - דירות': [1000, 1500, 2200, 3000, 4500],
    'מחיר אמיתי - דלק': [5, 6, 8, 10, 12],
    'מחיר אמיתי - מוצרים': [20, 25, 30, 40, 60],
}
df = pd.DataFrame(data)

# מחוון לקצב צמיחה
growth_rate = st.slider('בחר קצב צמיחה שנתי (%):', min_value=0.0, max_value=10.0, step=0.1)

# חישוב מחירים מדומים
for category in ['דירות', 'דלק', 'מוצרים']:
    initial_price = df[f'מחיר אמיתי - {category}'].iloc[0]
    df[f'מחיר מדומה - {category}'] = [
        initial_price * (1 + growth_rate / 100) ** i for i in range(len(df))
    ]

# בחירת קטגוריה להצגה
category = st.selectbox('בחר קטגוריה:', ['דירות', 'דלק', 'מוצרים'])

# יצירת גרף
fig, ax = plt.subplots()
ax.plot(df['שנה'], df[f'מחיר אמיתי - {category}'], label='מחיר אמיתי', color='blue')
ax.plot(df['שנה'], df[f'מחיר מדומה - {category}'], label='מחיר מדומה', color='orange', linestyle='--')
ax.set_title(f'השוואה בין מחיר אמיתי למחיר מדומה ({category})')
ax.set_xlabel('שנה')
ax.set_ylabel('מחיר')
ax.legend()

# הצגת הגרף
st.pyplot(fig)
