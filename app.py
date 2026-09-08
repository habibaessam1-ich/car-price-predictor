import io
import json
import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="Car Price Predictor Pro - Ultimate Edition",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# قاعدة البيانات الشاملة للسيارات والمواصفات
CAR_MODELS = {
    "Nissan": {
        "Sunny": {
            "price": 800000,
            "engine": "1.5L",
            "body": "Sedan",
            "hp": 108,
            "fuel_consumption": 6.9,
        },
        "Sentra": {
            "price": 1100000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 118,
            "fuel_consumption": 7.1,
        },
        "Qashqai": {
            "price": 1650000,
            "engine": "1.3L Turbo",
            "body": "SUV",
            "hp": 148,
            "fuel_consumption": 6.5,
        },
        "Juke": {
            "price": 1300000,
            "engine": "1.0L Turbo",
            "body": "SUV",
            "hp": 114,
            "fuel_consumption": 5.8,
        },
    },
    "Toyota": {
        "Corolla": {
            "price": 1600000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 120,
            "fuel_consumption": 6.8,
        },
        "Yaris": {
            "price": 1000000,
            "engine": "1.5L",
            "body": "Hatchback",
            "hp": 118,
            "fuel_consumption": 4.9,
        },
        "Fortuner": {
            "price": 3800000,
            "engine": "4.0L",
            "body": "SUV",
            "hp": 234,
            "fuel_consumption": 11.5,
        },
        "C-HR": {
            "price": 1750000,
            "engine": "1.2L Turbo",
            "body": "SUV",
            "hp": 113,
            "fuel_consumption": 6.0,
        },
    },
    "Hyundai": {
        "Elantra": {
            "price": 1300000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 127,
            "fuel_consumption": 7.0,
        },
        "Tucson": {
            "price": 1900000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 180,
            "fuel_consumption": 7.5,
        },
        "Accent": {
            "price": 900000,
            "engine": "1.4L",
            "body": "Sedan",
            "hp": 100,
            "fuel_consumption": 6.4,
        },
        "Creta": {
            "price": 1400000,
            "engine": "1.5L",
            "body": "SUV",
            "hp": 113,
            "fuel_consumption": 6.7,
        },
    },
    "Kia": {
        "Cerato / K3": {
            "price": 1350000,
            "engine": "1.6L",
            "body": "Sedan",
            "hp": 130,
            "fuel_consumption": 6.9,
        },
        "Sportage": {
            "price": 1950000,
            "engine": "1.6L Turbo",
            "body": "SUV",
            "hp": 177,
            "fuel_consumption": 7.6,
        },
        "Pegas": {
            "price": 850000,
            "engine": "1.4L",
            "body": "Sedan",
            "hp": 95,
            "fuel_consumption": 6.1,
        },
        "Seltos": {
            "price": 1500000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 140,
            "fuel_consumption": 6.3,
        },
    },
    "BMW": {
        "3 Series (320i)": {
            "price": 3500000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 184,
            "fuel_consumption": 6.3,
        },
        "5 Series (520i)": {
            "price": 4800000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 184,
            "fuel_consumption": 6.7,
        },
        "X1": {
            "price": 2900000,
            "engine": "1.5L Turbo",
            "body": "SUV",
            "hp": 140,
            "fuel_consumption": 6.5,
        },
        "X5": {
            "price": 6200000,
            "engine": "3.0L Turbo",
            "body": "SUV",
            "hp": 340,
            "fuel_consumption": 9.2,
        },
    },
    "Mercedes": {
        "C-Class (C180)": {
            "price": 4200000,
            "engine": "1.5L Turbo",
            "body": "Sedan",
            "hp": 170,
            "fuel_consumption": 6.5,
        },
        "E-Class (E200)": {
            "price": 5800000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 197,
            "fuel_consumption": 7.0,
        },
        "GLC": {
            "price": 5900000,
            "engine": "2.0L Turbo",
            "body": "SUV",
            "hp": 204,
            "fuel_consumption": 7.4,
        },
    },
    "Audi": {
        "A4": {
            "price": 2800000,
            "engine": "2.0L Turbo",
            "body": "Sedan",
            "hp": 190,
            "fuel_consumption": 6.1,
        },
        "Q3": {
            "price": 2500000,
            "engine": "1.4L Turbo",
            "body": "SUV",
            "hp": 150,
            "fuel_consumption": 6.8,
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
    "Audi": (
        "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=800&q=80"
    ),
}

# تهيئة الـ Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# القائمة الجانبية المتقدمة
st.sidebar.title("🛠️ لوحة التحكم الشاملة")
app_mode = st.sidebar.selectbox(
    "اختر القسم:",
    [
        "توقع الأسعار الذكي",
        "مقارنة السيارات المتقدمة",
        "مكتشف الميزانية الشامل",
        "إحصائيات وتحليلات السوق",
        "سجل البحث والمفضلة",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 **المطورون:** Salma Ahmed & Habiba Essam")

# ================= 1. قسم توقع الأسعار الذكي =================
if app_mode == "توقع الأسعار الذكي":
    st.title("🚗 نظام توقع أسعار السيارات المتقدم والذكي")
    st.markdown("---")

    col_input, col_img = st.columns([1.2, 1])

    with col_input:
        brand = st.selectbox("ماركة السيارة (Brand)", sorted(list(CAR_MODELS.keys())))
        available_models = list(CAR_MODELS[brand].keys())
        model_name = st.selectbox("موديل السيارة (Model)", available_models)

        car_info = CAR_MODELS[brand][model_name]
        st.info(
            f"ℹ️ **المواصفات الأساسية:** المحرك: `{car_info['engine']}` | الهيكل: `{car_info['body']}` | القوة: `{car_info['hp']} HP` | استهلاك الوقود: `{car_info['fuel_consumption']}L/100km`"
        )

        transmission = st.selectbox(
            "ناقل الحركة (Transmission)", ["Automatic", "Manual"]
        )
        car_color = st.selectbox(
            "لون السيارة",
            ["أبيض", "أسود", "فضي", "رمادي", "أحمر", "أزرق", "ألوان أخرى"],
        )

    with col_img:
        img_url = CAR_IMAGES.get(
            brand,
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80",
        )
        st.image(
            img_url,
            caption=f"{brand} - {model_name} معاينة",
            use_container_width=True,
        )

    car_condition = st.radio(
        "حالة السيارة",
        ["زيرو (جديدة تماماً)", "حالة الزيرو (كسر زيرو)", "مستعملة"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input(
            "سنة الصنع", min_value=2005, max_value=2026, value=2022
        )
        fuel_type = st.selectbox(
            "نوع الوقود", ["بنزين", "هجين (Hybrid)", "كهرباء", "ديزل"]
        )

    with col2:
        if car_condition == "زيرو (جديدة تماماً)":
            km_driven = 0
            st.success("المسافة المقطوعة: 0 كم (زيرو)")
        else:
            km_driven = st.number_input(
                "المسافة المقطوعة (كم)",
                min_value=0,
                max_value=500000,
                value=40000,
                step=5000,
            )

    # تفاصيل إضافية متقدمة
    with st.exparker("⚙️ خيارات متقدمة (حالة الدهان والصيانة)") if hasattr(st, 'exparker') else st.container():
        st.write("تقييم هيكل السيارة:")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            has_scratch = st.checkbox("خربوش بسيط / رش صاج خارجي")
        with col_b:
            has_accident = st.checkbox("حوادث سابقة (تأثير على الشاسيه)")
        with col_c:
            agency_maintenance = st.checkbox("صيانة دورية بالتوكيل")

    st.markdown("---")

    if st.button("🚀 احسب السعر المتوقع الآن"):
        base_price = car_info["price"]
        years_old = 2026 - year

        # معادلة حساب الاستهلاك والخصم الذكية
        age_depreciation = min(years_old * 0.03, 0.45)
        km_depreciation = min((km_driven / 15000) * 0.012, 0.20)
        trans_dep = 0.04 if transmission == "Manual" else 0.0
        accident_dep = 0.15 if has_accident else (0.05 if has_scratch else 0.0)
        agency_bonus = 0.05 if agency_maintenance else 0.0

        total_factor = (
            1.0
            - age_depreciation
            - km_depreciation
            - trans_dep
            - accident_dep
            + agency_bonus
        )

        if car_condition == "زيرو (جديدة تماماً)":
            estimated_price = base_price
        elif car_condition == "حالة الزيرو (كسر زيرو)":
            estimated_price = base_price * 0.95
        else:
            estimated_price = base_price * max(total_factor, 0.35)

        min_price = estimated_price * 0.94
        max_price = estimated_price * 1.06

        st.success(
            f"🎯 **السعر التقديري لـ ({brand} {model_name} - {year}):** `{estimated_price:,.2f}` جنيه مصري\n\n"
            f"📊 **النطاق المتوقع للسوق (هامش خطأ ±6%):** `{min_price:,.2f}` ج.م — `{max_price:,.2f}` ج.م"
        )

        # حفظ في السجل
        search_record = {
            "Brand": brand,
            "Model": model_name,
            "Year": year,
            "Estimated Price": f"{estimated_price:,.2f} EGP",
            "Condition": car_condition,
        }
        if search_record not in st.session_state.history:
            st.session_state.history.append(search_record)

        # رسم بياني للتحليل
        chart_df = pd.DataFrame(
            {
                "الفئة": ["الحد الأدنى", "السعر المتوقع", "الحد الأقصى"],
                "السعر (جنيه)": [min_price, estimated_price, max_price],
            }
        )
        st.subheader("📊 تحليل نطاق الأسعار")
        st.bar_chart(chart_df.set_index("الفئة"))

        # حاسبة التقسيط المتقدمة
        st.markdown("---")
        st.subheader("💳 حاسبة الأقساط والتمويل الشاملة")
        cp1, cp2 = st.columns(2)
        with cp1:
            down_payment_pct = st.slider("مقدم الحجز (%)", 20, 80, 30, key="dp1")
            down_payment = estimated_price * (down_payment_pct / 100)
            loan_amount = estimated_price - down_payment
            st.write(f"مبلغ المقدم: **{down_payment:,.2f} ج.م**")
            st.write(f"إجمالي قيمة القرض: **{loan_amount:,.2f} ج.م**")
        with cp2:
            loan_years = st.selectbox(
                "فترة السداد (بالسنوات)", [1, 2, 3, 4, 5, 7], key="ly1"
            )
            annual_interest = 0.16  # نسبة فائدة سنوية افتراضية
            total_interest = loan_amount * (1 + (annual_interest * loan_years))
            monthly_installment = total_interest / (loan_years * 12)
            st.write(
                f"القسط الشهري التقريبي: **{monthly_installment:,.2f} ج.م / شهرياً**"
            )

        # أزرار التنزيل والتصدير
        st.markdown("---")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            csv_data = pd.DataFrame([search_record]).to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 تنزيل تقرير السيارة (CSV)",
                data=csv_data,
                file_name=f"{brand}_{model_name}_report.csv",
                mime="text/csv",
            )
        with col_d2:
            json_data = json.dumps(search_record, ensure_ascii=False, indent=4)
            st.download_button(
                label="📥 تنزيل تقرير السيارة (JSON)",
                data=json_data,
                file_name=f"{brand}_{model_name}_report.json",
                mime="application/json",
            )


# ================= 2. قسم مقارنة السيارات المتقدمة =================
elif app_mode == "مقارنة السيارات المتقدمة":
    st.title("⚖️ مقارنة شاملة جنباً إلى جنب بين سيارتين")
    st.markdown(
        "قارن بين مواصفات، أسعار، استهلاك الوقود، وقوة المحرك لسيارتين مختلفتين بدقة."
    )

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("السيارة الأولى")
        b1 = st.selectbox("الماركة 1", list(CAR_MODELS.keys()), key="comp_b1")
        m1 = st.selectbox(
            "الموديل 1", list(CAR_MODELS[b1].keys()), key="comp_m1"
        )
        info1 = CAR_MODELS[b1][m1]
        st.markdown(
            f"""
        - 💰 السعر الأساسي: **{info1['price']:,.2f} ج.م**
        - 🏎️ المحرك: **{info1['engine']}**
        - 🚗 نمط الهيكل: **{info1['body']}**
        - ⚡ قوة الحصان: **{info1['hp']} HP**
        - ⛽ استهلاك الوقود: **{info1['fuel_consumption']} L/100km**
        """
        )

    with col_c2:
        st.subheader("السيارة الثانية")
        b2 = st.selectbox("الماركة 2", list(CAR_MODELS.keys()), key="comp_b2")
        m2 = st.selectbox(
            "الموديل 2", list(CAR_MODELS[b2].keys()), key="comp_m2"
        )
        info2 = CAR_MODELS[b2][m2]
        st.markdown(
            f"""
        - 💰 السعر الأساسي: **{info2['price']:,.2f} ج.م**
        - 🏎️ المحرك: **{info2['engine']}**
        - 🚗 نمط الهيكل: **{info2['body']}**
        - ⚡ قوة الحصان: **{info2['hp']} HP**
        - ⛽ استهلاك الوقود: **{info2['fuel_consumption']} L/100km**
        """
        )

    st.markdown("---")
    st.subheader("📊 مقارنة الأداء والقوة")
    comp_chart_df = pd.DataFrame(
        {
            "المؤشر": ["السعر (بالألف)", "قوة الحصان (HP)", "استهلاك الوقود"],
            f"{b1} {m1}": [
                info1["price"] / 1000,
                info1["hp"],
                info1["fuel_consumption"] * 10,
            ],
            f"{b2} {m2}": [
                info2["price"] / 1000,
                info2["hp"],
                info2["fuel_consumption"] * 10,
            ],
        }
    )
    st.bar_chart(comp_chart_df.set_index("المؤشر"))


# ================= 3. قسم مكتشف الميزانية الشامل =================
elif app_mode == "مكتشف الميزانية الشامل":
    st.title("💰 مكتشف السيارات حسب الميزانية المتاحة")
    st.markdown("حدد ميزانيتك القصوى وسيعرض لك التطبيق كل السيارات المتاحة فوراً.")

    user_budget = st.slider(
        "أقصى ميزانية متاح (جنيه مصري):",
        min_value=600000,
        max_value=7000000,
        value=1800000,
        step=50000,
    )

    body_filter = st.selectbox(
        "تصفية حسب نمط الهيكل (اختياري)",
        ["الكل", "Sedan", "SUV", "Hatchback"],
    )

    matching_cars = []
    for brand_name, models in CAR_MODELS.items():
        for mod_name, data in models.items():
            if data["price"] <= user_budget:
                if body_filter == "الكل" or data["body"] == body_filter:
                    matching_cars.append(
                        {
                            "الماركة": brand_name,
                            "الموديل": mod_name,
                            "السعر التقديري": f"{data['price']:,.2f} ج.م",
                            "المحرك": data["engine"],
                            "الهيكل": data["body"],
                            "القدرة الحصانية": f"{data['hp']} HP",
                        }
                    )

    if matching_cars:
        st.success(
            f"🎉 وجدنا {len(matching_cars)} سيارة تتناسب مع ميزانيتك وشروطك:"
        )
        st.dataframe(pd.DataFrame(matching_cars), use_container_width=True)
    else:
        st.warning(
            "عذراً، لا توجد سيارات مطابقة لهذه الميزانية في قاعدة البيانات الحالية."
        )


# ================= 4. قسم إحصائيات وتحليلات السوق =================
elif app_mode == "إحصائيات وتحليلات السوق":
    st.title("📈 لوحة إحصائيات وتحليلات سوق السيارات")
    st.markdown(
        "نظرة عامة على الأسعار والمتوسطات العامة داخل قاعدة البيانات."
    )

    all_prices = [
        data["price"]
        for brand in CAR_MODELS.values()
        for data in brand.values()
    ]
    avg_price = sum(all_prices) / len(all_prices)

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    col_stat1.metric("إجمالي الموديلات المتاحة", len(all_prices))
    col_stat2.metric("متوسط أسعار السوق", f"{avg_price:,.0f} ج.م")
    col_stat3.metric("عدد الماركات العالمية", len(CAR_MODELS))

    st.markdown("---")
    st.subheader("📊 توزيع الأسعار حسب الماركات")
    brand_avg_prices = {
        b: sum(d["price"] for d in m.values()) / len(m)
        for b, m in CAR_MODELS.items()
    }
    st.bar_chart(pd.Series(brand_avg_prices))


# ================= 5. قسم سجل البحث والمفضلة =================
elif app_mode == "سجل البحث والمفضلة":
    st.title("📋 سجل عمليات البحث السابقة")

    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

        if st.button("🗑️ مسح سجل البحث بالكامل"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info(
            "لا يوجد سجل بحث حتى الآن. قم بتجربة قسم توقع الأسعار لإنشاء سجلات جديدة!"
        )