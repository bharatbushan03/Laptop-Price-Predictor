import streamlit as st
import pandas as pd
import requests
import os

try:
    df = pd.read_csv('new_laptop_price.csv')
except FileNotFoundError:
    st.error("Dataset 'new_laptop_price.csv' not found. Cannot populate dropdowns.")
    st.stop()

st.title("Laptop Price Predictor")

company = st.selectbox('Choose the laptop company', df['Company'].unique())
typename = st.selectbox('Choose the laptop type', df['TypeName'].unique())
inches = st.slider('Choose the size of the laptop in inches', 10.0, 20.0, 10.6)
screen_resolution = st.selectbox('Choose the screen resolution', df['ScreenResolution'].unique())
cpu = st.selectbox('Choose the CPU of the laptop', df['Cpu'].unique())
ram = st.slider('Choose the RAM of the laptop in GB', 2, 64, 16)
gpu = st.selectbox('Choose the GPU of the laptop', df['Gpu'].unique())
os_selection = st.selectbox('Choose the operating system of the laptop', df['OpSys'].unique())
weight = st.slider('Choose the weight of the laptop in kg', 0.5, 5.0, 1.5)
ssd = st.slider('Choose the SSD of the laptop in GB', 0, 2048, 256)
hdd = st.slider('Choose the HDD of the laptop in GB', 0, 2048, 0)
flash_storage = st.slider('Choose the flash storage of the laptop in GB', 0, 1024, 0)
hybrid_storage = st.slider('Choose the hybrid storage of the laptop in GB', 0, 1024, 0)

API_URL = os.getenv('API_URL', 'https://laptop-price-predictor-d3g1.onrender.com/predict')

if st.button('Predict Price'):
    data = {
        'company': company,
        'typename': typename,
        'inches': inches,
        'screen_resolution': screen_resolution,
        'cpu': cpu,
        'ram': ram,
        'gpu': gpu,
        'os': os_selection,
        'weight': weight,
        'ssd': ssd,
        'hdd': hdd,
        'flash_storage': flash_storage,
        'hybrid_storage': hybrid_storage
    }

    with st.spinner('Predicting...'):
        try:
            response = requests.post(API_URL, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            st.success(result['message'])
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
