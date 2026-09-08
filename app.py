import io
import json
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Car Price Predictor Pro - Ultimate Edition",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Comprehensive Car Database (All Brands, Models, and Engine Options)
CAR_MODELS = {
    "Toyota": {
        "Corolla": {
            "engines": ["1.6L Normal", "1.8L Hybrid"],
            "base_price": 1600000,
            "body": "Sedan",
            "hp": 120,
        },
        "Yaris": {
            "engines": ["1.5L Normal"],
            "base_price": 1000000,
            "body": "Hatchback",
            "hp": 118,
        },
        "Fortuner": {
            "engines": ["2.7L Normal", "4.0L V6"],
            "base_price": 3800000,
            "body": "SUV",
            "hp": 234,
        },
        "C-HR": {
            "engines": ["1.2L Turbo", "1.8L Hybrid"],
            "base_price": 1750000,
            "body": "SUV",
            "hp": 113,
        },
        "Belta": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 103,
        },
    },
    "Nissan": {
        "Sunny": {
            "engines": ["1.5L Normal"],
            "base_price": 800000,
            "body": "Sedan",
            "hp": 108,
        },
        "Sentra": {
            "engines": ["1.6L Normal"],
            "base_price": 1100000,
            "body": "Sedan",
            "hp": 118,
        },
        "Qashqai": {
            "engines": ["1.3L Turbo"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 148,
        },
        "Juke": {
            "engines": ["1.0L Turbo"],
            "base_price": 1300000,
            "body": "SUV",
            "hp": 114,
        },
    },
    "Hyundai": {
        "Elantra": {
            "engines": ["1.6L Normal"],
            "base_price": 1300000,
            "body": "Sedan",
            "hp": 127,
        },
        "Tucson": {
            "engines": ["1.6L Turbo"],
            "base_price": 1900000,
            "body": "SUV",
            "hp": 180,
        },
        "Accent": {
            "engines": ["1.4L Normal"],
            "base_price": 900000,
            "body": "Sedan",
            "hp": 100,
        },
        "Creta": {
            "engines": ["1.5L Normal"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 113,
        },
        "i10": {
            "engines": ["1.2L Normal"],
            "base_price": 700000,
            "body": "Hatchback",
            "hp": 84,
        },
    },
    "Kia": {
        "Cerato / K3": {
            "engines": ["1.6L Normal"],
            "base_price": 1350000,
            "body": "Sedan",
            "hp": 130,
        },
        "Sportage": {
            "engines": ["1.6L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 177,
        },
        "Pegas": {
            "engines": ["1.4L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 95,
        },
        "Seltos": {
            "engines": ["1.4L Turbo", "1.5L Normal"],
            "base_price": 1500000,
            "body": "SUV",
            "hp": 140,
        },
    },
    "MG": {
        "MG 5": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 118,
        },
        "MG 6": {
            "engines": ["1.5L Turbo"],
            "base_price": 1200000,
            "body": "Sedan",
            "hp": 169,
        },
        "MG ZS": {
            "engines": ["1.5L Normal"],
            "base_price": 1050000,
            "body": "SUV",
            "hp": 119,
        },
        "MG RX5": {
            "engines": ["1.5L Turbo"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 171,
        },
        "MG 4 EV": {
            "engines": ["Electric EV"],
            "base_price": 1350000,
            "body": "Hatchback",
            "hp": 170,
        },
    },
    "Chery": {
        "Arrizo 5": {
            "engines": ["1.5L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 114,
        },
        "Tiggo 3": {
            "engines": ["1.6L Normal"],
            "base_price": 880000,
            "body": "SUV",
            "hp": 126,
        },
        "Tiggo 7": {
            "engines": ["1.5L Turbo"],
            "base_price": 1100000,
            "body": "SUV",
            "hp": 145,
        },
        "Tiggo 8 Pro": {
            "engines": ["1.5L Turbo", "1.6L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 145,
        },
    },
    "BYD": {
        "F3": {
            "engines": ["1.5L Normal"],
            "base_price": 620000,
            "body": "Sedan",
            "hp": 108,
        },
        "Song Plus Hybrid": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1600000,
            "body": "SUV",
            "hp": 197,
        },
    },
    "Changan": {
        "Alsvin": {
            "engines": ["1.4L Normal", "1.5L Normal"],
            "base_price": 650000,
            "body": "Sedan",
            "hp": 107,
        },
        "CS35 Plus": {
            "engines": ["1.4L Turbo"],
            "base_price": 1150000,
            "body": "SUV",
            "hp": 158,
        },
        "CS55 Plus": {
            "engines": ["1.5L Turbo"],
            "base_price": 1350000,
            "body": "SUV",
            "hp": 185,
        },
    },
    "Geely": {
        "Emgrand": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 102,
        },
        "Coolray": {
            "engines": ["1.5L Turbo"],
            "base_price": 1300000,
            "body": "SUV",
            "hp": 175,
        },
        "Okavango": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 190,
        },
    },
    "Skoda": {
        "Octavia": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 1850000,
            "body": "Sedan",
            "hp": 150,
        },
        "Kodiaq": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 2600000,
            "body": "SUV",
            "hp": 150,
        },
        "Karoq": {
            "engines": ["1.4L Turbo"],
            "base_price": 2100000,
            "body": "SUV",
            "hp": 150,
        },
        "Scala": {
            "engines": ["1.6L Normal"],
            "base_price": 1300000,
            "body": "Hatchback",
            "hp": 110,
        },
    },
    "BMW": {
        "3 Series (320i)": {
            "engines": ["2.0L Turbo"],
            "base_price": 3500000,
            "body": "Sedan",
            "hp": 184,
        },
        "5 Series (520i)": {
            "engines": ["2.0L Turbo"],
            "base_price": 4800000,
            "body": "Sedan",
            "hp": 184,
        },
        "X1": {
            "engines": ["1.5L Turbo"],
            "base_price": 2900000,
            "body": "SUV",
            "hp": 140,
        },
        "X5": {
            "engines": ["3.0L Turbo"],
            "base_price": 6200000,
            "body": "SUV",
            "hp": 340,
        },
    },
    "Mercedes-Benz": {
        "C-Class (C180 / C200)": {
            "engines": ["1.5L Turbo", "2.0L Turbo"],
            "base_price": 4200000,
            "body": "Sedan",
            "hp": 170,
        },
        "E-Class (E200)": {
            "engines": ["2.0L Turbo"],
            "base_price": 5800000,
            "body": "Sedan",
            "hp": 197,
        },
        "GLC": {
            "engines": ["2.0L Turbo"],
            "base_price": 5900000,
            "body": "SUV",
            "hp": 204,
        },
        "A-Class": {
            "engines": ["1.3L Turbo"],
            "base_price": 2700000,
            "body": "Hatchback",
            "hp": 136,
        },
    },
    "Audi": {
        "A4": {
            "engines": ["2.0L Turbo"],
            "base_price": 2800000,
            "body": "Sedan",
            "hp": 190,
        },
        "A6": {
            "engines": ["2.0L Turbo"],
            "base_price": 3900000,
            "body": "Sedan",
            "hp": 245,
        },
        "Q3": {
            "engines": ["1.4L Turbo"],
            "base_price": 2500000,
            "body": "SUV",
            "hp": 150,
        },
        "Q7": {
            "engines": ["3.0L Turbo"],
            "base_price": 4900000,
            "body": "SUV",
            "hp": 340,
        },
    },
    "Chevrolet": {
        "Optra": {
            "engines": ["1.5L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 110,
        },
        "Captiva": {
            "engines": ["1.5L Turbo"],
            "base_price": 1500000,
            "body": "SUV",
            "hp": 148,
        },
        "Aveo": {
            "engines": ["1.5L Normal"],
            "base_price": 600000,
            "body": "Sedan",
            "hp": 105,
        },
    },
    "Renault": {
        "Megane": {
            "engines": ["1.6L Normal", "1.3L Turbo"],
            "base_price": 1400000,
            "body": "Sedan",
            "hp": 115,
        },
        "Logan": {
            "engines": ["1.6L Normal"],
            "base_price": 650000,
            "body": "Sedan",
            "hp": 110,
        },
        "Duster": {
            "engines": ["1.6L Normal"],
            "base_price": 1200000,
            "body": "SUV",
            "hp": 115,
        },
        "Sandero Stepway": {
            "engines": ["1.6L Normal"],
            "base_price": 850000,
            "body": "Hatchback",
            "hp": 110,
        },
    },
    "Fiat": {
        "Tipo": {
            "engines": ["1.4L Normal", "1.6L Normal"],
            "base_price": 1050000,
            "body": "Sedan",
            "hp": 110,
        },
        "500": {
            "engines": ["1.4L Normal"],
            "base_price": 1100000,
            "body": "Hatchback",
            "hp": 100,
        },
    },
    "Peugeot": {
        "301": {
            "engines": ["1.6L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 115,
        },
        "508": {
            "engines": ["1.6L Turbo"],
            "base_price": 1800000,
            "body": "Sedan",
            "hp": 165,
        },
        "2008": {
            "engines": ["1.2L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 130,
        },
        "3008": {
            "engines": ["1.6L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 180,
        },
        "5008": {
            "engines": ["1.6L Turbo"],
            "base_price": 2200000,
            "body": "SUV",
            "hp": 180,
        },
    },
    "Suzuki": {
        "Swift": {
            "engines": ["1.2L Normal"],
            "base_price": 750000,
            "body": "Hatchback",
            "hp": 84,
        },
        "Ciaz / Dzire": {
            "engines": ["1.2L Normal", "1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 104,
        },
        "Ertiga": {
            "engines": ["1.5L Normal"],
            "base_price": 950000,
            "body": "Van",
            "hp": 103,
        },
    },
}

# Session State Initialization
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar Navigation
st.sidebar.title("🛠️ Control Panel")
app_mode = st.sidebar.selectbox(
    "Choose Section:",
    [
        "Price Predictor",
        "Car Comparison",
        "Budget Finder",
        "Search History",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 **Developers:** Salma Ahmed & Habiba Essam")

# ================= 1. Price Predictor Section =================
if app_mode == "Price Predictor":
    st.title("🚗 Advanced Car Price Prediction System")
    st.markdown(
        "Select the brand, model, engine option, and extras to estimate the market price."
    )
    st.markdown("---")

    col_input, col_info_box = st.columns([1.3, 1])

    with col_input:
        brand = st.selectbox("Car Brand", sorted(list(CAR_MODELS.keys())))
        available_models = list(CAR_MODELS[brand].keys())
        model_name = st.selectbox("Car Model", available_models)

        car_data = CAR_MODELS[brand][model_name]

        # Engine selection
        selected_engine = st.selectbox(
            "Engine Capacity & Type", car_data["engines"]
        )

        transmission = st.selectbox(
            "Transmission", ["Automatic", "Manual"]
        )

        year = st.slider("Manufacturing Year", 2010, 2026, 2022)

        car_condition = st.radio(
            "Car Condition",
            ["Brand New (Zero)", "Nearly New", "Used in Good Condition"],
            horizontal=True,
        )

        if car_condition == "Brand New (Zero)":
            km_driven = 0
            st.info("Car is brand new (0 KM)")
        else:
            km_driven = st.number_input(
                "Kilometers Driven (KM)",
                min_value=0,
                max_value=400000,
                value=50000,
                step=5000,
            )

    with col_info_box:
        st.subheader("✨ Car Extras & Options")
        st.markdown("Check available features in the car:")

        has_sunroof = st.checkbox("☀️ Sunroof / Panoramic Glass (+2.5%)")
        has_leather = st.checkbox("💺 Leather Seats (+1.5%)")
        has_start_engine = st.checkbox(
            "🔑 Push Start Button & Smart Key (+1.5%)"
        )
        has_sensors_cam = st.checkbox(
            "📷 Rear Camera & Parking Sensors (+1.5%)"
        )
        has_alloy_wheels = st.checkbox("🛞 Original Alloy Wheels (+1%)")
        has_screens = st.checkbox("📱 Smart Media Display (+1%)")

        st.markdown("---")
        st.info(
            f"ℹ️ **Base Specs:**\n- Body Type: `{car_data['body']}`\n- Horsepower: `{car_data['hp']} HP`\n- Selected Engine: `{selected_engine}`"
        )

    st.markdown("---")

    if st.button("🚀 Calculate Estimated Price"):
        base_price = car_data["base_price"]

        # Adjust price based on engine type
        if "Turbo" in selected_engine or "Hybrid" in selected_engine:
            base_price *= 1.08
        if "V6" in selected_engine or "Electric" in selected_engine:
            base_price *= 1.15

        years_old = 2026 - year
        age_dep = min(years_old * 0.03, 0.45)
        km_dep = min((km_driven / 15000) * 0.012, 0.20)
        trans_dep = 0.05 if transmission == "Manual" else 0.0

        total_depreciation = 1.0 - (age_dep + km_dep + trans_dep)

        if car_condition == "Brand New (Zero)":
            estimated_price = base_price
        elif car_condition == "Nearly New":
            estimated_price = base_price * 0.96
        else:
            estimated_price = base_price * max(total_depreciation, 0.35)

        # Extras multiplier
        extras_multiplier = 1.0
        if has_sunroof:
            extras_multiplier += 0.025
        if has_leather:
            extras_multiplier += 0.015
        if has_start_engine:
            extras_multiplier += 0.015
        if has_sensors_cam:
            extras_multiplier += 0.015
        if has_alloy_wheels:
            extras_multiplier += 0.010
        if has_screens:
            extras_multiplier += 0.010

        estimated_price *= extras_multiplier

        min_price = estimated_price * 0.95
        max_price = estimated_price * 1.05

        st.success(
            f"🎯 **Estimated Price for ({brand} - {model_name}):**\n"
            f"### `{estimated_price:,.2f}` EGP\n\n"
            f"📊 **Expected Market Range:** `{min_price:,.2f}` EGP to `{max_price:,.2f}` EGP"
        )

        search_record = {
            "Brand": brand,
            "Model": model_name,
            "Engine": selected_engine,
            "Year": year,
            "Estimated Price": f"{estimated_price:,.2f} EGP",
            "Condition": car_condition,
        }
        if search_record not in st.session_state.history:
            st.session_state.history.append(search_record)

        chart_data = pd.DataFrame(
            {
                "Category": ["Minimum Price", "Estimated Price", "Maximum Price"],
                "Price (EGP)": [min_price, estimated_price, max_price],
            }
        )
        st.subheader("📊 Price Range Analysis")
        st.bar_chart(chart_data.set_index("Category"))

        st.markdown("---")
        st.subheader("💳 Suggested Installment Calculator")
        cp1, cp2 = st.columns(2)
        with cp1:
            down_payment_pct = st.slider("Down Payment (%)", 20, 70, 30)
            down_payment = estimated_price * (down_payment_pct / 100)
            loan_amt = estimated_price - down_payment
            st.write(f"Down Payment Amount: **{down_payment:,.2f} EGP**")
            st.write(f"Loan Amount: **{loan_amt:,.2f} EGP**")
        with cp2:
            duration = st.selectbox("Loan Duration (Years)", [1, 2, 3, 4, 5, 7])
            interest_rate = 0.16
            total_with_interest = loan_amt * (1 + (interest_rate * duration))
            monthly = total_with_interest / (duration * 12)
            st.write(f"Approx. Monthly Installment: **{monthly:,.2f} EGP / month**")

        st.markdown("---")
        csv_bytes = pd.DataFrame([search_record]).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Car Report (CSV)",
            data=csv_bytes,
            file_name="car_price_report.csv",
            mime="text/csv",
        )


# ================= 2. Car Comparison Section =================
elif app_mode == "Car Comparison":
    st.title("⚖️ Side-by-Side Car Comparison")
    st.markdown("Compare specifications and base prices of two different cars.")

    mc1, mc2 = st.columns(2)

    with mc1:
        st.subheader("First Car")
        b1 = st.selectbox("Brand 1", sorted(list(CAR_MODELS.keys())), key="b1")
        m1 = st.selectbox("Model 1", list(CAR_MODELS[b1].keys()), key="m1")
        info1 = CAR_MODELS[b1][m1]
        st.write(f"- Base Price: **{info1['base_price']:,.2f} EGP**")
        st.write(f"- Body Type: **{info1['body']}**")
        st.write(f"- Horsepower: **{info1['hp']} HP**")
        st.write(f"- Available Engines: {', '.join(info1['engines'])}")

    with mc2:
        st.subheader("Second Car")
        b2 = st.selectbox("Brand 2", sorted(list(CAR_MODELS.keys())), key="b2")
        m2 = st.selectbox("Model 2", list(CAR_MODELS[b2].keys()), key="m2")
        info2 = CAR_MODELS[b2][m2]
        st.write(f"- Base Price: **{info2['base_price']:,.2f} EGP**")
        st.write(f"- Body Type: **{info2['body']}**")
        st.write(f"- Horsepower: **{info2['hp']} HP**")
        st.write(f"- Available Engines: {', '.join(info2['engines'])}")


# ================= 3. Budget Finder Section =================
elif app_mode == "Budget Finder":
    st.title("💰 Budget Finder")
    st.markdown("Set your maximum budget to find matching cars.")

    user_budget = st.slider(
        "Maximum Budget (EGP):", 600000, 7000000, 1500000, step=50000
    )

    matched = []
    for br, mods in CAR_MODELS.items():
        for md, dt in mods.items():
            if dt["base_price"] <= user_budget:
                matched.append(
                    {
                        "Brand": br,
                        "Model": md,
                        "Base Price": f"{dt['base_price']:,.2f} EGP",
                        "Body Type": dt["body"],
                        "Horsepower": f"{dt['hp']} HP",
                    }
                )

    if matched:
        st.success(f"Found {len(matched)} cars matching your budget:")