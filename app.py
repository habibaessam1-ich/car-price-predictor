import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Car Price Predictor", page_icon="🚗", layout="centered"
)

# --- إضافة CSS لتخصيص الألوان والستايل بشكل إضافي ---
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    .stSuccess {
        background-color: #1b3820;
        border: 1px solid #2E7D32;
    }
    </style>
""",
    unsafe_allow_html=True,
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

        # Multiplier
        if brand in ["BMW", "Mercedes"]:
            multiplier = 6.5 if year >= 2021 else (4.5 if year >= 2017 else 3.0)
        else:
            multiplier = (
                3.2
                if year >= 2022
                else (1.8 if year >= 2012 else 1.3)
            )

        condition_multiplier = (
            1.25
            if car_condition == "Zero (Brand New)"
            else (1.10 if car_condition == "Nearly New (كسر زيرو)" else 1.0)
        )

        final_price = base_prediction * multiplier * condition_multiplier

        # حساب نطاق السعر (Min / Max Range)
        min_price = final_price * 0.95
        max_price = final_price * 1.05

        st.success(f"**Estimated Price:** {final_price:,.2f} EGP")
        st.info(
            f"💡 **Expected Market Range:** {min_price:,.2f} - {max_price:,.2f}"
            " EGP"
        )

        # 1. إمكانية تحميل التقرير (Download Report Option)
        report_data = input_data.copy()
        report_data["Estimated_Price_EGP"] = final_price
        csv = report_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📄 Download Valuation Report (CSV)",
            data=csv,
            file_name=f"car_valuation_{brand}_{year}.csv",
            mime="text/csv",
        )

        # 2. حاسبة التقسيط السريعة (Finance Calculator Option)
        with st.expander("💳 Estimated Monthly Installment Calculator"):
            down_payment_pct = st.slider(
                "Down Payment (%)", 10, 50, 20
            )
            years = st.selectbox("Loan Duration (Years)", [1, 2, 3, 4, 5])

            loan_amount = final_price * (1 - (down_payment_pct / 100))
            monthly_payment = (
                loan_amount * (1 + 0.15 * years)
            ) / (years * 12)  # افتراض فائدة 15% سنوية

            st.write(f"**Estimated Monthly Payment:** {monthly_payment:,.2f} EGP/month")

    except Exception as e:
        st.error(f"Error during prediction: {e}")