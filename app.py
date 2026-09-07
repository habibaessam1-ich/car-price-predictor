import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load('car_price_pipeline.pkl')

pipeline = load_model()

st.title("🚗 Used Car Price Prediction System")

st.markdown("---")
st.markdown("👨‍💻 **Developed by:** Habiba Essam & Salma Ahmed")
st.markdown("---")

st.write("Enter the car specifications to get the estimated price.")

brand = st.selectbox("Car Brand", ["Toyota", "Hyundai", "Kia", "Nissan", "Chevrolet", "BMW", "Mercedes"])
car_type = st.selectbox("Car Type / Model", ["Sedan", "SUV", "Hatchback", "Coupe"])
transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Manufacturing Year", min_value=2000, max_value=2026, value=2018)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])

with col2:
    km_driven = st.number_input("Kilometers Driven (KM)", min_value=0, max_value=500000, value=50000)

st.markdown("---")

if st.button("Predict Price"):
    # أسماء الأعمدة مطابقة تماماً لما يتوقعه الموديل
    input_data = pd.DataFrame({
        'brand': [brand],
        'car_type': [car_type],
        'Year': [year],
        'Fuel_Type': [fuel_type],
        'KM_Driven': [km_driven],
        'Transmission': [transmission]
    })
    
    try:
        prediction = pipeline.predict(input_data)
        st.success(f"The estimated car price is: {prediction[0]:,.2f} EGP")
    except Exception as e:
        st.error(f"An error occurred during prediction: Make sure model columns match input. Details: {e}")