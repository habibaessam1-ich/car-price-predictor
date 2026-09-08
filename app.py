import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Car Price Predictor Pro", page_icon="🚗", layout="wide"
)

# ---------------------------------------------------------
# Comprehensive Car Database (All Brands Restored)
# ---------------------------------------------------------
CAR_MODELS = {
    # 1. Japanese & Asian
    "Nissan": {
        "Sunny": {
            "price": 800000,
            "engine": "1.5L",
            "body": "Sedan",
            "hp": 108,
        },
        "Sentra": {
            "price": 1100000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 118,
        },
        "Qashqai": {
            "price": 1650000,
            "engine": "1.3L Turbo",
            "body": "SUV",
            "hp": 148,
        },
        "Juke": {
            "price": 1300000,
            "engine": "1.0L Turbo",
            "body": "SUV",
            "hp": 114,
        },
    },
    "Toyota": {
        "Corolla": {
            "price": 1600000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 120,
        },
        "Yaris": {
            "price": 1000000,
            "engine": "1.5L",
            "body": "Hatchback",
            "hp": 118,
        },
        "Fortuner": {
            "price": 3800000,
            "engine": "4.0L",
            "body": "SUV",
            "hp": 234,
        },
        "C-HR": {
            "price": 1750000,
            "engine": "1.2L Turbo",
            "body": "SUV",
            "hp": 113,
        },
        "Belta": {
            "price": 850000,
            "engine": "1.5L",
            "body": "Sedan",
            "hp": 103,
        },
    },
    "Hyundai": {
        "Elantra": {
            "price": 1300000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 127,
        },
        "Tucson": {
            "price": 1900000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 180,
        },
        "Accent": {
            "price": 900000,
            "engine": "1.4L",
            "body": "Sedan",
            "hp": 100,
        },
        "Creta": {
            "price": 1400000,
            "engine": "1.5L",
            "body": "SUV",
            "hp": 113,
        },
        "I10": {"price": 700000, "engine": "1.2L", "body": "Hatchback", "hp": 84},
    },
    "Kia": {
        "Cerato / K3": {
            "price": 1350000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 130,
        },
        "Sportage": {
            "price": 1950000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 177,
        },
        "Pegas": {"price": 850000, "engine": "1.4L", "body": "Sedan", "hp": 95},
        "Seltos": {
            "price": 1500000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 140,
        },
        "XCeed": {
            "price": 1600000,
            "engine": "1.5L Turbo",
            "body": "Crossover",
            "hp": 160,
        },
    },
    "Mitsubishi": {
        "Lancer": {
            "price": 750000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 115,
        },
        "Xpander": {
            "price": 1300000,
            "engine": "1.5L",
            "body": "Van",
            "hp": 103,
        },
        "Eclipse Cross": {
            "price": 1600000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Attrage": {
            "price": 750000,
            "engine": "1.2L",
            "body": "Sedan",
            "hp": 78,
        },
    },
    "Suzuki": {
        "Swift": {
            "price": 750000,
            "engine": "1.2L",
            "body": "Hatchback",
            "hp": 84,
        },
        "Ciaz": {"price": 850000, "engine": "1.5L", "body": "Sedan", "hp": 104},
        "Ertiga": {"price": 950000, "engine": "1.5L", "body": "Van", "hp": 103},
        "Espresso": {
            "price": 550000,
            "engine": "1.0L",
            "body": "Hatchback",
            "hp": 67,
        },
    },
    "Honda": {
        "Civic": {
            "price": 1700000,
            "engine": "1.5L Turbo",
            "body": "Sedan",
            "hp": 180,
        },
        "City": {"price": 1200000, "engine": "1.5L", "body": "Sedan", "hp": 121},
        "CR-V": {
            "price": 2200000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 190,
        },
    },
    # 2. European
    "Renault": {
        "Logan": {"price": 650000, "engine": "1.6L", "body": "Sedan", "hp": 110},
        "Megane": {
            "price": 1400000,
            "engine": "1.6L / 1.3T",
            "body": "Sedan",
            "hp": 115,
        },
        "Duster": {
            "price": 1200000,
            "engine": "1.6L",
            "body": "SUV",
            "hp": 115,
        },
        "Stepway": {
            "price": 850000,
            "engine": "1.6L",
            "body": "Hatchback",
            "hp": 110,
        },
    },
    "Peugeot": {
        "301": {"price": 850000, "engine": "1.6L", "body": "Sedan", "hp": 115},
        "508": {
            "price": 1800000,
            "engine": "1.6L Turbo",
            "body": "Sedan",
            "hp": 165,
        },
        "2008": {
            "price": 1450000,
            "engine": "1.2L Turbo",
            "body": "SUV",
            "hp": 130,
        },
        "3008": {
            "price": 1950000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 180,
        },
        "5008": {
            "price": 2200000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 180,
        },
    },
    "Fiat": {
        "Tipo": {"price": 1050000, "engine": "1.6L", "body": "Sedan", "hp": 110},
        "500": {
            "price": 1100000,
            "engine": "1.4L",
            "body": "Hatchback",
            "hp": 100,
        },
        "Punto": {
            "price": 500000,
            "engine": "1.4L",
            "body": "Hatchback",
            "hp": 77,
        },
    },
    "Skoda": {
        "Octavia": {
            "price": 1850000,
            "engine": "1.4L Turbo",
            "body": "Sedan",
            "hp": 150,
        },
        "Kodiaq": {
            "price": 2600000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Karoq": {
            "price": 2100000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Scala": {
            "price": 1300000,
            "engine": "1.6L",
            "body": "Hatchback",
            "hp": 110,
        },
    },
    "Volkswagen": {
        "Golf": {
            "price": 1700000,
            "engine": "1.4L Turbo",
            "body": "Hatchback",
            "hp": 150,
        },
        "Passat": {
            "price": 1900000,
            "engine": "1.4L Turbo",
            "body": "Sedan",
            "hp": 150,
        },
        "Tiguan": {
            "price": 2500000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Jetta": {"price": 900000, "engine": "1.4L", "body": "Sedan", "hp": 125},
    },
    "Opel": {
        "Astra": {
            "price": 950000,
            "engine": "1.4L Turbo",
            "body": "Sedan",
            "hp": 140,
        },
        "Corsa": {
            "price": 1250000,
            "engine": "1.2L Turbo",
            "body": "Hatchback",
            "hp": 130,
        },
        "Grandland": {
            "price": 1750000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 163,
        },
        "Mokka": {
            "price": 1500000,
            "engine": "1.2L Turbo",
            "body": "SUV",
            "hp": 130,
        },
    },
    "Seat": {
        "Ibiza": {
            "price": 1250000,
            "engine": "1.0L Turbo",
            "body": "Hatchback",
            "hp": 115,
        },
        "Leon": {
            "price": 1600000,
            "engine": "1.4L Turbo",
            "body": "Hatchback",
            "hp": 150,
        },
        "Ateca": {
            "price": 1850000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Arona": {
            "price": 1350000,
            "engine": "1.0L Turbo",
            "body": "SUV",
            "hp": 115,
        },
    },
    # 3. Chinese
    "MG": {
        "MG 5": {"price": 850000, "engine": "1.5L", "body": "Sedan", "hp": 118},
        "MG 6": {
            "price": 1200000,
            "engine": "1.5L Turbo",
            "body": "Sedan",
            "hp": 169,
        },
        "MG ZS": {
            "price": 1050000,
            "engine": "1.5L",
            "body": "SUV",
            "hp": 119,
        },
        "MG RX5": {
            "price": 1400000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 171,
        },
        "MG4": {
            "price": 1350000,
            "engine": "Electric",
            "body": "Hatchback",
            "hp": 170,
        },
    },
    "Chery": {
        "Arrizo 5": {
            "price": 750000,
            "engine": "1.5L",
            "body": "Sedan",
            "hp": 114,
        },
        "Tiggo 3": {
            "price": 880000,
            "engine": "1.6L",
            "body": "SUV",
            "hp": 126,
        },
        "Tiggo 7": {
            "price": 1100000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 145,
        },
        "Tiggo 8": {
            "price": 1450000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 145,
        },
    },
    "Geely": {
        "Emgrand": {"price": 850000, "engine": "1.5L", "body": "Sedan", "hp": 102},
        "Coolray": {
            "price": 1300000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 175,
        },
        "Okavango": {
            "price": 1650000,
            "engine": "1.5L Hybrid",
            "body": "SUV",
            "hp": 190,
        },
    },
    "Changan": {
        "Alsvin": {"price": 650000, "engine": "1.5L", "body": "Sedan", "hp": 107},
        "CS35 Plus": {
            "price": 1150000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 158,
        },
        "CS55 Plus": {
            "price": 1350000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 185,
        },
    },
    "BYD": {
        "F3": {"price": 620000, "engine": "1.5L", "body": "Sedan", "hp": 108},
        "Song Plus": {
            "price": 1600000,
            "engine": "Hybrid",
            "body": "SUV",
            "hp": 197,
        },
    },
    "HAVAL": {
        "H6": {
            "price": 1450000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Jolion": {
            "price": 1200000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 147,
        },
    },
    # 4. American & Luxury
    "Chevrolet": {
        "Optra": {"price": 750000, "engine": "1.5L", "body": "Sedan", "hp": 110},
        "Aveo": {"price": 600000, "engine": "1.5L", "body": "Sedan", "hp": 105},
        "Captiva": {
            "price": 1500000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 148,
        },
        "Cruze": {"price": 650000, "engine": "1.6L", "body": "Sedan", "hp": 113},
    },
    "Ford": {
        "Focus": {
            "price": 1200000,
            "engine": "1.5L",
            "body": "Hatchback",
            "hp": 120,
        },
        "EcoSport": {
            "price": 1000000,
            "engine": "1.0L Turbo",
            "body": "SUV",
            "hp": 123,
        },
        "Kuga": {
            "price": 1400000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 150,
        },
    },
    "BMW": {
        "3 Series (320i)": {
            "price": 3500000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 184,
        },
        "5 Series (520i)": {
            "price": 4800000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 184,
        },
        "X1": {
            "price": 2900000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 140,
        },
        "X5": {
            "price": 6200000,
            "engine": "3.0L Turbo",
            "body": "SUV",
            "hp": 340,
        },
    },
    "Mercedes": {
        "C-Class (C180/C200)": {
            "price": 4200000,
            "engine": "1.5L Turbo",
            "body": "Sedan",
            "hp": 170,
        },
        "E-Class (E200)": {
            "price": 5800000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 197,
        },
        "A-Class": {
            "price": 2700000,
            "engine": "1.3L Turbo",
            "body": "Hatchback",
            "hp": 136,
        },
        "GLC": {
            "price": 5900000,
            "engine": "2.0L Turbo",
            "body": "SUV",
            "hp": 204,
        },
    },
    "Audi": {
        "A4": {
            "price": 2800000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 190,
        },
        "A6": {
            "price": 3900000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 245,
        },
        "Q3": {
            "price": 2500000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 150,
        },
        "Q7": {
            "price": 4900000,
            "engine": "3.0L Turbo",
            "body": "SUV",
            "hp": 340,
        },
    },
}

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
    "Renault": (
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80"
    ),
}

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Section 1: Price Predictor
# ---------------------------------------------------------
if app_mode == "Price Predictor":
    st.title("🚗 Advanced Used Car Price Prediction System")
    st.markdown("---")

    col_input, col_img = st.columns([1.2, 1])

    with col_input:
        brand = st.selectbox("Car Brand", sorted(list(CAR_MODELS.keys())))
        available_models = list(CAR_MODELS[brand].keys())
        model_name = st.selectbox("Car Model", available_models)

        car_info = CAR_MODELS[brand][model_name]
        st.info(
            f"ℹ️ **Default Specs:** Engine: `{car_info['engine']}` | Body: `{car_info['body']}` | Power: `{car_info['hp']} HP`"
        )

        transmission = st.selectbox("Transmission", ["Automatic", "Manual"])
        car_color = st.selectbox(
            "Car Color", ["White", "Black", "Silver", "Gray", "Red", "Blue", "Other"]
        )

    with col_img:
        img_url = CAR_IMAGES.get(
            brand,
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80",
        )
        st.image(
            img_url, caption=f"{brand} - {model_name} Preview", use_container_width=True
        )

    car_condition = st.radio(
        "Car Condition",
        ["Zero (Brand New)", "Nearly New", "Used"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input(
            "Manufacturing Year", min_value=2000, max_value=2026, value=2020
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
                "Kilometers Driven (KM)", min_value=0, max_value=500000, value=60000
            )

    st.markdown("---")

    if st.button("🚀 Predict Estimated Price"):
        base_price = car_info["price"]

        years_old = 2026 - year
        age_depreciation = min(years_old * 0.035, 0.50)
        km_depreciation = min((km_driven / 20000) * 0.01, 0.15)
        trans_depreciation = 0.05 if transmission == "Manual" else 0.0

        total_depreciation = (
            age_depreciation + km_depreciation + trans_depreciation
        )

        if car_condition == "Zero (Brand New)":
            estimated_price = base_price
        elif car_condition == "Nearly New":
            estimated_price = base_price * 0.92
        else:
            estimated_price = base_price * (1.0 - total_depreciation)
            estimated_price = max(estimated_price, base_price * 0.40)

        min_price = estimated_price * 0.95
        max_price = estimated_price * 1.05

        st.success(
            f"🎯 **Estimated Price for ({brand} {model_name} - {year}):** {estimated_price:,.2f} EGP\n\n"
            f"📊 **Expected Range (±5% Error Margin):** {min_price:,.2f} EGP — {max_price:,.2f} EGP"
        )

        search_record = {
            "Brand": brand,
            "Model": model_name,
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
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            down_payment_pct = st.slider("Down Payment (%)", 20, 70, 30)
            down_payment = estimated_price * (down_payment_pct / 100)
            loan_amount = estimated_price - down_payment
            st.write(f"Down Payment Amount: **{down_payment:,.2f} EGP**")
            st.write(f"Loan Amount: **{loan_amount:,.2f} EGP**")
        with col_p2:
    