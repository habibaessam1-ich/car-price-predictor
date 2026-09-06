import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="توقع سعر السيارة", page_icon="🚗", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load('car_price_pipeline.pkl')

pipeline = load_model()

st.title("🚗 نظام التنبؤ بأسعار السيارات المستعملة")
st.write("أدخل مواصفات السيارة للحصول على السعر التقديري المتوقع")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("سنة الصنع (Year)", min_value=2000, max_value=2026, value=2018)
    fuel_type = st.selectbox("نوع الوقود (Fuel)", ["Petrol", "Diesel"])

with col2:
    km_driven = st.number_input("الكيلومترات المقطوعة (KM)", min_value=0, max_value=500000, value=50000, step=5000)
    transmission = st.radio("نوع القير (Transmission)", ["Manual", "Automatic"])

st.markdown("---")

if st.button("احسب السعر المتوقع 💰", use_container_width=True):
    input_data = pd.DataFrame({
        'Year': [year],
        'KM_Driven': [km_driven],
        'Fuel_Type': [fuel_type],
        'Transmission': [transmission]
    })
    
    predicted_price = pipeline.predict(input_data)[0]
    st.success(f"السعر التقديري للسيارة: **{predicted_price:,.2f} جنيه**")


st.markdown("---")
st.write("👨‍💻 **Developed by:**")
st.write("- Habiba Essam")
st.write("- Salma Ahmed")
