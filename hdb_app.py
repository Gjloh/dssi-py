# hdb_app.py
import streamlit as st
import pandas as pd
from src.inference import get_prediction

# Set page config
apptitle = 'HDB Rent Prediction'
st.set_page_config(page_title=apptitle, layout='wide')

st.title('🏠 HDB Rent Prediction App')
st.write('Enter flat details below to predict the monthly rent.')

# Input form
col1, col2 = st.columns([2,1])
with col1:
    year = st.number_input("Year", min_value=2021, max_value=2030, value=2021)
    month = st.selectbox("Month", list(range(1, 13)), index=0)
    town = st.text_input("Town", "ANG MO KIO")
    block = st.text_input("Block", "105")
    street_name = st.text_input("Street Name", "ANG MO KIO AVE 4")
    flat_type = st.selectbox("Flat Type", ["1-ROOM","2-ROOM","3-ROOM","4-ROOM","5-ROOM","EXECUTIVE"])

with col2:
    st.info("Fill in the details and click Predict.")

# Predict button
if st.button("Predict Rent"):
    input_data = {
        "year": year,
        "month": month,
        "town": town,
        "block": block,
        "street_name": street_name,
        "flat_type": flat_type
    }
    prediction = get_prediction(**input_data)
    st.success(f"Predicted Monthly Rent: ${prediction:.2f}")
