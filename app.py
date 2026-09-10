import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# 1. إعدادات الصفحة والتصميم
# ---------------------------------------------------------
st.set_page_config(
    page_title="Egyptian Ultimate Car Market Analyzer & Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stButton>button {
        width: 100%;
        background-color: #e63946;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.7rem;
        font-size: 16px;
    }
    .stButton>button:hover { background-color: #c1121f; color: white; }
    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        border-bottom: 4px solid #e63946;
    }
    .metric-card h4 { color: #6c757d; margin-bottom: 8px; font-size: 15px; }
    .metric-card h2 { color: #1d3557; margin: 0; font-size: 26px; font-weight: bold; }
    .spec-badge {
        background-color: #e9ecef;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 500;
        display: inline-block;
        margin: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. قاعدة بيانات الماركات والفئات والأسعار مرجعية (EGP)
# ---------------------------------------------------------
CAR_DATA = {
    "Toyota": {
        "models": ["Corolla", "Yaris", "Fortuner", "C-HR", "RAV4", "Camry", "Belta", "Rumion"],
        "base_price": 1150000,
        "multiplier": 1.15,
        "image": "https://images.unsplash.com/photo-1629897048983-85f8dc4e4abc?auto=format&fit=crop&q=80&w=800"
    },
    "Hyundai": {
        "models": ["Elantra HD", "Elantra CN7", "Elantra AD", "Tucson", "Accent RB", "Creta", "I10", "Bayon"],
        "base_price": 850000,
        "multiplier": 1.0,
        "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=800"
    },
    "Kia": {
        "models": ["Sportage", "Cerato / Grand Cerato", "Rio", "Picanto", "Sorento", "Pegas", "Exceed"],
        "base_price": 950000,
        "multiplier": 1.05,
        "image": "https://images.unsplash.com/photo-1583121274602-3e2820c69888?auto=format&fit=crop&q=80&w=800"
    },
    "Nissan": {
        "models": ["Sunny", "Sentra", "Qashqai", "Juke", "X-Trail"],
        "base_price": 750000,
        "multiplier": 0.92,
        "image": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&q=80&w=800"
    },
    "MG": {
        "models": ["MG 5", "MG ZS", "MG 6", "MG RX5 / RX5 Plus", "MG HS", "MG ONE"],
        "base_price": 800000,
        "multiplier": 0.95,
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
    },
    "Chery": {
        "models": ["Arrizo 5", "Tiggo 3", "Tiggo 7", "Tiggo 8", "Tiggo 4 Pro"],
        "base_price": 720000,
        "multiplier": 0.88,
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=800"
    },
    "BMW": {
        "models": ["320i / 330i", "520i / 530i", "X1", "X3", "X5", "4 Series", "1 Series"],
        "base_price": 2800000,
        "multiplier": 2.2,
        "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&q=80&w=800"
    },
    "Mercedes-Benz": {
        "models": ["C180 / C200", "E200 / E300", "A180 / A200", "GLA", "GLC", "CLA"],
        "base_price": 3200000,
        "multiplier": 2.5,
        "image": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&q=80&w=800"
    },
    "Skoda": {
        "models": ["Octavia", "Kodiaq", "Karoq", "Superb", "Kamiq", "Scala"],
        "base_price": 1350000,
        "multiplier": 1.25,
        "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&q=80&w=800"
    },
    "Volkswagen": {
        "models": ["Passat", "Tiguan", "Golf", "Polo", "T-Roc"],
        "base_price": 1400000,
        "multiplier": 1.3,
        "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&q=80&w=800"
    },
    "Renault": {
        "models": ["Logan", "Sandero / Stepway", "Duster", "Megane", "Kadjar", "Austral"],
        "base_price": 700000,
        "multiplier": 0.87,
        "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&q=80&w=800"
    },
    "Peugeot": {
        "models": ["301", "508", "2008", "3008", "5008"],
        "base_price": 1100000,
        "multiplier": 1.1,
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
    },
    "Fiat": {
        "models": ["Tipo", "500", "Punto", "500X"],
        "base_price": 750000,
        "multiplier": 0.9,
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=800"
    },
    "Chevrolet": {
        "models": ["Optra", "Aveo", "Captiva", "Lanos", "Cruze"],
        "base_price": 600000,
        "multiplier": 0.82,
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&q=80&w=800"
    },
    "Suzuki": {
        "models": ["Swift / Swift Dzire", "Ciaz", "Ertiga", "Baleno", "Vitara", "Espresso"],
        "base_price": 650000,
        "multiplier": 0.85,
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&q=80&w=800"
    },
    "Mitsubishi": {
        "models": ["Lancer EX (Shark)", "Eclipse Cross", "Xpander", "Attrage"],
        "base_price": 800000,
        "multiplier": 0.98,
        "image": "https://images.unsplash.com/photo-1609521263047-f8f205293f24?auto=format&fit=crop&q=80&w=800"
    }
}

# ---------------------------------------------------------
# 3. واجهة المستخدم والتصميم الرئيسي
# ---------------------------------------------------------
st.title("🚗 Egyptian Ultimate Used Car Valuation & Market System")
st.markdown("##### 🏆 Professional Market Valuation System | Developed by **Habiba Essam** & **Salma Ahmed**")
st.write("يقوم هذا النظام المطور بتحليل مواصفات السيارات وتقييم قيمتها السوقية العادلة في السوق المصري مع إمكانيات حساب الأقساط واستهلاك الوقود.")

st.sidebar.header("🔍 مواصفات السيارة التفصيلية")

# اختيار الماركة والموديل
brand = st.sidebar.selectbox("اختر ماركة السيارة (Brand)", list(CAR_DATA.keys()))
model = st.sidebar.selectbox("اختر الفئة / الموديل (Model)", CAR_DATA[brand]["models"])

# المواصفات الفنية
st.sidebar.subheader("⚙️ المواصفات الفنية")
year = st.sidebar.slider("سنة الصنع (Manufacturing Year)", 2005, 2026, 2021)
body_type = st.sidebar.selectbox("نوع الهيكل (Body Style)", ["Sedan", "SUV / Crossover", "Hatchback", "Coupe"])
transmission = st.sidebar.radio("ناقل الحركة (Transmission)", ["Automatic", "Manual"], horizontal=True)
engine_cc = st.sidebar.select_slider("سعة المحرك (Engine CC)", options=[1000, 1200, 1400, 1500, 1600, 2000, 2500, 3000, 4000], value=1600)
is_turbo = st.sidebar.checkbox("المحرك مزود بـ شاحن توربو (Turbocharged)?", value=False)
hp = st.sidebar.number_input("القوة الحصانية التقريبية (Horsepower HP)", min_value=70, max_value=500, value=120)
fuel_type = st.sidebar.selectbox("نوع الوقود (Fuel Type)", ["Petrol (80/92/95)", "Diesel", "Hybrid", "Electric"])

# حالة السيارة والمسافة
st.sidebar.subheader("🛠️ حالة السيارة والدهان")
mileage = st.sidebar.number_input("المسافة المقطوعة (Mileage - KM)", min_value=0, max_value=500000, value=60000, step=5000)
paint_condition = st.sidebar.selectbox("حالة الدهان الخارجي (Paint State)", [
    "فابريكا بالكامل (Factory Original)",
    "رشة حزام نظافة (Belt Repainted)",
    "رشة بره بالكامل (Fully Repainted Outside)",
    "مرشوشة أجزاء معينة (Partial Repairs)"
])
mechanical_condition = st.sidebar.slider("كفاءة المحرك والفتيس والفرش (%)", 50, 100, 90)

# عرض صورة مرجعية للماركة
if "image" in CAR_DATA[brand]:
    st.sidebar.image(CAR_DATA[brand]["image"], caption=f"مرجع ماركة {brand}", use_container_width=True)

# ---------------------------------------------------------
# 4. خوارزمية التقييم والتسعير المتقدمة (Valuation Engine)
# ---------------------------------------------------------
current_year = 2026
age = current_year - year

# السعر الأساسي للماركة
base = CAR_DATA[brand]["base_price"] * CAR_DATA[brand]["multiplier"]

# تأثير الفئة والقوة والتوربو
if is_turbo:
    base *= 1.12
if body_type == "SUV / Crossover":
    base *= 1.15
elif body_type == "Hatchback":
    base *= 0.92

base += (hp - 100) * 2000

# إهلاك السنين والمسافة
depreciation_year = age * 0.05  # 5% إهلاك عن كل سنة
depreciation_km = (mileage / 10000) * 0.015  # 1.5% إهلاك لكل 10,000 كم

total_depreciation = min(0.65, depreciation_year + depreciation_km)
val_after_dep = base * (1 - total_depreciation)

# خصومات حالة الدهان
paint_multipliers = {
    "فابريكا بالكامل (Factory Original)": 1.0,
    "رشة حزام نظافة (Belt Repainted)": 0.93,
    "مرشوشة أجزاء معينة (Partial Repairs)": 0.88,
    "رشة بره بالكامل (Fully Repainted Outside)": 0.82
}
val_after_paint = val_after_dep * paint_multipliers[paint_condition]

# تأثير الكفاءة الميكانيكية
calculated_price = val_after_paint * (mechanical_condition / 100)

# السعر النهائي ونطاق التداول
final_price = max(100000, int(calculated_price))
lower_price = int(final_price * 0.94)
upper_price = int(final_price * 1.06)

# ---------------------------------------------------------
# 5. التبويبات والشاشات الرئيسية (Tabs UI)
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 التقييم والتسعير", 
    "📊 تقرير وتفاصيل السيارة", 
    "📉 حاسبة القروض والأقساط", 
    "⛽ استهلاك الوقود والتكاليف",
    "📈 تحليلات السوق المصري"
])

# ----- Tab 1: التقييم -----
with tab1:
    st.subheader("💵 السعر السوقي العادل المتوقع (Market Valuation)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h4>متوسط السعر العادل</h4><h2>{final_price:,} EGP</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h4>الحد الأدنى للشراء</h4><h2>{lower_price:,} EGP</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h4>الحد الأقصى للتفاوض</h4><h2>{upper_price:,} EGP</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"✅ **ملخص التقييم:** سيارة **{brand} {model}** موديل **{year}** - ناقل حركة **{transmission}** وبحالة دهان **{paint_condition}**.")
    st.info("💡 **ملاحظة:** يستند هذا التقييم إلى أسعار حركة البيع والشراء الفعلية في المعارض والمنصات المصرية بناءً على حالة الدهان والمسافة المقطوعة والكفاءة الميكانيكية.")

# ----- Tab 2: المواصفات التفصيلية -----
with tab2:
    st.subheader("📋 بطاقة المواصفات وتقييم الإهلاك")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("### 🚘 بيانات السيارة المختارة")
        st.markdown(f"- **الماركة والموديل:** {brand} - {model}")
        st.markdown(f"- **سنة الصنع:** {year} ({age} سنوات استخدام)")
        st.markdown(f"- **نوع الهيكل:** {body_type}")
        st.markdown(f"- **سعة المحرك:** {engine_cc} CC {'(Turbo)' if is_turbo else ''}")
        st.markdown(f"- **القوة الحصانية:** {hp} HP")
        st.markdown(f"- **نوع الناقل والوقود:** {transmission} | {fuel_type}")

    with col_b:
        st.write("### 🛠️ تقييم الحالة الإجمالية")
        st.markdown(f"- **المسافة المقطوعة:** {mileage:,} KM")
        st.markdown(f"- **حالة الهيكل والدهان:** {paint_condition}")
        st.markdown(f"- **درجة الكفاءة الميكانيكية:** {mechanical_condition}%")
        
        # مؤشر كفاءة
        st.progress(mechanical_condition / 100)

# ----- Tab 3: حاسبة الأقساط -----
with tab3:
    st.subheader("📉 حاسبة تمويل السيارات والأقساط الشهرية")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        down_payment = st.number_input("المقدم المدفوع (EGP)", min_value=0, max_value=final_price, value=int(final_price * 0.3), step=25000)
    with col_in2:
        loan_months = st.selectbox("مدة التمويل (بالأشهر)", [12, 24, 36, 48, 60, 72, 84], index=2)
    with col_in3:
        interest_rate = st.slider("الفائدة السنوية المتوقعة (%)", 8.0, 35.0, 22.0, step=0.5)

    loan_amount = max(0, final_price - down_payment)
    monthly_interest = (interest_rate / 100) / 12
    
    if monthly_interest > 0 and loan_amount > 0:
        monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest)**loan_months) / ((1 + monthly_interest)**loan_months - 1)
    else:
        monthly_payment = loan_amount / loan_months if loan_months > 0 else 0

    st.markdown("---")
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("مبلغ التمويل المتبقي", f"{int(loan_amount):,} EGP")
    with res_col2:
        st.metric("القسط الشهري المتوقع", f"{int(monthly_payment):,} EGP / شهر")

