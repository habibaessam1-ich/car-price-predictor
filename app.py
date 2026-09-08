
import sys
import joblib
import pandas as pd
import streamlit as st

# حل مشكلة اسم المكتبة المكتوب غلط جوه ملف الموديل
sys.modules['mport pandas as pd'] = pd

# إعدادات الصفحة
st.set_page_config(
    page_title="Car Price Predictor", page_icon="🚗", layout="centered"
)

# تحميل الموديل المجهز
@st.cache_resource
def load_model():
    return joblib.load("car_price_pipeline.pkl")

pipeline = load_model()

# قاموس لربط ماركة كل سيارة برابط صورة عالية الجودة
CAR_IMAGES = {
    "BMW": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80",
    "Mercedes": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80",
    "Toyota": "https://images.unsplash.com/photo-1590362891991-f776e747a588?auto=format&fit=crop&w=800&q=80",
    "Hyundai": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80",
    "Kia": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80",
}

# عنوان التطبيق واسم الفريق
st.title("🚗 Used Car Price Prediction System")

st.markdown("---")
st.markdown("👩‍💻 **Developed by:** Habiba Essam & Salma Ahmed")
st.markdown("---")

st.write("Enter the car specifications to get the estimated price.")

# تقسيم الشاشة لعمودين: المدخلات والصورة التفاعلية
col_input, col_img = st.columns([1.2, 1])

with col_input:
    brand = st.selectbox("Car Brand", list(CAR_IMAGES.keys()))
    year = st.number_input("Year", min_value=1990, max_value=2026, value=2020)
    driven_kms = st.number_input("Driven Kilometers", min_value=0, value=50000)
    transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

with col_img:
    # عرض صورة الماركة المختارة تلقائياً
    if brand in CAR_IMAGES:
        st.image(CAR_IMAGES[brand], caption=f"{brand} Preview", use_container_width=True)

# اختيار حالة السيارة
car_condition = st.radio(
    "Car Condition",
    ["Zero (Brand New)", "Nearly New (كسر زيرو)", "Used (مستعمل)"]
)

st.markdown("---")

# زر التوقع والحسابات
if st.button("Predict Price"):
    input_data = pd.DataFrame({
        "brand": [brand],
        "Year": [year],
        "Driven_Kms": [driven_kms],
        "Transmission": [transmission]
    })
    
    try:
        base_prediction = pipeline.predict(input_data)[0]

        # معامل ضرب الفئات والموديلات
        if brand in ["BMW", "Mercedes"]:
            if year >= 2021:
                multiplier = 6.5
            else:
                multiplier = 4.0
        else:
            if year >= 2021:
                multiplier = 2.0
            else:
                multiplier = 1.3

        # معامل حالة السيارة (مكتوب كاملاً وبدون أخطاء)
        if car_condition == "Zero (Brand New)":
            condition_multiplier = 1.25
        elif car_condition == "Nearly New (كسر زيرو)":
            condition_multiplier = 1.10
        else:
            condition_multiplier = 1.0

        final_price = base_prediction * multiplier * condition_multiplier

        st.success(f"Estimated Car Price: {final_price:,.2f} EGP")

    except Exception as e:
        st.error(f"حدث خطأ أثناء التوقع: {e}")