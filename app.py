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

# 1. قاموس لربط ماركة كل سيارة برابط صورة عالية الجودة
CAR_IMAGES = {
    "BMW": (
        "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80"
    ),
    "Mercedes": (
        "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80"
    ),
    "Toyota": (
        "https://images.unsplash.com/photo-1629897048514-3dd7414fe72a?auto=format&fit=crop&w=800&q=80"
    ),
    "Hyundai": (
        "https://images.unsplash.com/photo-1619767886558-efdc259cde1a?auto=format&fit=crop&w=800&q=80"
    ),
    "Kia": (
        "https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?auto=format&fit=crop&w=800&q=80"
    ),
    "Nissan": (
        "https://images.unsplash.com/photo-1609521263047-f8d205293f24?auto=format&fit=crop&w=800&q=80"
    ),
    "Chevrolet": (
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80"
    ),
}

# عنوان التطبيق واسم الفريق
st.title("🚗 Used Car Price Prediction System")

st.markdown("---")
st.markdown("👩‍💻 **Developed by:** Salma Ahmed & Habiba Essam")
st.markdown("---")

st.write("Enter the car specifications to get the estimated price.")

# 2. تقسيم الشاشة لعمودين: المدخلات والصورة التفاعلية
col_input, col_img = st.columns([1.2, 1])

with col_input:
    brand = st.selectbox("Car Brand", list(CAR_IMAGES.keys()))
    car_type = st.selectbox(
        "Car Type / Model", ["Sedan", "SUV", "Hatchback", "Coupe"]
    )
    transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

with col_img:
    st.image(
        CAR_IMAGES[brand], caption=f"{brand} Preview", use_container_width=True
    )

# اختيار حالة السيارة
car_condition = st.radio(
    "Car Condition",
    ["Zero (Brand New)", "Nearly New (كسر زيرو)", "Used (مستعمل)"],
    horizontal=True,
)

col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "Manufacturing Year", min_value=2000, max_value=2026, value=2022
    )
    fuel_type = st.selectbox(
        "Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"]
    )

with col2:
    if car_condition == "Zero (Brand New)":
        km_driven = 0
        st.info("Kilometers Driven: 0 KM (Brand New)")
    else:
        km_driven = st.number_input(
            "Kilometers Driven (KM)", min_value=0, max_value=500000, value=5000
        )

st.markdown("---")

# زر التوقع والحسابات
if st.button("Predict Price"):
    input_data = pd.DataFrame({
        "brand": [brand],
        "car_type": [car_type],
        "Year": [year],
        "Fuel_Type": [fuel_type],
        "KM_Driven": [km_driven],
        "Transmission": [transmission],
    })

    try:
        base_prediction = pipeline.predict(input_data)[0]

        # معامل ضرب الفئات والموديلات
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
            elif year >= 2012:
                multiplier = 1.8
            else:
                multiplier = 1.3

        # معامل حالة السيارة
        if car_condition == "Zero (Brand New)":
            condition_multiplier = 1.25
        elif car_condition == "Nearly New (كسر زيرو)":
            condition_multiplier = 1.10
        else:
            condition_multiplier = 1.0

        final_price = base_prediction * multiplier * condition_multiplier

        st.success(f"The estimated car price is: {final_price:,.2f} EGP")

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")