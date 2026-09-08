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

# قاعدة بيانات شاملة لكل الماركات والموديلات وسعات المحركات في السوق المصري
CAR_MODELS = {
    "تويوتا (Toyota)": {
        "كورولا (Corolla)": {
            "engines": ["1.6L Normal", "1.8L Hybrid"],
            "base_price": 1600000,
            "body": "Sedan",
            "hp": 120,
        },
        "ياريس (Yaris)": {
            "engines": ["1.5L Normal"],
            "base_price": 1000000,
            "body": "Hatchback",
            "hp": 118,
        },
        "فورتشنر (Fortuner)": {
            "engines": ["2.7L Normal", "4.0L V6"],
            "base_price": 3800000,
            "body": "SUV",
            "hp": 234,
        },
        "رانر / C-HR": {
            "engines": ["1.2L Turbo", "1.8L Hybrid"],
            "base_price": 1750000,
            "body": "SUV",
            "hp": 113,
        },
        "بلتا (Belta)": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 103,
        },
    },
    "نيسان (Nissan)": {
        "صني (Sunny)": {
            "engines": ["1.5L Normal"],
            "base_price": 800000,
            "body": "Sedan",
            "hp": 108,
        },
        "سنترا (Sentra)": {
            "engines": ["1.6L Normal"],
            "base_price": 1100000,
            "body": "Sedan",
            "hp": 118,
        },
        "قشقاي (Qashqai)": {
            "engines": ["1.3L Turbo"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 148,
        },
        "جوك (Juke)": {
            "engines": ["1.0L Turbo"],
            "base_price": 1300000,
            "body": "SUV",
            "hp": 114,
        },
    },
    "هيونداي (Hyundai)": {
        "النترا (Elantra CN7 / AD)": {
            "engines": ["1.6L Normal"],
            "base_price": 1300000,
            "body": "Sedan",
            "hp": 127,
        },
        "توسان (Tucson)": {
            "engines": ["1.6L Turbo"],
            "base_price": 1900000,
            "body": "SUV",
            "hp": 180,
        },
        "أكسنت (Accent RB)": {
            "engines": ["1.4L Normal"],
            "base_price": 900000,
            "body": "Sedan",
            "hp": 100,
        },
        "كريتا (Creta)": {
            "engines": ["1.5L Normal"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 113,
        },
        "آي 10 (i10)": {
            "engines": ["1.2L Normal"],
            "base_price": 700000,
            "body": "Hatchback",
            "hp": 84,
        },
    },
    "كيا (Kia)": {
        "سيراتو / كيه 3 (Cerato / K3)": {
            "engines": ["1.6L Normal"],
            "base_price": 1350000,
            "body": "Sedan",
            "hp": 130,
        },
        "سبورتاج (Sportage)": {
            "engines": ["1.6L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 177,
        },
        "بيجاس (Pegas)": {
            "engines": ["1.4L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 95,
        },
        "سيلتوس (Seltos)": {
            "engines": ["1.4L Turbo", "1.5L Normal"],
            "base_price": 1500000,
            "body": "SUV",
            "hp": 140,
        },
    },
    "إم جي (MG)": {
        "إم جي 5 (MG 5)": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 118,
        },
        "إم جي 6 (MG 6)": {
            "engines": ["1.5L Turbo"],
            "base_price": 1200000,
            "body": "Sedan",
            "hp": 169,
        },
        "إم جي زد إس (MG ZS)": {
            "engines": ["1.5L Normal"],
            "base_price": 1050000,
            "body": "SUV",
            "hp": 119,
        },
        "إم جي آر إكس 5 (MG RX5)": {
            "engines": ["1.5L Turbo"],
            "base_price": 1400000,
            "body": "SUV",
            "hp": 171,
        },
        "إم جي 4 (MG4 Electric)": {
            "engines": ["Electric EV"],
            "base_price": 1350000,
            "body": "Hatchback",
            "hp": 170,
        },
    },
    "شيري (Chery)": {
        "أريزو 5 (Arrizo 5)": {
            "engines": ["1.5L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 114,
        },
        "تيجو 3 (Tiggo 3)": {
            "engines": ["1.6L Normal"],
            "base_price": 880000,
            "body": "SUV",
            "hp": 126,
        },
        "تيجو 7 (Tiggo 7)": {
            "engines": ["1.5L Turbo"],
            "base_price": 1100000,
            "body": "SUV",
            "hp": 145,
        },
        "تيجو 8 (Tiggo 8 / Pro)": {
            "engines": ["1.5L Turbo", "1.6L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 145,
        },
    },
    "بي واي دي (BYD)": {
        "إف 3 (F3)": {
            "engines": ["1.5L Normal"],
            "base_price": 620000,
            "body": "Sedan",
            "hp": 108,
        },
        "سونج بلس (Song Plus Hybrid)": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1600000,
            "body": "SUV",
            "hp": 197,
        },
    },
    "شانجان (Changan)": {
        "ألسفين (Alsvin)": {
            "engines": ["1.4L Normal", "1.5L Normal"],
            "base_price": 650000,
            "body": "Sedan",
            "hp": 107,
        },
        "سي إس 35 بلس (CS35 Plus)": {
            "engines": ["1.4L Turbo"],
            "base_price": 1150000,
            "body": "SUV",
            "hp": 158,
        },
        "سي إس 55 بلس (CS55 Plus)": {
            "engines": ["1.5L Turbo"],
            "base_price": 1350000,
            "body": "SUV",
            "hp": 185,
        },
    },
    "جيلي (Geely)": {
        "إمجراند (Emgrand)": {
            "engines": ["1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 102,
        },
        "كولراي (Coolray)": {
            "engines": ["1.5L Turbo"],
            "base_price": 1300000,
            "body": "SUV",
            "hp": 175,
        },
        "أوكافانجو (Okavango)": {
            "engines": ["1.5L Hybrid"],
            "base_price": 1650000,
            "body": "SUV",
            "hp": 190,
        },
    },
    "سكودا (Skoda)": {
        "أوكتافيا (Octavia)": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 1850000,
            "body": "Sedan",
            "hp": 150,
        },
        "كودياك (Kodiaq)": {
            "engines": ["1.4L Turbo", "2.0L Turbo"],
            "base_price": 2600000,
            "body": "SUV",
            "hp": 150,
        },
        "كاروك (Karoq)": {
            "engines": ["1.4L Turbo"],
            "base_price": 2100000,
            "body": "SUV",
            "hp": 150,
        },
        "سكالا (Scala)": {
            "engines": ["1.6L Normal"],
            "base_price": 1300000,
            "body": "Hatchback",
            "hp": 110,
        },
    },
    "بي إم دبليو (BMW)": {
        "الفئة الثالثة (320i)": {
            "engines": ["2.0L Turbo"],
            "base_price": 3500000,
            "body": "Sedan",
            "hp": 184,
        },
        "الفئة الخامسة (520i)": {
            "engines": ["2.0L Turbo"],
            "base_price": 4800000,
            "body": "Sedan",
            "hp": 184,
        },
        "إكس 1 (X1)": {
            "engines": ["1.5L Turbo"],
            "base_price": 2900000,
            "body": "SUV",
            "hp": 140,
        },
        "إكس 5 (X5)": {
            "engines": ["3.0L Turbo"],
            "base_price": 6200000,
            "body": "SUV",
            "hp": 340,
        },
    },
    "مرسيدس (Mercedes-Benz)": {
        "سي كلاس (C180 / C200)": {
            "engines": ["1.5L Turbo", "2.0L Turbo"],
            "base_price": 4200000,
            "body": "Sedan",
            "hp": 170,
        },
        "إي كلاس (E200)": {
            "engines": ["2.0L Turbo"],
            "base_price": 5800000,
            "body": "Sedan",
            "hp": 197,
        },
        "جي إل سي (GLC)": {
            "engines": ["2.0L Turbo"],
            "base_price": 5900000,
            "body": "SUV",
            "hp": 204,
        },
        "إيه كلاس (A200)": {
            "engines": ["1.3L Turbo"],
            "base_price": 2700000,
            "body": "Hatchback",
            "hp": 136,
        },
    },
    "أودي (Audi)": {
        "أودي إيه 4 (A4)": {
            "engines": ["2.0L Turbo"],
            "base_price": 2800000,
            "body": "Sedan",
            "hp": 190,
        },
        "أودي إيه 6 (A6)": {
            "engines": ["2.0L Turbo"],
            "base_price": 3900000,
            "body": "Sedan",
            "hp": 245,
        },
        "أودي كيو 3 (Q3)": {
            "engines": ["1.4L Turbo"],
            "base_price": 2500000,
            "body": "SUV",
            "hp": 150,
        },
        "أودي كيو 7 (Q7)": {
            "engines": ["3.0L Turbo"],
            "base_price": 4900000,
            "body": "SUV",
            "hp": 340,
        },
    },
    "شيفروليه (Chevrolet)": {
        "أوبترا (Optra)": {
            "engines": ["1.5L Normal"],
            "base_price": 750000,
            "body": "Sedan",
            "hp": 110,
        },
        "كابتيفا (Captiva)": {
            "engines": ["1.5L Turbo"],
            "base_price": 1500000,
            "body": "SUV",
            "hp": 148,
        },
        "أفيو (Aveo)": {
            "engines": ["1.5L Normal"],
            "base_price": 600000,
            "body": "Sedan",
            "hp": 105,
        },
    },
    "رينو (Renault)": {
        "ميجان (Megane)": {
            "engines": ["1.6L Normal", "1.3L Turbo"],
            "base_price": 1400000,
            "body": "Sedan",
            "hp": 115,
        },
        "لوجان (Logan)": {
            "engines": ["1.6L Normal"],
            "base_price": 650000,
            "body": "Sedan",
            "hp": 110,
        },
        "داستر (Duster)": {
            "engines": ["1.6L Normal"],
            "base_price": 1200000,
            "body": "SUV",
            "hp": 115,
        },
        "ستيبواي (Sandero Stepway)": {
            "engines": ["1.6L Normal"],
            "base_price": 850000,
            "body": "Hatchback",
            "hp": 110,
        },
    },
    "فيات (Fiat)": {
        "تيبو (Tipo)": {
            "engines": ["1.4L Normal", "1.6L Normal"],
            "base_price": 1050000,
            "body": "Sedan",
            "hp": 110,
        },
        "فيات 500 (500)": {
            "engines": ["1.4L Normal"],
            "base_price": 1100000,
            "body": "Hatchback",
            "hp": 100,
        },
    },
    "بيجو (Peugeot)": {
        "بيجو 301 (301)": {
            "engines": ["1.6L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 115,
        },
        "بيجو 508 (508)": {
            "engines": ["1.6L Turbo"],
            "base_price": 1800000,
            "body": "Sedan",
            "hp": 165,
        },
        "بيجو 2008 (2008)": {
            "engines": ["1.2L Turbo"],
            "base_price": 1450000,
            "body": "SUV",
            "hp": 130,
        },
        "بيجو 3008 (3008)": {
            "engines": ["1.6L Turbo"],
            "base_price": 1950000,
            "body": "SUV",
            "hp": 180,
        },
        "بيجو 5008 (5008)": {
            "engines": ["1.6L Turbo"],
            "base_price": 2200000,
            "body": "SUV",
            "hp": 180,
        },
    },
    "سوزوكي (Suzuki)": {
        "سويفت (Swift)": {
            "engines": ["1.2L Normal"],
            "base_price": 750000,
            "body": "Hatchback",
            "hp": 84,
        },
        "ديزاير / سياز (Ciaz / Dzire)": {
            "engines": ["1.2L Normal", "1.5L Normal"],
            "base_price": 850000,
            "body": "Sedan",
            "hp": 104,
        },
        "إرتيجا (Ertiga)": {
            "engines": ["1.5L Normal"],
            "base_price": 950000,
            "body": "Van",
            "hp": 103,
        },
    },
}

# تهيئة الـ Session State
if "history" not in st.session_state:
    st.session_state.history = []

# القائمة الجانبية
st.sidebar.title("🛠️ لوحة التحكم العربية الشاملة")
app_mode = st.sidebar.selectbox(
    "اختر القسم:",
    [
        "توقع أسعار السيارات بالتفصيل",
        "مقارنة بين سيارتين",
        "البحث بالميزانية المتاحة",
        "سجل البحث السابق",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 **المطورون:** Salma Ahmed & Habiba Essam")

# ================= 1. قسم توقع أسعار السيارات بالتفصيل =================
if app_mode == "توقع أسعار السيارات بالتفصيل":
    st.title("🚗 نظام توقع وتحديد أسعار السيارات في مصر")
    st.markdown(
        "اختر الماركة، الموديل، سعة المحرك، والإضافات الخاصة بالسيارة للحصول على سعر دقيق."
    )
    st.markdown("---")

    col_input, col_info_box = st.columns([1.3, 1])

    with col_input:
        # اختيار الماركة
        brand = st.selectbox(
            "اختر ماركة السيارة (Brand)", sorted(list(CAR_MODELS.keys()))
        )

        # اختيار الموديل بناء على الماركة
        available_models = list(CAR_MODELS[brand].keys())
        model_name = st.selectbox("اختر موديل السيارة (Model)", available_models)

        car_data = CAR_MODELS[brand][model_name]

        # اختيار سعة المحرك المتاحة لهذا الموديل
        selected_engine = st.selectbox(
            "اختر سعة وتكوين المحرك (Engine Capacity)", car_data["engines"]
        )

        # ناقل الحركة
        transmission = st.selectbox(
            "ناقل الحركة (Transmission)", ["أوتوماتيك (Automatic)", "مانيوال (Manual)"]
        )

        # سنة الصنع
        year = st.slider("سنة الصنع (Manufacturing Year)", 2010, 2026, 2022)

        # حالة السيارة
        car_condition = st.radio(
            "حالة السيارة العامة",
            ["زيرو (جديدة تماماً)", "كسر زيرو (بحالة الوكالة)", "مستعملة بحالة جيدة"],
            horizontal=True,
        )

        # المسافة المقطوعة
        if car_condition == "زيرو (جديدة تماماً)":
            km_driven = 0
            st.info("السيارة جديدة تماماً (0 كم)")
        else:
            km_driven = st.number_input(
                "عداد المسافات المقطوعة (بالكيلومتر)",
                min_value=0,
                max_value=400000,
                value=50000,
                step=5000,
            )

    with col_info_box:
        st.subheader("✨ الإضافات والكماليات (Extras)")
        st.markdown("حدد الميزات والكماليات المتوفرة في السيارة:")

        has_sunroof = st.checkbox("☀️ فتحة سقف / سقف زجاجي بانوراما (+2.5%)")
        has_leather = st.checkbox("💺 فرش جلد طبيعي للمقاعد (+1.5%)")
        has_start_engine = st.checkbox("🔑 بصمة تشغيل ونظام دخول ذكي (+1.5%)")
        has_sensors_cam = st.checkbox(
            "📷 كاميرا خلفية وحساسات парковки (+1.5%)"
        )
        has_alloy_wheels = st.checkbox("🛞 جنوط رياضية أصلية (+1%)")
        has_screens = st.checkbox("📱 شاشة وسائط ذكية وتحكم طارة (+1%)")

        st.markdown("---")
        st.info(
            f"ℹ️ **المواصفات الأساسية:**\n- نمط الهيكل: `{car_data['body']}`\n- الققدرة الحصانية: `{car_data['hp']} حصان`\n- المحرك المختار: `{selected_engine}`"
        )

    st.markdown("---")

    if st.button("🚀 احسب السعر النهائي المتوقع"):
        base_price = car_data["base_price"]

        # تعديل السعر حسب نوع المحرك المختار
        if "Turbo" in selected_engine or "Hybrid" in selected_engine:
            base_price *= 1.08
        if "V6" in selected_engine or "Electric" in selected_engine:
            base_price *= 1.15

        # حساب الاستهلاك والعمر
        years_old = 2026 - year
        age_dep = min(years_old * 0.03, 0.45)
        km_dep = min((km_driven / 15000) * 0.012, 0.20)
        trans_dep = 0.05 if "مانيوال" in transmission else 0.0

        total_depreciation = 1.0 - (age_dep + km_dep + trans_dep)

        if car_condition == "زيرو (جديدة تماماً)":
            estimated_price = base_price
        elif car_condition == "كسر زيرو (بحالة الوكالة)":
            estimated_price = base_price * 0.96
        else:
            estimated_price = base_price * max(total_depreciation, 0.35)

        # إضافة قيمة الإضافات والكماليات
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

        # عرض النتائج باللغة العربية
        st.success(
            f"🎯 **السعر التقديري للسيارة ({brand} - {model_name}):**\n"
            f"### `{estimated_price:,.2f}` جنيه مصري\n\n"
            f"📊 **النطاق المتوقع في السوق المصري:** `{min_price:,.2f}` ج.م إلى `{max_price:,.2f}` ج.م"
        )

        # حفظ البحث في السجل
        search_record = {
            "الماركة": brand,
            "الموديل": model_name,
            "المحرك": selected_engine,
            "سنة الصنع": year,
            "السعر المتوقع": f"{estimated_price:,.2f} ج.م",
            "الحالة": car_condition,
        }
        if search_record not in st.session_state.history:
            st.session_state.history.append(search_record)

        # رسم بياني توضيحي
        chart_data = pd.DataFrame(
            {
                "الفئة": ["الحد الأدنى", "السعر المتوقع", "الحد الأقصى"],
                "السعر بالجنيه": [min_price, estimated_price, max_price],
            }
        )
        st.subheader("📊 تحليل نطاق الأسعار")
        st.bar_chart(chart_data.set_index("الفئة"))

        # حاسبة التقسيط بالجنيه
        st.markdown("---")
        st.subheader("💳 حاسبة الأقساط البنكية المقترحة")
        cp1, cp2 = st.columns(2)
        with cp1:
            down_payment_pct = st.slider("نسبة المقدم (%)", 20, 70, 30)
            down_payment = estimated_price * (down_payment_pct / 100)
            loan_amt = estimated_price - down_payment
            st.write(f"مقدم الحجز: **{down_payment:,.2f} ج.م**")
            st.write(f"مبلغ التمويل / القرض: **{loan_amt:,.2f} ج.م**")
        with cp2:
            duration = st.selectbox("مدة التقسيط (بالسنوات)", [1, 2, 3, 4, 5, 7])
            interest_rate = 0.16  # 16% فائدة سنوية تقريبية
            total_with_interest = loan_amt * (1 + (interest_rate * duration))
            monthly = total_with_interest / (duration * 12)
            st.write(f"قيمة القسط الشهري التقريبي: **{monthly:,.2f} ج.م / شهرياً**")

        # تصدير التقرير
        st.markdown("---")
        csv_bytes = pd.DataFrame([search_record]).to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 تحميل تقرير السيارة (CSV)",
            data=csv_bytes,
            file_name="car_price_report.csv",
            mime="text/csv",
        )


# ================= 2. قسم مقارنة بين سيارتين =================
elif app_mode == "مقارنة بين سيارتين":
    st.title("⚖️ مقارنة شاملة بين سيارتين في السوق المصري")
    st.markdown("قارن المواصفات والأسعار والقوة الحصانية جنباً إلى جنب.")

    mc1, mc2 = st.columns(2)

    with mc1:
        st.subheader("السيارة الأولى")
        b1 = st.selectbox("ماركة 1", sorted(list(CAR_MODELS.keys())), key="b1")
        m1 = st.selectbox("موديل 1", list(CAR_MODELS[b1].keys()), key="m1")
        info1 = CAR_MODELS[b1][m1]
        st.write(f"- السعر المبدئي: **{info1['base_price']:,.2f} ج.م**")
        st.write(f"- الهيكل: **{info1['bod