# ----- Tab 4: الوقود والتكاليف -----
with tab4:
    st.subheader("⛽ حساب استهلاك الوقود والتكاليف التشغيلية")
    
    # حساب الاستهلاك التقريبي لكل 100 كم
    base_consumption = 6.0 + (engine_cc / 1000) * 1.5
    if is_turbo:
        base_consumption -= 0.5
    if fuel_type == "Hybrid":
        base_consumption *= 0.6
    
    est_consumption = round(base_consumption, 1)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        monthly_km = st.slider("معدل القيادة الشهرية المتوقع (KM)", 500, 5000, 1500, step=100)
        fuel_price_per_liter = st.number_input("سعر لتر الوقود الحالي (EGP)", min_value=5.0, max_value=30.0, value=15.0, step=0.5)
    
    with col_f2:
        monthly_liters = (monthly_km / 100) * est_consumption
        monthly_fuel_cost = monthly_liters * fuel_price_per_liter
        
        st.metric("معدل الاستهلاك", f"{est_consumption} لتر / 100 كم")
        st.metric("تكلفة الوقود الشهرية المتوقعة", f"{int(monthly_fuel_cost):,} EGP")

# ----- Tab 5: تحليلات السوق -----
with tab5:
    st.subheader("📈 متوسط الأسعار ومقارنة العلامات التجارية")
    st.write("جدول مقارنة بمتوسط أسعار السيارات المستعملة الأكثر طلباً في السوق المصري:")
    
    market_df = pd.DataFrame({
        "الماركة (Brand)": list(CAR_DATA.keys()),
        "متوسط السعر التقريبي (EGP)": [int(v["base_price"] * v["multiplier"]) for v in CAR_DATA.values()]
    })
    
    st.bar_chart(market_df.set_index("الماركة (Brand)"))

# ---------------------------------------------------------
# 6. التذييل (Footer)
# ---------------------------------------------------------
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6c757d;'>Egyptian Ultimate Car Valuation System | Developed by <b>Habiba Essam</b> & <b>Salma Ahmed</b></p>", unsafe_allow_html=True)
