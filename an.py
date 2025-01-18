import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# נתונים לדוגמה
years = list(range(2015, 2024))
prices = [100, 120, 140, 150, 170, 200, 230, 250, 270]
products = ["Flour", "Rice", "Chicken", "Oil", "Milk", "Bread", "Eggs", "Tomatoes"]

# פונקציה ליצירת פריים באנימציה
def update(frame):
    plt.clf()
    plt.barh(products[:frame+1], prices[:frame+1], color="skyblue")
    plt.title(f"Shopping Basket in {years[frame]}")
    plt.xlabel("Price")
    plt.xlim(0, max(prices) + 50)

# יצירת האנימציה
fig, ax = plt.subplots(figsize=(6, 4))
ani = FuncAnimation(fig, update, frames=len(years), interval=1000, repeat=True)

# הצגת האנימציה ב-Streamlit
st.write("### Dynamic Shopping Basket")
st.write("See how the basket's price grows over the years.")
st.pyplot(fig)
