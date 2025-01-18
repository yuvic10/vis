import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tempfile
import os

# נתונים לדוגמה
data = {
    "Year": list(range(2015, 2024)),
    "Price": [4000, 4500, 4800, 5000, 5200, 5300, 5400, 5500, 5700],
}
df = pd.DataFrame(data)

# פונקציה ליצירת אנימציה
def create_animation(dataframe):
    years = dataframe["Year"]
    prices = dataframe["Price"]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(min(years) - 1, max(years) + 1)
    ax.set_ylim(0, max(prices) * 1.1)
    ax.set_title("זרימת מחירי הסל לאורך השנים", fontsize=16)
    ax.set_xlabel("שנה", fontsize=14)
    ax.set_ylabel("מחיר (₪)", fontsize=14)

    line, = ax.plot([], [], lw=2, color="blue", marker="o")

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        line.set_data(years[:frame + 1], prices[:frame + 1])
        return line,

    ani = FuncAnimation(fig, update, frames=len(years), init_func=init, interval=500, blit=True)

    # שמירת האנימציה כ-GIF זמני
    temp_gif = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
    ani.save(temp_gif.name, writer="pillow", fps=2)
    plt.close(fig)
    return temp_gif.name

# יצירת אנימציה
st.title("זרימת מחירי הסל לאורך השנים")
st.write("האנימציה מציגה את העלייה במחירי הסל לאורך השנים בצורה דינמית.")

gif_path = create_animation(df)

# הצגת האנימציה ב-Streamlit
st.image(gif_path)

# מחיקת הקובץ הזמני אחרי סיום השימוש
def cleanup_file():
    if os.path.exists(gif_path):
        os.remove(gif_path)

st.on_event("disconnect", cleanup_file)
