import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="Car Price Predictor", page_icon="🚗", layout="wide"
)

# 1. قاعدة بيانات ضخمة وشاملة لكل ماركات وموديلات السيارات
CAR_MODELS = {
    # السيارات الكورية
    "Hyundai": {
        "Elantra": 1300000,
        "Tucson": 1900000,
        "Accent": 900000,
        "Creta": 1400000,
        "I10": 700000,
        "Sonata": 1700000,
        "Santa Fe": 2400000,
        "Bayon": 1150000,
        "Grand i10": 750000,
    },
    "Kia": {
        "Cerato / K3": 1350000,
        "Sportage": 1950000,
        "Pegas": 850000,
        "Seltos": 1500000,
        "XCeed": 1600000,
        "Sorento": 2500000,
        "Soul": 1100000,
        "Grand Cerato": 1400000,
        "Carnival": 3200000,
    },
    # السيارات اليابانية
    "Toyota": {
        "Corolla": 1600000,
        "Yaris": 1000000,
        "Fortuner": 3800000,
        "C-HR": 1750000,
        "Belta": 850000,
        "Camry": 2800000,
        "RAV4": 2900000,
        "Land Cruiser": 6500000,
        "Hilux": 2200000,
        "Rush": 1150000,
    },
    "Nissan": {
        "Sunny": 800000,
        "Sentra": 1100000,
        "Qashqai": 1650000,
        "Juke": 1300000,
        "Patrol": 5500000,
        "X-Trail": 2100000,
        "Altima": 1900000,
        "Maxima": 2300000,
    },
    "Honda": {
        "Civic": 1700000,
        "City": 1200000,
        "CR-V": 2200000,
        "Accord": 2400000,
        "HR-V": 1750000,
        "Pilot": 3100000,
    },
    "Mitsubishi": {
        "Lancer": 750000,
        "Xpander": 1300000,
        "Eclipse Cross": 1600000,
        "Attrage": 750000,
        "Pajero": 3500000,
        "Outlander": 2100000,
        "Mirage": 700000,
    },
    "Suzuki": {
        "Swift": 750000,
        "Ciaz": 850000,
        "Ertiga": 950000,
        "Espresso": 550000,
        "Vitara": 1250000,
        "Grand Vitara": 1600000,
        "Jimny": 1400000,
        "Baleno": 850000,
    },
    # السيارات الأوروبية والألمانية
    "BMW": {
        "3 Series (320i)": 3500000,
        "5 Series (520i)": 4800000,
        "X1": 2900000,
        "X5": 6200000,
        "1 Series": 2200000,
        "4 Series": 4500000,
        "7 Series": 8500000,
        "X3": 4100000,
        "X6": 6800000,
    },
    "Mercedes": {
        "C-Class (C180/C200)": 4200000,
        "E-Class (E200)": 5800000,
        "A-Class": 2700000,
        "GLC": 5900000,
        "S-Class": 9500000,
        "CLA": 3600000,
        "GLA": 3400000,
        "GLE": 6500000,
        "G-Class": 12000000,
    },
    "Audi": {
        "A4": 2800000,
        "A6": 3900000,
        "Q3": 2500000,
        "Q7": 4900000,
        "A3": 2200000,
        "A8": 7500000,
        "Q5": 3700000,
        "Q8": 5800000,
    },
    "Volkswagen": {
        "Golf": 1700000,
        "Passat": 1900000,
        "Tiguan": 2500000,
        "Jetta": 900000,
        "Polo": 950000,
        "Touareg": 3800000,
        "Teramont": 3200000,
    },
    "Skoda": {
        "Octavia": 1850000,
        "Kodiaq": 2600000,
        "Karoq": 2100000,
        "Scala": 1300000,
        "Superb": 2400000,
        "Kamiq": 1450000,
        "Fabia": 950000,
    },
    "Porsche": {
        "Cayenne": 6500000,
        "Macan": 5200000,
        "Panamera": 8000000,
        "911": 9800000,
        "Taycan": 7200000,
    },
    # السيارات الفرنسية والإيطالية
    "Renault": {
        "Logan": 650000,
        "Megane": 1400000,
        "Duster": 1200000,
        "Stepway": 850000,
        "Sandero": 750000,
        "Kadjar": 1500000,
        "Captur": 1250000,
    },
    "Peugeot": {
        "301": 850000,
        "508": 1800000,
        "2008": 1450000,
        "3008": 1950000,
        "5008": 2200000,
        "208": 1100000,
        "408": 2100000,
    },
    "Citroen": {
        "C3": 950000,
        "C4": 1350000,
        "C5 Aircross": 1850000,
        "Elysee": 800000,
    },
    "Fiat": {
        "Tipo": 1050000,
        "500": 1100000,
        "Punto": 500000,
        "Doblo": 900000,
    },
    "Alfa Romeo": {"Giulia": 3100000, "Stelvio": 3600000, "Tonale": 2600000},
    # السيارات الأمريكية
    "Chevrolet": {
        "Aveo": 600000,
        "Optra": 750000,
        "Cruze": 650000,
        "Captiva": 1500000,
        "Malibu": 1400000,
        "Tahoe": 5500000,
        "Suburban": 5800000,
        "Camaro": 4200000,
        "Corvette": 8500000,
        "Silverado": 3400000,
    },
    "Ford": {
        "Focus": 1200000,
        "EcoSport": 1000000,
        "Kuga": 1400000,
        "Fusion": 1600000,
        "Explorer": 3900000,
        "Mustang": 4500000,
        "Edge": 2400000,
        "Ranger": 2100000,
    },
    "Jeep": {
        "Grand Cherokee": 4200000,
        "Wrangler": 4800000,
        "Renegade": 1600000,
        "Compass": 2100000,
        "Gladiator": 4500000,
    },
    "Dodge": {"Charger": 4100000, "Challenger": 4300000, "Durango": 3900000},
    "GMC": {"Terrain": 2600000, "Acadia": 3400000, "Yukon": 5900000},
    "Tesla": {
        "Model 3": 2800000,
        "Model Y": 3200000,
        "Model S": 4800000,
        "Model X": 5200000,
    },
    # السيارات الصينية الرائجة
    "MG": {
        "MG 5": 850000,
        "MG 6": 1200000,
        "MG ZS": 1050000,
        "MG RX5": 1400000,
        "MG4": 1350000,
        "MG HS": 1600000,
        "MG One": 1450000,
    },
    "Chery": {
        "Arrizo 5": 750000,
        "Tiggo 3": 880000,
        "Tiggo 7": 1100000,
        "Tiggo 8": 1450000,
        "Arrizo 6 Pro": 1150000,
        "Tiggo 4 Pro": 980000,
    },
    "Geely": {
        "Emgrand": 850000,
        "Coolray": 1300000,
        "Okavango": 1650000,
        "Monjaro": 2100000,
        "Starray": 1750000,
    },
    "Changan": {
        "Alsvin": 650000,
        "CS35 Plus": 1150000,
        "CS55 Plus": 1350000,
        "CS75 Plus": 1600000,
        "Eado Plus": 1050000,
        "Uni-T": 1500000,
        "Uni-K": 1900000,
        "Uni-V": 1550000,
    },
    "BYD": {
        "F3": 620000,
        "Song Plus": 1600000,
        "Qin Plus": 1100000,
        "Atto 3": 1700000,
        "Han": 2400000,
        "Seagull": 750000,
    },
    "HAVAL": {
        "H6": 1450000,
        "Jolion": 1200000,
        "Darog": 1700000,
        "H6 GT": 1650000,
    },
    "Jetour": {
        "X70": 1250000,
        "X70 Plus": 1450000,
        "X90 Plus": 1750000,
        "Dashing": 1500000,
    },
    "Exeed": {"TXL": 1950000, "LX": 1700000, "VX": 2400000},
    "Omoda": {"C5": 1350000, "S5": 1150000},
    "Jaecoo": {"J7": 1650000},
    "Baic": {"X3": 850000, "X7": 1450000, "U5 Plus": 800000},
    "GAC": {"Empow": 1250000, "GS3": 1150000, "GS8": 2100000, "Emkoo": 1450000},
    "Proton": {"Saga": 750000, "X50": 1300000, "X70": 1550000},
}

