
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Car Price Predictor", page_icon="🚗", layout="centered"
)


@st.cache_resource
def load_model():
    return joblib.load("car_price_pipeline.pkl")


pipeline = load_model()

st.title("🚗 Used Car Price Prediction System")

st.markdown("---")
st.markdown("👩‍💻 **Developed by:** Habiba Essam & Salma Ahmed")
st.markdown("---")

st.write("Enter the car specifications to get the estimated price.")

brand = st.selectbox(
    "Car Brand",
    ["Toyota", "Hyundai", "Kia", "Nissan", "Chevrolet", "BMW", "Mercedes"],
)
car_type = st.selectbox(
    "Car Type / Model", ["Sedan", "SUV", "Hatchback", "Coupe"]
)
transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

# إضافة خيار حالة السيارة (زيرو / كسر زيرو / مستعمل)
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
    # لو اختار زيرو تلقائياً بنخلي العداد 0، غير كدة يقدر يكتب الممشى
    if car_condition == "Zero (Brand New)":
        km_driven = 0
        st.info("Kilometers Driven: 0 KM (Brand New)")
    else:
        km_driven = st.number_input(
            "Kilometers Driven (KM)", min_value=0, max_value=500000, value=5000
        )

st.markdown("---")

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

        # 1. معامل تصحيح الماركة والسنة
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

        # 2. معامل حالة السيارة (Zero / Nearly New / Used)
        if car_condition == "Zero (Brand New)":
            condition_multiplier = 1.25  # زيادة 25% للزيرو
        elif car_condition == "Nearly New (كسر زيرو)":
            condition_multiplier = 1.10  # زيادة 10% لكسر الزيرو
        else:
            condition_multiplier = 1.0  # المستعمل العادي

        # حساب السعر النهائي
        final_price = base_prediction * multiplier * condition_multiplier

        st.success(f"The estimated car price is: {final_price:,.2f} EGP")

    except Exception as e:
        st.error(
            "An error occurred during prediction: Make sure model columns match"
            f" input. Details: {e}"
        )