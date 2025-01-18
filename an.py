import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
import streamlit as st
import tempfile

# נתוני הדוגמה
years = list(range(2015, 2024))
prices = [4000, 4500, 4800, 5000, 5200, 5300, 5400, 5500, 5700]
data = pd.DataFrame({"Year": years, "Price": prices})

# הגדרות הגרף
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(years))
bars = ax.bar(x, [0] * len(years), color='blue')

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylim(0, max(prices) * 1.1)
ax.set_title("מחירי הסל לאורך השנים", fontsize=16)
ax.set_xlabel("שנה", fontsize=14)
ax.set_ylabel("מחיר (₪)", fontsize=14)

# פונקציית עדכון לאנימציה
def update(frame):
    for i, bar in enumerate(bars):
        if i <= frame:
            bar.set_height(data["Price"].iloc[i])
        else:
            bar.set_height(0)

# יצירת אנימציה
ani = FuncAnimation(fig, update, frames=len(years), interval=500, repeat=False)

# שמירת האנימציה כקובץ GIF זמני
temp_gif = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
ani.save(temp_gif.name, writer="pillow", fps=2)

# הצגת האנימציה ב-Streamlit
st.title("אנימציה של מחירי הסל לאורך השנים")
st.image(temp_gif.name)
