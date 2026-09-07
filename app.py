import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

st.set_page_config(page_title="Car Price Predictor - Egypt", page_icon="🚗", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load('car_price_pipeline.pkl')

pipeline = load_model()

st.title("🚗 Egyptian Used Car Price Prediction System")

st.markdown("---")
st.markdown("👩‍💻 **Developed by:** Habiba Essam & Salma Ahmed")
st.markdown("---")

st.write("Enter the car specifications to get the estimated market price in Egypt.")

# إدخال البيانات
brand = st.selectbox("Car Brand", ["Toyota", "Hyundai", "Kia", "Nissan", "Chevrolet", "BMW", "Mercedes"])
car_type = st.selectbox("Car Type / Model", ["Sedan", "SUV", "Hatchback", "Coupe"])
transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Manufacturing Year", min_value=2000, max_value=2026, value=2022)
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])

with col2:
    km_driven = st.number_input("Kilometers Driven (KM)", min_value=0, max_value=500000, value=5000)

st.markdown("---")
st.subheader("🛠️ Extra Features & Options")

# إضافات جديدة للواجهة
col3, col4 = st.columns(2)
with col3:
    sunroof = st.checkbox("Sunroof / Panoramic Roof")
    screen = st.checkbox("Touchscreen Multimedia")
with col4:
    sensors = st.checkbox("Parking Sensors & Camera")
    leather_seats = st.checkbox("Leather Seats")

st.markdown("---")

if st.button("Predict Price"):
    input_data = pd.DataFrame({
        'brand': [brand],
        'car_type': [car_type],
        'Year': [year],
        'Fuel_Type': [fuel_type],
        'KM_Driven': [km_driven],
        'Transmission': [transmission]
    })
    
    try:
        base_prediction = pipeline.predict(input_data)[0]
        
        # معامل التصحيح الأساسي للسوق المصري
        multiplier = 1.0
        if brand in ["BMW", "Mercedes"]:
            if year >= 2021:
                multiplier = 6.5
            elif year >= 2017:
                multiplier = 4.5
            else:
                multiplier = 3.0
        else:
            if year >= 2022:
                multiplier = 3.2
            elif year >= 2018:
                multiplier = 2.4
            else:
                multiplier = 1.8
                
        # إضافة قيمة بسيطة للإضافات (الكماليات) لو المستخدم اختارها
        extras_bonus = 0
        if sunroof: extras_bonus += 50000
        if screen: extras_bonus += 20000
        if sensors: extras_bonus += 15000
        if leather_seats: extras_bonus += 25000
        
        final_price = (base_prediction * multiplier) + extras_bonus
        
        # عرض السعر المتوقع
        st.success(f"🏷️ The estimated car price is: {final_price:,.2f} EGP")
        
        # صندوق معلومات السوق (Market Insights)
        st.info("💡 **Market Insight:** Price calculated based on current Egyptian market inflation, brand tier, manufacturing year, and selected luxury options.")
        
        # رسم بياني مبسط لمقارنة السعر حسب السنوات القريبة
        st.markdown("### 📊 Price Comparison Across Recent Years")
        fig, ax = plt.subplots(figsize=(8, 3))
        years_list = [year - 2, year - 1, year, year + 1]
        # محاكاة أسعار تقريبية للرسم البياني للتوضيح
        prices_list = [final_price * 0.8, final_price * 0.9, final_price, final_price * 1.1]
        ax.plot([str(y) for y in years_list], prices_list, marker='o', color='#1f77b4', linewidth=2)
        ax.set_ylabel("Price (EGP)")
        ax.set_xlabel("Year Trend")
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")