CAR_IMAGES = {
    "BMW": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=800&q=80",
    "Mercedes": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?auto=format&fit=crop&w=800&q=80",
    "Toyota": "https://images.unsplash.com/photo-1629897048514-3dd7414fe72a?auto=format&fit=crop&w=800&q=80",
    "Hyundai": "https://images.unsplash.com/photo-1619767886558-efdc259cde1a?auto=format&fit=crop&w=800&q=80",
    "Kia": "https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?auto=format&fit=crop&w=800&q=80",
    "Nissan": "https://images.unsplash.com/photo-1609521263047-f8d205293f24?auto=format&fit=crop&w=800&q=80",
    "Chevrolet": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80",
    "Audi": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80",
    "Porsche": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=800&q=80",
    "Tesla": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=800&q=80",
}


def calculate_car_price(
    brand, model_name, year, km_driven, car_condition, transmission
):
    base_price = CAR_MODELS[brand][model_name]
    years_old = 2026 - year

    age_dep = min(years_old * 0.035, 0.50)
    km_dep = min((km_driven / 20000) * 0.01, 0.15)
    trans_dep = 0.05 if transmission == "Manual" else 0.0

    total_dep = age_dep + km_dep + trans_dep

    if car_condition == "Zero (Brand New)":
        est_price = base_price
        age_dep, km_dep, trans_dep = 0.0, 0.0, 0.0
    elif (
        car_condition == "Nearly New (كسر زيرو)"
        and years_old <= 3
        and km_driven <= 30000
    ):
        est_price = base_price * 0.92
    else:
        est_price = base_price * (1.0 - total_dep)
        est_price = max(est_price, base_price * 0.45)

    min_p = est_price * 0.95
    max_p = est_price * 1.05

    return est_price, min_p, max_p, base_price, age_dep, km_dep, trans_dep


