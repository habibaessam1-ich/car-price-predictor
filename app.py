import pandas as pd
import streamlit as st

# إعدادات الصفحة المتقدمة
st.set_page_config(
    page_title="Advanced Car Valuation & Market Intelligence",
    page_icon="🚀",
    layout="wide",
)

# 1. قاعدة بيانات شاملة وموسعة لكل الماركات والموديلات العالمية والمحلية
CAR_MODELS = {
    "Hyundai": {
        "Elantra": 1300000,
        "Tucson": 1900000,
        "Accent": 900000,
        "Creta": 1400000,
        "I10": 700000,
        "Sonata": 1700000,
        "Santa Fe": 2400000,
        "Bayon": 1150000,
    },
    "Kia": {
        "Cerato / K3": 1350000,
        "Sportage": 1950000,
        "Pegas": 850000,
        "Seltos": 1500000,
        "XCeed": 1600000,
        "Sorento": 2500000,
        "Soul": 1100000,
    },
    "Toyota": {
        "Corolla": 1600000,
        "Yaris": 1000000,
        "Fortuner": 3800000,
        "C-HR": 1750000,
        "Belta": 850000,
        "Camry": 2800000,
        "RAV4": 2900000,
        "Land Cruiser": 6500000,
    },
    "Nissan": {
        "Sunny": 800000,
        "Sentra": 1100000,
        "Qashqai": 1650000,
        "Juke": 1300000,
        "Patrol": 5500000,
        "X-Trail": 2100000,
    },
    "Honda": {
        "Civic": 1700000,
        "City": 1200000,
        "CR-V": 2200000,
        "Accord": 2400000,
        "HR-V": 1750000,
    },
    "Mitsubishi": {
        "Lancer": 750000,
        "Xpander": 1300000,
        "Eclipse Cross": 1600000,
        "Attrage": 750000,
        "Pajero": 3500000,
    },
    "Suzuki": {
        "Swift": 750000,
        "Ciaz": 850000,
        "Ertiga": 950000,
        "Espresso": 550000,
        "Vitara": 1250000,
        "Jimny": 1400000,
    },
    "BMW": {
        "3 Series (320i)": 3500000,
        "5 Series (520i)": 4800000,
        "X1": 2900000,
        "X5": 6200000,
        "4 Series": 4500000,
        "7 Series": 8500000,
    },
    "Mercedes": {
        "C-Class (C180/C200)": 4200000,
        "E-Class (E200)": 5800000,
        "A-Class": 2700000,
        "GLC": 5900000,
        "S-Class": 9500000,
        "G-Class": 12000000,
    },
    "Audi": {
        "A4": 2800000,
        "A6": 3900000,
        "Q3": 2500000,
        "Q7": 4900000,
        "Q5": 3700000,
        "Q8": 5800000,
    },
    "Volkswagen": {
        "Golf": 1700000,
        "Passat": 1900000,
        "Tiguan": 2500000,
        "Jetta": 900000,
        "Touareg": 3800000,
    },
    "Skoda": {
        "Octavia": 1850000,
        "Kodiaq": 2600000,
        "Karoq": 2100000,
        "Scala": 1300000,
        "Superb": 2400000,
    },
    "Porsche": {
        "Cayenne": 6500000,
        "Macan": 5200000,
        "Panamera": 8000000,
        "911": 9800000,
    },
    "Renault": {
        "Logan": 650000,
        "Megane": 1400000,
        "Duster": 1200000,
        "Stepway": 850000,
        "Kadjar": 1500000,
    },
    "Peugeot": {
        "301": 850000,
        "508": 1800000,
        "2008": 1450000,
        "3008": 1950000,
        "5008": 2200000,
    },
    "Citroen": {"C3": 950000, "C4": 1350000, "C5 Aircross": 1850000},
    "Fiat": {"Tipo": 1050000, "500": 1100000, "Punto": 500000},
    "Chevrolet": {
        "Aveo": 600000,
        "Optra": 750000,
        "Cruze": 650000,
        "Captiva": 1500000,
        "Malibu": 1400000,
        "Tahoe": 5500000,
    },
    "Ford": {
        "Focus": 1200000,
        "EcoSport": 1000000,
        "Kuga": 1400000,
        "Explorer": 3900000,
        "Mustang": 4500000,
    },
    "Jeep": {
        "Grand Cherokee": 4200000,
        "Wrangler": 4800000,
        "Renegade": 1600000,
        "Compass": 2100000,
    },
    "Tesla": {
        "Model 3": 2800000,
        "Model Y": 3200000,
        "Model S": 4800000,
    },
    "MG": {
        "MG 5": 850000,
        "MG 6": 1200000,
        "MG ZS": 1050000,
        "MG RX5": 1400000,
        "MG4": 1350000,
        "MG HS": 1600000,
    },
    "Chery": {
        "Arrizo 5": 750000,
        "Tiggo 3": 880000,
        "Tiggo 7": 1100000,
        "Tiggo 8": 1450000,
        "Tiggo 4 Pro": 980000,
    },
    "Geely": {
        "Emgrand": 850000,
        "Coolray": 1300000,
        "Okavango": 1650000,
        "Monjaro": 2100000,
    },
    "Changan": {
        "Alsvin": 650000,
        "CS35 Plus": 1150000,
        "CS55 Plus": 1350000,
        "Uni-T": 1500000,
        "Uni-V": 1550000,
    },
    "BYD": {"F3": 620000, "Song Plus": 1600000, "Atto 3": 1700000},
    "HAVAL": {"H6": 1450000, "Jolion": 1200000, "H6 GT": 1650000},
    "Jetour": {"X70": 1250000, "X70 Plus": 1450000, "Dashing": 1500000},
    "GAC": {"Empow": 1250000, "GS3": 1150000, "GS8": 2100000},
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


# 2. خوارزمية التسعير والتحليل المتقدم
def advanced_valuation(
    brand, model_name, year, km_driven, car_condition, transmission, fuel_type
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

    # حساب مؤشر صحة السيارة وتقييم الصفقة
    health_score = max(
        20, int(100 - (years_old * 3.5) - (km_driven / 10000 * 1.5))
    )
    deal_rating = (
        "🔥 Excellent Deal"
        if km_driven < 50000 and years_old < 4
        else "👍 Fair Market Value"
        if years_old < 8
        else "⚠️ High Mileage / Old"
    )

    return (
        est_price,
        min_p,
        max_p,
        base_price,
        age_dep,
        km_dep,
        trans_dep,
        health_score,
        deal_rating,
    )


# واجهة التطبيق الرئيسية
st.title("🚀 Advanced Car Intelligence & Valuation Suite")
st.caption("👩‍💻 **Developed by:** Habiba Essam & Salma Ahmed")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    [
        "🔮 Advanced AI Predictor",
        "⚖️ Dual Car Comparison Matrix",
        "📊 Market Trend Analytics",
    ]
)

# ==================== TAB 1 ====================
with tab1:
    col_input, col_img = st.columns([1.3, 1])

    with col_input:
        brand = st.selectbox("Select Brand", sorted(list(CAR_MODELS.keys())))
        model_name = st.selectbox(
            "Select Model", list(CAR_MODELS[brand].keys())
        )
        transmission = st.selectbox(
            "Transmission Type", ["Automatic", "Manual"]
        )
        fuel_type = st.selectbox(
            "Engine / Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"]
        )

    with col_img:
        img_url = CAR_IMAGES.get(
            brand,
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80",
        )
        st.image(img_url, caption=f"{brand} Dynamic View", use_container_width=True)

    car_condition = st.radio(
        "Vehicle Condition Status",
        ["Zero (Brand New)", "Nearly New (كسر زيرو)", "Used (مستعمل)"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input(
            "Manufacturing Year", min_value=2000, max_value=2026, value=2020
        )
    with col2:
        if car_condition == "Zero (Brand New)":
            km_driven = 0
            st.info("Odometer: 0 KM (Factory Fresh)")
        else:
            km_driven = st.number_input(
                "Odometer Reading (KM)",
                min_value=0,
                max_value=500000,
                value=45000,
            )

    if st.button(
        "Run Advanced Valuation & Diagnostics", key="btn_adv_predict"
    ):
        (
            est_p,
            min_p,
            max_p,
            base_p,
            age_dep,
            km_dep,
            trans_dep,
            health_score,
            deal_rating,
        ) = advanced_valuation(
            brand,
            model_name,
            year,
            km_driven,
            car_condition,
            transmission,
            fuel_type,
        )

        st.success(
            f"🎯 **Predicted Valuation:** {est_p:,.2f} EGP  |  "
            f"📈 **Confidence Interval:** {min_p:,.0f} — {max_p:,.0f} EGP"
        )

        # لوحة تحكم متقدمة من 4 أعمدة للتحليلات
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Vehicle Health Score", f"{health_score}% / 100%")
        m2.metric("Market Deal Rating", deal_rating)
        monthly_inst = (est_p * 0.70 * 1.15) / 36
        m3.metric("Est. Monthly Installment", f"{monthly_inst:,.0f} EGP")
        fuel_rate = (
            "7.2 L/100km"
            if fuel_type == "Petrol"
            else "14 kWh/100km"
            if fuel_type == "Electric"
            else "5.0 L/100km"
        )
        m4.metric("Fuel Efficiency Rate", fuel_rate)

        st.markdown("---")
        exp1, exp2 = st.columns(2)
        with exp1:
            st.markdown("##### 📉 Depreciation Breakdown Factors")
            st.write(f"• **Base MSRP Value:** {base_p:,.2f} EGP")
            st.write(
                f"• **Age Impact ({2026 - year} yrs):** -{age_dep * 100:.1f}%"
            )
            st.write(f"• **Mileage Impact ({km_driven:,} KM):** -{km_dep * 100:.1f}%")
            if transmission == "Manual":
                st.write("• **Transmission Penalty:** -5.0%")

        with exp2:
            st.markdown("##### 📥 Export Diagnostic Report")
            report_df = pd.DataFrame(
                [
                    {
                        "Brand": brand,
                        "Model": model_name,
                        "Year": year,
                        "Condition": car_condition,
                        "KM": km_driven,
                        "Fuel": fuel_type,
                        "Health Score": health_score,
                        "Estimated Price (EGP)": est_p,
                    }
                ]
            )
            csv = report_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Professional CSV Report",
                data=csv,
                file_name=f"{brand}_{model_name}_advanced_report.csv",
                mime="text/csv",
            )

# ==================== TAB 2 ====================
with tab2:
    st.subheader("⚖️ Comprehensive Multi-Variable Car Matrix Comparison")
    cc1, cc2 = st.columns(2)

    with cc1:
        st.markdown("### Vehicle A")
        b_a = st.selectbox(
            "Brand A", sorted(list(CAR_MODELS.keys())), key="ba"
        )
        m_a = st.selectbox(
            "Model A", list(CAR_MODELS[b_a].keys()), key="ma"
        )
        y_a = st.number_input("Year A", 2000, 2026, 2021, key="ya")
        km_a = st.number_input("KM A", 0, 500000, 40000, key="kma")
        cond_a = st.radio(
            "Condition A",
            ["Used (مستعمل)", "Zero (Brand New)", "Nearly New (كسر زيرو)"],
            key="cda",
        )
        t_a = st.selectbox("Transmission A", ["Automatic", "Manual"], key="ta")

    with cc2:
        st.markdown("### Vehicle B")
        b_b = st.selectbox(
            "Brand B", sorted(list(CAR_MODELS.keys())), key="bb"
        )
        m_b = st.selectbox(
            "Model B", list(CAR_MODELS[b_b].keys()), key="mb"
        )
        y_b = st.number_input("Year B", 2000, 2026, 2019, key="yb")
        km_b = st.number_input("KM B", 0, 500000, 90000, key="kmb")
        cond_b = st.radio(
            "Condition B",
            ["Used (مستعمل)", "Zero (Brand New)", "Nearly New (كسر زيرو)"],
            key="cdb",
        )
        t_b = st.selectbox("Transmission B", ["Automatic", "Manual"], key="tb")

    if st.button("Execute Matrix Comparison", key="btn_matrix"):
        p_a, _, _, _, _, _, _, h_a, _ = advanced_valuation(
            b_a, m_a, y_a, km_a, cond_a, t_a, "Petrol"
        )
        p_b, _, _, _, _, _, _, h_b, _ = advanced_valuation(
            b_b, m_b, y_b, km_b, cond_b, t_b, "Petrol"
        )

        st.markdown("---")
        res_a, res_b = st.columns(2)
        res_a.metric(
            f"{b_a} {m_a}",
            f"{p_a:,.0f} EGP",
            delta=f"Health Score: {h_a}%",
        )
        res_b.metric(
            f"{b_b} {m_b}",
            f"{p_b:,.0f} EGP",
            delta=f"Health Score: {h_b}%",
        )

        price_diff = abs(p_a - p_b)
        better_buy = (
            f"{b_a} {m_a}"
            if (p_a < p_b and h_a >= h_b)
            else f"{b_b} {m_b}"
            if p_b < p_a
            else f"{b_a} {m_a}"
        )
        st.info(
            f"💡 **Smart Recommendation Matrix:** **{better_buy}** offers a superior value proposition with a price variance of **{price_diff:,.0f} EGP**."
        )

# ==================== TAB 3 ====================
with tab3:
    st.subheader("📊 Local Automotive Market Price Distribution")
    st.write(
        "نظرة عامة على متوسط أسعار الفئات المختلفة داخل قاعدة البيانات المتكاملة:"
    )

    # تجميع عينة بيانات لعرض رسم بياني تحليلي
    market_sample = pd.DataFrame(
        [
            {"Category": "Economy / Sedans", "Average Price (EGP)": 1100000},
            {"Category": "SUVs & Crossovers", "Average Price (EGP)": 1850000},
            {"Category": "Luxury & Executive", "Average Price (EGP)": 4500000},
            {"Category": "Electric & Hybrid", "Average Price (EGP)": 2600000},
        ]
    )
    st.bar_chart(market_sample.set_index("Category"))