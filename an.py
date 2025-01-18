import pandas as pd
import folium
from folium.plugins import TimeSliderChoropleth

# נתונים לדוגמה: אזורים, שנים והוצאות
data = {
    "Region": ["Tel Aviv", "Jerusalem", "Haifa"],
    "Lat": [32.0853, 31.7683, 32.7940],
    "Lon": [34.7818, 35.2137, 34.9896],
    "2015": [1000, 800, 700],
    "2016": [1100, 850, 720],
    "2017": [1200, 900, 740],
    "2018": [1300, 950, 770],
    "2019": [1400, 1000, 800],
    "2020": [1500, 1050, 850]
}

# יצירת DataFrame
df = pd.DataFrame(data)

# יצירת מפה
m = folium.Map(location=[32.0853, 34.7818], zoom_start=7)

# הוספת שכבות לפי שנים
for year in range(2015, 2021):
    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=10,
            color=f"#{hex(int(row[str(year)]) % 255)[2:]:0>2}00",
            fill=True,
            fill_opacity=0.6,
            popup=f"{row['Region']} - {year}: {row[str(year)]} NIS",
        ).add_to(m)

# שמירת המפה
m.save("expenses_map.html")
