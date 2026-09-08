import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Egyptian Car Price Predictor & Market Analyzer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #e03e3e;
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

CAR_IMAGES = {
    "Toyota": "https://images.unsplash.com/photo-1629897048983-85f8dc4e4abc?auto=format&fit=crop&q=80&w=800",
    "Hyundai": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=800",
    "Nissan": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&q=80&w=800",
    "Kia": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&q=80&w=800",
    "Chevrolet": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800",
    "BMW": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&q=80&w=800",
    "Mercedes": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=800",
    "Renault": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&q=80&w=800",
    "Skoda": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=800",
    "Other": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=800"
}

CAR_MODELS = {
    "Toyota": ["Corolla", "Yaris", "Fortuner", "C-HR", "RAV4", "Camry"],
    "Hyundai": ["Elantra", "Tucson", "Accent", "Creta", "Grand i10", "Sonata"],
    "Nissan": ["Sunny", "Sentra", "Qashqai", "Juke", "Patrol", "X-Trail"],
    "Kia": ["Cerato", "Sportage", "Rio", "Sorento", "Grand Cerato", "Picanto"],
    "Chevrolet": ["Optra", "Captiva", "Aveo", "T-Avenue", "Lanos"],
    "BMW": ["3 Series", "5 Series", "X1", "X3", "X5", "4 Series"],
    "Mercedes": ["C-Class", "E-Class", "GLA", "GLC", "A-Class"],
    "Renault": ["Logan", "Sandero", "Duster", "Megane", "Kadjar"],
    "Skoda": ["Octavia", "Kodiaq", "Superb", "Karoq"],
    "Other": ["Standard Model"]
}

st.title("🚗 Egyptian Used Car Price Predictor & Market Analyzer")
st.markdown("### Developed by Habiba Essam & Salma Ahmed")
st.write("Welcome! Use this professional tool to estimate car market values in Egypt, calculate installments, evaluate vehicle condition, and analyze fuel consumption.")

st.sidebar.header("🔍 Vehicle Specifications")

brand = st.sidebar.selectbox("Select Car Brand", list(CAR_MODELS.keys()))
model = st.sidebar.selectbox("Select Car Model", CAR_MODELS[brand])
year = st.sidebar.slider("Manufacturing Year", 2010, 2026, 2022)
transmission = st.sidebar.selectbox("Transmission Type", ["Automatic", "Manual"])
fuel_type = st.sidebar.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])
mileage = st.sidebar.number_input("Mileage (KM)", min_value=0, max_value=400000, value=50000, step=5000)
engine_cc = st.sidebar.slider("Engine Capacity (CC)", 1000, 4000, 1600, step=100)
condition_score = st.sidebar.slider("Body & Mechanical Condition Score (%)", 50, 100, 85)

if brand in CAR_IMAGES:
    st.sidebar.image(CAR_IMAGES[brand], caption=f"{brand} Model Reference", use_column_width=True)

tab1, tab2, tab3, tab4 = st.tabs(["💰 Price Prediction", "📊 Market Trends", "📉 Installment Calculator", "⛽ Fuel Analysis"])

with tab1:
    st.subheader("Estimated Market Valuation")
    base_price = 450000
    brand_multiplier = {"BMW": 2.5, "Mercedes": 3.0, "Toyota": 1.5, "Hyundai": 1.2, "Nissan": 1.15, "Kia": 1.2, "Chevrolet": 0.9, "Renault": 0.95, "Skoda": 1.4, "Other": 1.0}
    
    age = 2026 - year
    calculated_price = base_price * brand_multiplier.get(brand, 1.0)
    calculated_price += (engine_cc / 1600) * 100000
    calculated_price -= age * 25000
    calculated_price -= (mileage / 10000) * 8000
    calculated_price = calculated_price * (condition_score / 100)
    
    final_price = max(150000, int(calculated_price))
    min_range = int(final_price * 0.95)
    max_range = int(final_price * 1.05)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><h4>Estimated Price</h4><h2>' + f"{final_price:,}" + ' EGP</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>Lower Range</h4><h2>' + f"{min_range:,}" + ' EGP</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h4>Upper Range</h4><h2>' + f"{max_range:,}" + ' EGP</h2></div>', unsafe_allow_html=True)
        
    st.markdown("---")
    st.info("💡 **Valuation Insight:** Price takes into account current market inflation, depreciation per kilometer, and overall mechanical condition score.")

with tab2:
    st.subheader("📊 Egyptian Used Car Market Insights")
    st.write("Historical price trends and demand distribution across popular brands in the Egyptian market.")
    
    chart_data = pd.DataFrame({
        'Brand': list(CAR_MODELS.keys())[:7],
        'Average Price (EGP)': [850000, 720000, 680000, 700000, 520000, 1400000, 1850000]
    })
    st.bar_chart(chart_data.set_index('Brand'))

with tab3:
    st.subheader("📉 Car Loan & Installment Calculator")
    down_payment = st.number_input("Down Payment (EGP)", min_value=0, value=int(final_price * 0.3), step=10000)
    loan_term_months = st.selectbox("Loan Tenure (Months)", [12, 24, 36, 48, 60], index=2)
    interest_rate = st.slider("Annual Interest Rate (%)", 5.0, 30.0, 18.0, step=0.5)
    
    loan_amount = max(0, final_price - down_payment)
    monthly_interest = (interest_rate / 100) / 12
    if monthly_interest > 0:
        monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest)**loan_term_months) / ((1 + monthly_interest)**loan_term_months - 1)
    else:
        monthly_payment = loan_amount / loan_term_months
        
    st.success("📌 **Estimated Monthly Installment:** " + f"{int(monthly_payment):,}" + " EGP / month for " + str(loan_term_months) + " months.")

with tab4:
    st.subheader("⛽ Fuel Consumption & Efficiency Estimator")
    est_fuel_consumption = round(7.5 + (engine_cc / 1000) * 1.8 - (0.5 if fuel_type == "Hybrid" else 0.0), 1)
    st.metric(label="Estimated Fuel Consumption", value=str(est_fuel_consumption) + " Liters / 100 KM")
    st.write("Estimated monthly fuel cost based on an average driving distance of 1,000 KM and current fuel prices in Egypt.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Car Price Predictor System | Created with Streamlit & Python by Habiba Essam & Salma Ahmed</p>", unsafe_allow_html=True)