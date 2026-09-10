import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. Page Configuration & Modern CSS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Egyptian Ultimate Car Valuation System",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Global Typography & Light Clean Background */
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Main Title Header */
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

    /* Price Displays */
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
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Detailed Egyptian Market Database with Trim Specifics
# ---------------------------------------------------------
CAR_DATA = {
    "Toyota": {
        "models": {
            "Corolla": 1500000,
            "Yaris": 1100000,
            "Fortuner": 3300000,
            "C-HR": 1650000,
            "Belta": 850000,
            "Rumion": 900000
        },
        "image": "https://images.unsplash.com/photo-1629897048983-85f8dc4e4abc?auto=format&fit=crop&q=80&w=800"
    },
    "Hyundai": {
        "models": {
            "Elantra CN7": 1550000,
            "Elantra HD": 900000,
            "Elantra AD": 1150000,
            "Tucson": 1950000,
            "Accent RB": 820000,
            "Creta": 1400000
        },
        "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=800"
    },
    "Kia": {
        "models": {
            "Sportage": 2050000,
            "Cerato / Grand Cerato": 1250000,
            "Rio": 950000,
            "Picanto": 750000,
            "Sorento": 3100000
        },
        "image": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&q=80&w=800"
    },
    "Nissan": {
        "models": {
            "Sunny": 750000,
            "Sentra": 950000,
            "Qashqai": 1550000,
            "Juke": 1150000
        },
        "image": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&q=80&w=800"
    },
    "MG": {
        "models": {
            "MG 5": 880000,
            "MG ZS": 1050000,
            "MG 6": 1250000,
            "MG RX5 / RX5 Plus": 1450000,
            "MG HS": 1600000
        },
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
    },
    "Chery": {
        "models": {
            "Arrizo 5": 780000,
            "Tiggo 3": 850000,
            "Tiggo 7": 1120000,
            "Tiggo 8": 1450000,
            "Omoda C5": 1400000
        },
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=800"
    },
    "BMW": {
        "models": {
            "320i": 2900000,
            "330i": 3500000,
            "520i": 4200000,
            "X1": 2600000,
            "X3": 3900000,
            "X5": 5800000
        },
        "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&q=80&w=800"
    },
    "Mercedes-Benz": {
        "models": {
            "C180": 3200000,
            "C200": 3800000,
            "E200": 4800000,
            "A180": 2200000,
            "GLA": 2700000,
            "GLC": 4500000
        },
        "image": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=800"
    },
    "Skoda": {
        "models": {
            "Octavia": 1750000,
            "Kodiaq": 2450000,
            "Karoq": 1850000,
            "Superb": 2100000
        },
        "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=800"
    },
    "Komodo": {
        "models": {
            "Komodo 2.4 4x2": 480000,
            "Komodo 2.4 4x4": 560000
        },
        "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=800"
    }
}

TRIM_MULTIPLIERS = {
    "Base Line (الفئة الأولى)": 0.92,
    "Mid Line (الفئة الثانية / المتواسطة)": 1.0,
    "High Line / Elegance (الفئة الأولى المجهزة)": 1.08,
    "Topline / Sport / Luxury (أعلى فئة)": 1.15
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
# 4. Input Configuration Section
# ---------------------------------------------------------
with st.expander("⚙️ **Configure Vehicle Specs & Trim**", expanded=True):
    col_in1, col_in2 = st.columns(2)
    
    with col_in1:
        brand = st.selectbox("Car Brand", list(CAR_DATA.keys()))
        model = st.selectbox("Car Model", list(CAR_DATA[brand]["models"].keys()))
        trim = st.selectbox("Trim / Category Tier (فئة السيارة)", list(TRIM_MULTIPLIERS.keys()), index=1)
        year = st.slider("Model Year", 2005, 2026, 2021)

    with col_in2:
        transmission = st.radio("Transmission", ["Automatic", "Manual"], horizontal=True)
        mileage = st.number_input("Mileage (KM)", min_value=0, max_value=500000, value=60000, step=5000)
        paint_condition = st.selectbox("Body / Paint Condition", [
            "Factory Original (Fabrika)",
            "Belt Repainted (Hizam)",
            "Partial Repairs",
            "Fully Repainted"
        ])
        mechanical_condition = st.slider("Mechanical Condition (%)", 50, 100, 90)

    # Car image preview
    st.image(CAR_DATA[brand]["image"], caption=f"{brand} Reference Model", use_container_width=True)

    # Advanced Specifications
    with st.popover("🔧 Advanced Engine Options"):
        engine_cc = st.select_slider("Engine CC", options=[1000, 1200, 1400, 1500, 1600, 2000, 2500, 3000], value=1600)
        is_turbo = st.checkbox("Turbocharged Engine?", value=False)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"])

# ---------------------------------------------------------
# 5. Precise Market Calculation Engine
# ---------------------------------------------------------
current_year = 2026
age = current_year - year

# Model Base Price
model_base_2026 = CAR_DATA[brand]["models"][model]

# Apply Trim Multiplier
model_price_with_trim = model_base_2026 * TRIM_MULTIPLIERS[trim]

# Adjust for Turbo or Transmission
if is_turbo:
    model_price_with_trim *= 1.05
if transmission == "Manual":
    model_price_with_trim *= 0.88

# Depreciation Curve (~3.8% yearly for clean cars)
depreciation = min(0.60, (age * 0.038) + ((mileage / 10000) * 0.009))
val_after_dep = model_price_with_trim * (1 - depreciation)

# Paint Condition Penalty
paint_rates = {
    "Factory Original (Fabrika)": 1.0,
    "Belt Repainted (Hizam)": 0.93,
    "Partial Repairs": 0.88,
    "Fully Repainted": 0.80
}
val_after_paint = val_after_dep * paint_rates[paint_condition]

# Final Valuation Calculation
final_price = max(80000, int(val_after_paint * (mechanical_condition / 100)))

lower_price = int(final_price * 0.95)
upper_price = int(final_price * 1.05)

# ---------------------------------------------------------
# 6. Price Valuation Display
# ---------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Main Fair Price Card
st.markdown(f'''
    <div class="price-card-main">
        <h4>Estimated Market Value ({trim.split('(')[0].strip()})</h4>
        <h2>{final_price:,} EGP</h2>
    </div>
''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Min & Max Buying Range
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
        interest = st.slider("Interest Rate (%)", 8.0, 35.0, 22.0, step=0.5)
        loan = max(0, final_price - down_pay)
        r = (interest / 100) / 12
        monthly = loan * (r * (1 + r)**months) / ((1 + r)**months - 1) if r > 0 and loan > 0 else loan / months
        
        st.metric("Monthly Payment", f"{int(monthly):,} EGP")

with tab2:
    f1, f2 = st.columns(2)
    with f1:
        monthly_km = st.slider("Monthly Distance (KM)", 500, 5000, 1500, step=100)
    with f2:
        fuel_price = st.number_input("Fuel Price / Liter (EGP)", value=17.0, step=0.5)
        cost = (monthly_km / 100) * 8.5 * fuel_price
        st.metric("Monthly Fuel Cost", f"{int(cost):,} EGP")

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.8rem;'>Egyptian Used Car Valuation System • Updated Precise Trim Rates</p>", unsafe_allow_html=True)
