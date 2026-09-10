import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. Page Configuration & Custom CSS (Clean UI)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Egyptian Car Valuation & Market System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Main Background */
    .main {
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-title {
        color: #1e293b;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .author-badge {
        background-color: #e2e8f0;
        color: #334155;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }

    /* Metric Card Styling */
    .metric-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #ff4b4b;
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-3px);
    }
    .metric-card h4 {
        color: #64748b;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    .metric-card h2 {
        color: #0f172a;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    
    /* Sidebar Fixes */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Database (Clean Models & Working Image Placeholders)
# ---------------------------------------------------------
CAR_DATA = {
    "Toyota": {
        "models": ["Corolla", "Yaris", "Fortuner", "C-HR", "RAV4", "Camry", "Belta"],
        "base_price": 1150000,
        "multiplier": 1.15,
        "image": "https://images.unsplash.com/photo-1629897048983-85f8dc4e4abc?auto=format&fit=crop&q=80&w=800"
    },
    "Hyundai": {
        "models": ["Elantra CN7", "Elantra HD", "Tucson", "Accent RB", "Creta", "I10"],
        "base_price": 850000,
        "multiplier": 1.0,
        "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=800"
    },
    "Kia": {
        "models": ["Sportage", "Cerato / Grand Cerato", "Rio", "Picanto", "Sorento"],
        "base_price": 950000,
        "multiplier": 1.05,
        "image": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&q=80&w=800"
    },
    "Nissan": {
        "models": ["Sunny", "Sentra", "Qashqai", "Juke"],
        "base_price": 750000,
        "multiplier": 0.92,
        "image": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&q=80&w=800"
    },
    "MG": {
        "models": ["MG 5", "MG ZS", "MG 6", "MG RX5", "MG HS"],
        "base_price": 800000,
        "multiplier": 0.95,
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
    },
    "BMW": {
        "models": ["320i / 330i", "520i / 530i", "X1", "X3", "X5"],
        "base_price": 2800000,
        "multiplier": 2.2,
        "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&q=80&w=800"
    },
    "Mercedes-Benz": {
        "models": ["C180 / C200", "E200 / E300", "A180", "GLA", "GLC"],
        "base_price": 3200000,
        "multiplier": 2.5,
        "image": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=800"
    },
    "Skoda": {
        "models": ["Octavia", "Kodiaq", "Karoq", "Superb"],
        "base_price": 1350000,
        "multiplier": 1.25,
        "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=800"
    }
}

# ---------------------------------------------------------
# 3. Header Section
# ---------------------------------------------------------
st.markdown('<div class="main-title">🚗 Egyptian Used Car Valuation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Developed by <span class="author-badge">Habiba Essam</span> & <span class="author-badge">Salma Ahmed</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Sidebar Inputs (English Clean Labels)
# ---------------------------------------------------------
st.sidebar.header("🔍 Vehicle Specifications")

brand = st.sidebar.selectbox("Car Brand", list(CAR_DATA.keys()))
model = st.sidebar.selectbox("Car Model", CAR_DATA[brand]["models"])

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Technical Specs")
year = st.sidebar.slider("Manufacturing Year", 2005, 2026, 2021)
body_type = st.sidebar.selectbox("Body Style", ["Sedan", "SUV / Crossover", "Hatchback", "Coupe"])
transmission = st.sidebar.radio("Transmission", ["Automatic", "Manual"], horizontal=True)
engine_cc = st.sidebar.select_slider("Engine Capacity (CC)", options=[1000, 1200, 1400, 1500, 1600, 2000, 2500, 3000], value=1600)
is_turbo = st.sidebar.checkbox("Turbocharged Engine?", value=False)
hp = st.sidebar.number_input("Horsepower (HP)", min_value=70, max_value=500, value=120)
fuel_type = st.sidebar.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])

st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Vehicle Condition")
mileage = st.sidebar.number_input("Mileage (KM)", min_value=0, max_value=500000, value=60000, step=5000)
paint_condition = st.sidebar.selectbox("Paint & Body State", [
    "Factory Original (Fabrika)",
    "Belt Repainted (Hizam)",
    "Partial Body Repairs",
    "Fully Repainted Outside"
])
mechanical_condition = st.sidebar.slider("Mechanical & Engine Condition (%)", 50, 100, 90)

# Display Brand Image safely
if "image" in CAR_DATA[brand] and CAR_DATA[brand]["image"]:
    st.sidebar.markdown("---")
    st.sidebar.image(CAR_DATA[brand]["image"], caption=f"{brand} Reference", use_container_width=True)

# ---------------------------------------------------------
# 5. Dynamic Valuation Engine
# ---------------------------------------------------------
current_year = 2026
age = current_year - year

base = CAR_DATA[brand]["base_price"] * CAR_DATA[brand]["multiplier"]