st.title("🚗 Smart Car Price Valuation System")
st.caption("👩‍💻 **Developed by:** Habiba Essam & Salma Ahmed")
st.markdown("---")

tab1, tab2 = st.tabs(["🔮 Predict Single Car Price", "⚖️ Compare Two Cars"])

with tab1:
    col_input, col_img = st.columns([1.2, 1])

    with col_input:
        brand = st.selectbox("Car Brand", sorted(list(CAR_MODELS.keys())))
        available_models = list(CAR_MODELS[brand].keys())
        model_name = st.selectbox("Car Model / Line", available_models)
        transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

    with col_img:
        img_url = CAR_IMAGES.get(
            brand,
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80",
        )
        st.image(img_url, caption=f"{brand} Preview", use_container_width=True)

    car_condition = st.radio(
        "Car Condition",
        ["Zero (Brand New)", "Nearly New (كسر زيرو)", "Used (مستعمل)"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input(
            "Manufacturing Year", min_value=2000, max_value=2026, value=2016
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
                "Kilometers Driven (KM)",
                min_value=0,
                max_value=500000,
                value=80000,
            )

    if st.button("Predict Price & Analyze All", key="btn_single"):
        est_p, min_p, max_p, base_p, age_dep, km_dep, trans_dep = (
            calculate_car_price(
                brand, model_name, year, km_driven, car_condition, transmission
            )
        )

        st.success(
            f"🎯 **Estimated Price ({brand} {model_name} {year}):** {est_p:,.2f} EGP  |  "
            f"📊 **Range:** {min_p:,.2f} — {max_p:,.2f} EGP"
        )

        st.markdown("---")
        c_a, c_b, c_c = st.columns(3)

        with c_a:
            st.markdown("##### 🔍 Price Breakdown")
            st.write(f"• **Base Price:** {base_p:,.2f}")
            st.write(f"• **Age Disc:** -{age_dep * 100:.1f}%")
            st.write(f"• **KM Disc:** -{km_dep * 100:.1f}%")
            if transmission == "Manual":
                st.write("• **Manual Disc:** -5.0%")

        with c_b:
            st.markdown("##### ⛽ Operational Specs")
            fuel_rate = "7.5 L / 100km" if fuel_type == "Petrol" else "5.0 L / 100km"
            if fuel_type == "Electric":
                fuel_rate = "15 kWh / 100km"
            st.write(f"• **Fuel Type:** {fuel_type}")
            st.write(f"• **Est. Consumption:** {fuel_rate}")
            st.write(f"• **Market Status:** High Demand 🔥")

        with c_c:
            st.markdown("##### 💳 Loan Calculator")
            down_payment = est_p * 0.30
            monthly_installment = (est_p * 0.70 * 1.15) / 36
            st.write(f"• **Down Payment (30%):** {down_payment:,.0f}")
            st.write(
                f"• **Est. Monthly (3 Years):** {monthly_installment:,.0f} EGP/mo"
            )

        st.markdown("---")

        report_df = pd.DataFrame(
            [
                {
                    "Brand": brand,
                    "Model": model_name,
                    "Year": year,
                    "Condition": car_condition,
                    "KM": km_driven,
                    "Fuel": fuel_type,
                    "Estimated Price (EGP)": est_p,
                    "Min Price": min_p,
                    "Max Price": max_p,
                }
            ]
        )
        csv = report_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Full Valuation & Analysis Report (CSV)",
            data=csv,
            file_name=f"{brand}_{model_name}_complete_report.csv",
            mime="text/csv",
        )

with tab2:
    st.subheader("⚖️ Side-by-Side Car Valuation Comparison")
    col_car1, col_car2 = st.columns(2)

    with col_car1:
        st.markdown("### 🚗 Car 1")
        b1 = st.selectbox("Brand 1", sorted(list(CAR_MODELS.keys())), key="b1")
        m1 = st.selectbox("Model 1", list(CAR_MODELS[b1].keys()), key="m1")
        y1 = st.number_input("Year 1", 2000, 2026, 2020, key="y1")
        km1 = st.number_input("KM 1", 0, 500000, 60000, key="km1")
        cond1 = st.radio(
            "Condition 1",
            ["Used (مستعمل)", "Zero (Brand New)", "Nearly New (كسر زيرو)"],
            key="cond1",
        )
        trans1 = st.selectbox(
            "Transmission 1", ["Automatic", "Manual"], key="t1"
        )

    with col_car2:
        st.markdown("### 🚗 Car 2")
        b2 = st.selectbox("Brand 2", sorted(list(CAR_MODELS.keys())), key="b2")
        m2 = st.selectbox("Model 2", list(CAR_MODELS[b2].keys()), key="m2")
        y2 = st.number_input("Year 2", 2000, 2026, 2018, key="y2")
        km2 = st.number_input("KM 2", 0, 500000, 100000, key="km2")
        cond2 = st.radio(
            "Condition 2",
            ["Used (مستعمل)", "Zero (Brand New)", "Nearly New (كسر زيرو)"],
            key="cond2",
        )
        trans2 = st.selectbox(
            "Transmission 2", ["Automatic", "Manual"], key="t2"
        )

    if st.button("Compare Prices", key="btn_compare"):
        p1, _, _, _, _, _, _ = calculate_car_price(
            b1, m1, y1, km1, cond1, trans1
        )
        p2, _, _, _, _, _, _ = calculate_car_price(
            b2, m2, y2, km2, cond2, trans2
        )

        st.markdown("---")
        res1, res2 = st.columns(2)
        res1.metric(f"{b1} {m1} ({y1})", f"{p1:,.0f} EGP")
        res2.metric(f"{b2} {m2} ({y2})", f"{p2:,.0f} EGP")

        diff = abs(p1 - p2)
        cheaper = f"{b1} {m1}" if p1 < p2 else f"{b2} {m2}"
        st.info(
            f"💡 **Comparison Summary:** {cheaper} is cheaper by approximately **{diff:,.0f} EGP**."
        )