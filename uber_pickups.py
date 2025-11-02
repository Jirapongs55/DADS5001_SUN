import streamlit as st
import pandas as pd
import numpy as np
import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("starbucks/store-locations")

print("Path to dataset files:", path)


for file in os.listdir(path):
    if file.endwith(".csv"):
        data_path = os.path.join(path, file)
        break
    
df = pd.read_csv(data_path)

st.title('Starbucks Locations Worldwide by JS')

@st.cache_data
def load_data(nrows):
    data = df
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
