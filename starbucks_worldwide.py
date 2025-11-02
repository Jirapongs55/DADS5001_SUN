import streamlit as st
import pandas as pd
import numpy as np
import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("starbucks/store-locations")

print("Path to dataset files:", path)


for file in os.listdir(path):
    if file.endswith(".csv"):
        data_path = os.path.join(path, file)
        break
    
df = pd.read_csv(data_path)

st.title('Starbucks Locations Worldwide by JS')

@st.cache_data
def load_data():
    data = df.copy()
    data.columns = [c.lower() for c in data.columns]
    return data
    

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data.head())

st.subheader('Number of Starbucks stores by country')
country_counts = data["country"].value_counts()
st.bar_chart(country_counts)

# แสดงแผนที่ของร้าน (ใช้ latitude และ longitude)
if 'latitude' in data.columns and 'longitude' in data.columns:
    st.subheader('🗺️ Starbucks Store Locations Map')
    map_data = data.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
    map_data = map_data.dropna(subset=['lat', 'lon'])  # ✅ ลบแถวที่ lat/lon ว่าง
    st.map(map_data)
else:
    st.warning("This dataset does not contain latitude/longitude columns.")