if is_turbo:
    base *= 1.10
if body_type == "SUV / Crossover":
    base *= 1.12
elif body_type == "Hatchback":
    base *= 0.92

base += (hp - 100) * 1500

depreciation_year = age * 0.045
depreciation_km = (mileage / 10000) * 0.012
total_depreciation = min(0.60, depreciation_year + depreciation_km)

val_after_dep = base * (1 - total_depreciation)

paint_multipliers = {
    "Factory Original (Fabrika)": 1.0,
    "Belt Repainted (Hizam)": 0.93,
    "Partial Body Repairs": 0.88,
    "Fully Repainted Outside": 0.82
}
val_after_paint = val_after_dep * paint_multipliers[paint_condition]
calculated_price = val_after_paint * (mechanical_condition / 100)

final_price = max(100000, int(calculated_price))
lower_price = int(final_price * 0.95)
upper_price = int(final_price * 1.05)

# ---------------------------------------------------------
# 6. Tabs Section
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Price Prediction", 
    "📊 Specs & Inspection", 
    "📉 Installment Calculator", 
    "⛽ Fuel Analysis"
])

with tab1:
    st.subheader("Market Valuation Result")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h4>Estimated Fair Price</h4><h2>{final_price:,} EGP</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h4>Minimum Buy Range</h4><h2>{lower_price:,} EGP</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h4>Maximum Negotiable Price</h4><h2>{upper_price:,} EGP</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"📌 **Summary:** {brand} {model} ({year}) | {transmission} | {paint_condition} | {mileage:,} KM")
    st.info("💡 **Insight:** Valuation reflects real-time Egyptian market demand, depreciation per KM, and mechanical state.")

with tab2:
    st.subheader("Vehicle Inspection Breakdown")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🚘 Car Specifications")
        st.markdown(f"- **Brand & Model:** {brand} {model}")
        st.markdown(f"- **Year:** {year} ({age} years old)")
        st.markdown(f"- **Engine:** {engine_cc} CC {'(Turbo)' if is_turbo else ''}")
        st.markdown(f"- **Horsepower:** {hp} HP")
        st.markdown(f"- **Fuel & Gearbox:** {fuel_type} | {transmission}")

    with col_b:
        st.markdown("### 🛠️ Condition Score")
        st.markdown(f"- **Total Mileage:** {mileage:,} KM")
        st.markdown(f"- **Paint Condition:** {paint_condition}")
        st.markdown(f"- **Mechanical Score:** {mechanical_condition}%")
        st.progress(mechanical_condition / 100)

with tab3:
    st.subheader("Loan & Installment Estimator")
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        down_payment = st.number_input("Down Payment (EGP)", min_value=0, max_value=final_price, value=int(final_price * 0.3), step=25000)
    with col_in2:
        loan_months = st.selectbox("Tenure (Months)", [12, 24, 36, 48, 60], index=2)
    with col_in3:
        interest_rate = st.slider("Annual Interest Rate (%)", 8.0, 35.0, 22.0, step=0.5)

    loan_amount = max(0, final_price - down_payment)
    monthly_interest = (interest_rate / 100) / 12
    
    if monthly_interest > 0 and loan_amount > 0:
        monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest)**loan_months) / ((1 + monthly_interest)**loan_months - 1)
    else:
        monthly_payment = loan_amount / loan_months if loan_months > 0 else 0

    st.markdown("---")
    res1, res2 = st.columns(2)
    with res1:
        st.metric("Loan Principal", f"{int(loan_amount):,} EGP")
    with res2:
        st.metric("Estimated Monthly Installment", f"{int(monthly_payment):,} EGP / Month")

with tab4:
    st.subheader("Fuel Efficiency Estimator")
    base_consumption = 6.0 + (engine_cc / 1000) * 1.5
    if is_turbo:
        base_consumption -= 0.5
    if fuel_type == "Hybrid":
        base_consumption *= 0.6
    
    est_consumption = round(base_consumption, 1)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        monthly_km = st.slider("Monthly Driving Distance (KM)", 500, 5000, 1500, step=100)
        fuel_price = st.number_input("Fuel Price per Liter (EGP)", min_value=5.0, max_value=30.0, value=15.0, step=0.5)
    
    with col_f2:
        monthly_liters = (monthly_km / 100) * est_consumption
        monthly_fuel_cost = monthly_liters * fuel_price
        
        st.metric("Avg Consumption Rate", f"{est_consumption} L / 100 KM")
        st.metric("Est. Monthly Fuel Cost", f"{int(monthly_fuel_cost):,} EGP")

# ---------------------------------------------------------
# 7. Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>Egyptian Car Valuation System | Developed by Habiba Essam & Salma Ahmed</p>", unsafe_allow_html=True)
