import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Car Price Predictor Pro", page_icon="🚗", layout="wide"
)

# ---------------------------------------------------------
# بيانات السيارات الشاملة مع سعة المحرك ونوع الهيكل
# ---------------------------------------------------------
CAR_MODELS = {
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
    "MG": (
        "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80"
    ),
    "Chery": (
        "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80"
    ),
}

# ---------------------------------------------------------
# تهيئة الـ Session State لحفظ سجل البحث
# ---------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------------
# واجهة التطبيق الجانبية (Sidebar) للفلترة والميزانية
# ---------------------------------------------------------
st.sidebar.title("🛠️ لوحة التحكم والإعدادات")
app_mode = st.sidebar.selectbox(
    "اختر القسم:",
    [
        "حاسبة وسعر السيارة (Predictor)",
        "مقارنة السيارات (Comparison)",
        "فلتر حسب الميزانية (Budget Finder)",
        "سجل البحث السابق (History)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 **المطورون:** سلمى أحمد & حبيبة عصام")

# ---------------------------------------------------------
# القسم الأول: التنبؤ بالسعر (الرئيسي)
# ---------------------------------------------------------
if app_mode == "حاسبة وسعر السيارة (Predictor)":
    st.title("🚗 نظام تقييم وتوقع أسعار السيارات المتقدم")
    st.markdown("---")

    col_input, col_img = st.columns([1.2, 1])

    with col_input:
        brand = st.selectbox("ماركة السيارة (Brand)", sorted(list(CAR_MODELS.keys())))
        available_models = list(CAR_MODELS[brand].keys())
        model_name = st.selectbox("موديل السيارة (Model)", available_models)

        # استخراج مواصفات الموديل الحالي
        car_info = CAR_MODELS[brand][model_name]
        st.info(
            f"ℹ️ **المواصفات الافتراضية:** المحرك: `{car_info['engine']}` | الهيكل: `{car_info['body']}` | القوة: `{car_info['hp']} حصان`"
        )

        transmission = st.selectbox("ناقل الحركة (Transmission)", ["Automatic", "Manual"])
        car_color = st.selectbox("لون السيارة", ["أبيض", "أسود", "فضي", "رمادي", "أحمر", "أزرق", "أخرى"])

    with col_img:
        img_url = CAR_IMAGES.get(
            brand,
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80",
        )
        st.image(img_url, caption=f"{brand} - {model_name} Preview", use_container_width=True)

    car_condition = st.radio(
        "حالة السيارة (Condition)",
        ["Zero (Brand New)", "Nearly New (كسر زيرو)", "Used (مستعمل)"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input("سنة الصنع (Manufacturing Year)", min_value=2000, max_value=2026, value=2020)
        fuel_type = st.selectbox("نوع الوقود (Fuel Type)", ["Petrol", "Diesel", "Hybrid", "Electric"])

    with col2:
        if car_condition == "Zero (Brand New)":
            km_driven = 0
            st.info("الكيلومترات المقطوعة: 0 كم (كسر زيرو / زيرو)")
        else:
            km_driven = st.number_input("الكيلومترات المقطوعة (KM)", min_value=0, max_value=500000, value=60000)

    st.markdown("---")

    if st.button("🚀 احسب السعر المتوقع الآن"):
        base_price = car_info["price"]

        years_old = 2026 - year
        age_depreciation = min(years_old * 0.035, 0.50)
        km_depreciation = min((km_driven / 20000) * 0.01, 0.15)
        trans_depreciation = 0.05 if transmission == "Manual" else 0.0

        total_depreciation = age_depreciation + km_depreciation + trans_depreciation

        if car_condition == "Zero (Brand New)":
            estimated_price = base_price
        elif car_condition == "Nearly New (كسر زيرو)":
            estimated_price = base_price * 0.92
        else:
            estimated_price = base_price * (1.0 - total_depreciation)
            estimated_price = max(estimated_price, base_price * 0.40)

        min_price = estimated_price * 0.95
        max_price = estimated_price * 1.05

        st.success(
            f"🎯 **السعر التقديري لـ ({brand} {model_name} - {year}):** {estimated_price:,.2f} جنيه مصري\n\n"
            f"📊 **النطاق المتوقع (هامش خطأ ±5%):** {min_price:,.2f} ج.م — {max_price:,.2f} ج.م"
        )

        # إضافة السجل إلى الـ Session State
        search_record = {
            "Brand": brand,
            "Model": model_name,
            "Year": year,
            "Estimated Price": f"{estimated_price:,.2f} EGP",
            "Condition": car_condition,
        }
        if search_record not in st.session_state.history:
            st.session_state.history.append(search_record)

        # رسم بياني للنطاق السعري
        chart_data = pd.DataFrame(
            {
                "الفئة": ["الحد الأدنى", "السعر التقديري", "الحد الأقصى"],
                "السعر (ج.م)": [min_price, estimated_price, max_price],
            }
        )
        st.subheader("📊 تحليل نطاق السعر")
        st.bar_chart(chart_data.set_index("الفئة"))

        # --- حاسبة التقسيط المصغرة ---
        st.markdown("---")
        st.subheader("💳 حاسبة الأقساط المقترحة")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            down_payment_pct = st.slider("نسبة المقدم (%)", 20, 70, 30)
            down_payment = estimated_price * (down_payment_pct / 100)
            loan_amount = estimated_price - down_payment
            st.write(f"مبلغ المقدم: **{down_payment:,.2f} ج.م**")
            st.write(f"مبلغ التمويل/القرض: **{loan_amount:,.2f} ج.م**")
        with col_p2:
            loan_years = st.selectbox("مدة التقسيط (بالسنوات)", [1, 2, 3, 4, 5])
            interest_rate = 0.15  # نسبة فائدة تقديرية سنوية 15%
            total_with_interest = loan_amount * (1 + (interest_rate * loan_years))
            monthly_installment = total_with_interest / (loan_years * 12)
            st.write(f"القسط الشهري التقريبي: **{monthly_installment:,.2f} ج.م / شهرياً**")

        # --- زر تصدير التقرير (CSV) ---
        st.markdown("---")
        report_df = pd.DataFrame([search_record])
        csv_data = report_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 تحميل تقرير السيارة (CSV)",
            data=csv_data,
            file_name=f"{brand}_{model_name}_report.csv",
            mime="text/csv",
        )

# ---------------------------------------------------------
# القسم الثاني: مقارنة السيارات
# ---------------------------------------------------------
elif app_mode == "مقارنة السيارات (Comparison)":
    st.title("⚖️ مقارنة بين سيارتين")
    st.markdown("قارن بين مواصفات وأسعار سيارتين جنباً إلى جنب.")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("السيارة الأولى")
        b1 = st.selectbox("الماركة 1", list(CAR_MODELS.keys()), key="b1")
        m1 = st.selectbox("الموديل 1", list(CAR_MODELS[b1].keys()), key="m1")
        info1 = CAR_MODELS[b1][m1]
        st.write(f"- السعر الأساسي: **{info1['price']:,.2f} ج.م**")
        st.write(f"- المحرك: **{info1['engine']}**")
        st.write(f"- الهيكل: **{info1['body']}**")
        st.write(f"- القوة: **{info1['hp']} حصان**")

    with c2:
        st.subheader("السيارة الثانية")
        b2 = st.selectbox("الماركة 2", list(CAR_MODELS.keys()), key="b2")
        m2 = st.selectbox("الموديل 2", list(CAR_MODELS[b2].keys()), key="m2")
        info2 = CAR_MODELS[b2][m2]
        st.write(f"- السعر الأساسي: **{info2['price']:,.2f} ج.م**")
        st.write(f"- المحرك: **{info2['engine']}**")
        st.write(f"- الهيكل: **{info2['body']}**")
        st.write(f"- القوة: **{info2['hp']} حصان**")

# ---------------------------------------------------------
# القسم الثالث: البحث حسب الميزانية
# ---------------------------------------------------------
elif app_mode == "فلتر حسب الميزانية (Budget Finder)":
    st.title("💰 البحث المتقدم حسب الميزانية")
    st.markdown("حدد ميزانيتك لنقترح عليك السيارات المناسبة المتاحة في القائمة.")

    max_budget = st.slider(
        "أقصى ميزانية لديك (بالجنيه المصري):",
        min_value=500000,
        max_value=7000000,
        value=1500000,
        step=50000,
    )

    matched_cars = []
    for brand_name, models in CAR_MODELS.items():
        for mod_name, data in models.items():
            if data["price"] <= max_budget:
                matched_cars.append(
                    {
                        "الماركة": brand_name,
                        "الموديل": mod_name,
                        "السعر التقديري": f"{data['price']:,.2f} ج.م",
                        "المحرك": data["engine"],
                        "الهيكل": data["body"],
                    }
                )

    if matched_cars:
        st.success(f"تم العثور على {lenطات := len(matched_cars)} سيارة تناسب ميزانيتك:")
        df_matched = pd.DataFrame(matched_cars)
        st.dataframe(df_matched, use_container_width=True)
    else:
        st.warning("عذراً، لا توجد سيارات أقل من هذه الميزانية في قاعدة البيانات الحالية.")

# ---------------------------------------------------------
# القسم الرابع: سجل البحث السابق
# ---------------------------------------------------------
elif app_mode == "سجل البحث السابق (History)":
    st.title("📋 سجل عمليات البحث الأخيرة")
    if st.session_state.history:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history, use_container_width=True)
        if st.button("مسح السجل"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("لا توجد عمليات بحث مسجلة حتى الآن. جرب البحث عن سيارة في القسم الرئيسي!")