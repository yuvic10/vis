import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# נתוני דוגמה
data = {
    'שנה': [2000, 2005, 2010, 2015, 2020],
    'שכר מינימום': [3000, 3500, 4000, 4500, 5000],
    'יוקר מחיה': [2800, 3600, 4200, 4800, 5500]
}
df = pd.DataFrame(data)

# חישוב פערים
df['פער (ש"ח)'] = df['שכר מינימום'] - df['יוקר מחיה']

# כותרת האפליקציה
st.title("שכר מינימום מול יוקר המחיה")

# גרף קווי: שכר מינימום ויוקר מחיה
fig, ax = plt.subplots()
ax.plot(df['שנה'], df['שכר מינימום'], label='שכר מינימום', color='blue')
ax.plot(df['שנה'], df['יוקר מחיה'], label='יוקר מחיה', color='red')
ax.fill_between(df['שנה'], df['שכר מינימום'], df['יוקר מחיה'], 
                where=(df['שכר מינימום'] < df['יוקר מחיה']), color='pink', alpha=0.3, label='פער שלילי')
ax.fill_between(df['שנה'], df['שכר מינימום'], df['יוקר מחיה'], 
                where=(df['שכר מינימום'] >= df['יוקר מחיה']), color='lightgreen', alpha=0.3, label='פער חיובי')
ax.set_title("השוואת שכר מינימום ליוקר המחיה")
ax.set_xlabel("שנה")
ax.set_ylabel("ש"ח")
ax.legend()

# הצגת הגרף
st.pyplot(fig)

# טבלה להצגת הנתונים
st.dataframe(df)

# מד חיסכון שנתי
year = st.selectbox('בחר שנה:', df['שנה'])
selected_year = df[df['שנה'] == year]
st.metric(label=f"פער בשנה {year}", value=f"{selected_year['פער (ש"ח)'].values[0]} ש\"ח")
