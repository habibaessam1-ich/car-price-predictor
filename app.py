import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. Page Configuration & Modern CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Egyptian Used Car Predictor",
    page_icon="🚗",
    layout="centered",  # Optimal for mobile and desktop readability
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Global Typography & Colors */
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Remove padding issues on mobile */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Main Title Card */
    .hero-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    .hero-title {
        color: #0f172a;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: #64748b;
        font-size: 0.9rem;
    }
    .author-tag {
        color: #2563eb;
        font-weight: 600;
    }

    /* Price Cards */
    .price-card-main {
        background: #2563eb;
        color: white;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.2);
    }
    .price-card-main h4 {
        color: #93c5fd;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }
    .price-card-main h2 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }

    .price-card-sub {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .price-card-sub h4 {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .price-card-sub h3 {
        color: #1e293b;
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0;
    }

    /* Inputs Accordion Style */
    .stHeader {
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Database
# ---------------------------------------------------------
CAR_DATA = {
    "Toyota": {"models": ["Corolla", "Yaris", "Fortuner", "C-HR", "RAV4", "Belta"], "base": 1150000, "mult": 1.15},
    "Hyundai": {"models": ["Elantra CN7", "Elantra HD", "Tucson", "Accent RB", "Creta"], "base": 850000, "mult": 1.0},
    "Kia": {"models": ["Sportage", "Cerato", "Rio", "Picanto", "Sorento"], "base": 950000, "mult": 1.05},
    "Nissan": {"models": ["Sunny", "Sentra", "Qashqai", "Juke"], "base": 750000, "mult": 0.92},
    "MG": {"models": ["MG 5", "MG ZS", "MG 6", "MG RX5", "MG HS"], "base": 800000, "mult": 0.95},
    "BMW": {"models": ["320i / 330i", "520i / 530i", "X1", "X3", "X5"], "base": 2800000, "mult": 2.2},
    "Mercedes-Benz": {"models": ["C180 / C200", "E200 / E300", "A180", "GLC"], "base": 3200000, "mult": 2.5},
    "Skoda": {"models": ["Octavia", "Kodiaq", "Karoq", "Superb"], "base": 1350000, "mult": 1.25}
}

# ---------------------------------------------------------
# 3. Header Section
# ---------------------------------------------------------
st.markdown("""
    <div class="hero-card">
        <div class="hero-title">🚗 Egyptian Used Car Predictor</div>
        <div class="hero-sub">Smart Market Valuation | By <span class="author-tag">Habiba Essam</span> & <span class="author-tag">Salma Ahmed</span></div>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Inputs Section (Expander for Clean UI)
# ---------------------------------------------------------
with st.expander("⚙️ **Configure Vehicle Specs & Condition**", expanded=True):
    col_in1, col_in2 = st.columns(2)
    
    with col_in1:
        brand = st.selectbox("Car Brand", list(CAR_DATA.keys()))
        model = st.selectbox("Car Model", CAR_DATA[brand]["models"])
        year = st.slider("Model Year", 2005, 2026, 2021)
        transmission = st.radio("Transmission", ["Automatic", "Manual"], horizontal=True)

    with col_in2:
        mileage = st.number_input("Mileage (KM)", min_value=0, max_value=500000, value=60000, step=5000)
        paint_condition = st.selectbox("Body / Paint Condition", [
            "Factory Original (Fabrika)",
            "Belt Repainted (Hizam)",
            "Partial Repairs",
            "Fully Repainted"
        ])
        mechanical_condition = st.slider("Mechanical Condition (%)", 50, 100, 90)

    # Advanced Specs Option
    with st.popover("🔧 Advanced Options (Engine & Fuel)"):
        engine_cc = st.select_slider("Engine CC", options=[1000, 1200, 1400, 1500, 1600, 2000, 2500, 3000], value=1600)
        is_turbo = st.checkbox("Turbocharged Engine?", value=False)
        hp = st.number_input("Horsepower (HP)", min_value=70, max_value=500, value=120)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])
        body_type = st.selectbox("Body Style", ["Sedan", "SUV / Crossover", "Hatchback", "Coupe"])

# ---------------------------------------------------------
# 5. Calculation Logic
# ---------------------------------------------------------
current_year = 2026
age = current_year - year
base_price = CAR_DATA[brand]["base"] * CAR_DATA[brand]["mult"]

if is_turbo:
    base_price *= 1.10
if body_type == "SUV / Crossover":
    base_price *= 1.12

base_price += (hp - 100) * 1500

depreciation = min(0.60, (age * 0.045) + ((mileage / 10000) * 0.012))
val_after_dep = base_price * (1 - depreciation)

paint_rates = {
    "Factory Original (Fabrika)": 1.0,
    "Belt Repainted (Hizam)": 0.93,
    "Partial Repairs": 0.88,
    "Fully Repainted": 0.82
}
val_after_paint = val_after_dep * paint_rates[paint_condition]
final_price = max(100000, int(val_after_paint * (mechanical_condition / 100)))

lower_price = int(final_price * 0.95)
upper_price = int(final_price * 1.05)

# ---------------------------------------------------------
# 6. Clean Valuation Display
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Main Fair Price Metric
st.markdown(f'''
    <div class="price-card-main">
        <h4>Estimated Market Value</h4>
        <h2>{final_price:,} EGP</h2>
    </div>
''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Min and Max Range Cards
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.markdown(f'''
        <div class="price-card-sub">
            <h4>Min Buying Price</h4>
            <h3>{lower_price:,} EGP</h3>
        </div>
    ''', unsafe_allow_html=True)

with col_res2:
    st.markdown(f'''
        <div class="price-card-sub">
            <h4>Max Negotiable</h4>
            <h3>{upper_price:,} EGP</h3>
        </div>
    ''', unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. Additional Tools (Tabs)
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📉 Installment Calculator", "⛽ Fuel Estimator"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        down_pay = st.number_input("Down Payment (EGP)", min_value=0, max_value=final_price, value=int(final_price * 0.3), step=25000)
        months = st.selectbox("Tenure (Months)", [12, 24, 36, 48, 60], index=2)
    with c2:
        interest = st.slider("Interest Rate (%)", 8.0, 30.0, 20.0, step=0.5)
        loan = max(0, final_price - down_pay)
        r = (interest / 100) / 12
        monthly = loan * (r * (1 + r)**months) / ((1 + r)**months - 1) if r > 0 and loan > 0 else loan / months
        
        st.metric("Monthly Payment", f"{int(monthly):,} EGP")

with tab2:
    f1, f2 = st.columns(2)
    with f1:
        monthly_km = st.slider("Monthly Distance (KM)", 500, 5000, 1500, step=100)
    with f2:
        fuel_price = st.number_input("Fuel Price / Liter (EGP)", value=15.0, step=0.5)
        cost = (monthly_km / 100) * 8.0 * fuel_price
        st.metric("Monthly Fuel Cost", f"{int(cost):,} EGP")

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Egyptian Used Car Valuation System • 2026</p>", unsafe_allow_html=True)
