import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# --------------------------- Page Config ---------------------------
# إعدادات الصفحة
st.set_page_config(page_title="نظام تسجيل الحضور", page_icon="📝", layout="centered")

# --------------------------- CSS Loader ----------------------------
# دالة تحميل ملف الأنماط (CSS)
def load_css():
    css_candidates = ["static/style.css", "style.css"]
    for p in css_candidates:
        try:
            with open(p, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                return
        except FileNotFoundError:
            continue

load_css()

# --------------------------- Data setup ----------------------------
DATA_FILE = Path("attendance_data.csv")
# قائمة الأعمدة المحدثة مع حقول الهاتف
COLUMNS = ["timestamp", "name", "email", "masterclass", "session", "phone_code", "phone_number"]

MASTERCLASSES = [
    "كيف تتحقق من الأخبار باستخدام الذكاء الاصطناعي - فهمي متولي",
    "كتابة المحتوى للسوشيال ميديا - أشرف سالم",
    "كتابة وصياغة الأخبار للسوشيال ميديا - محمد عواد",
    "تصحيح مفاهيم التسويق الرقمي - يحيى نايل",
]
SESSIONS = ["اليوم الأول", "اليوم الثاني", "اليوم الثالث"]

# قائمة أكواد الدول
COUNTRY_CODES = [
    "+966 (السعودية)", "+971 (الإمارات)", "+20 (مصر)",
    "+962 (الأردن)", "+965 (الكويت)", "+974 (قطر)", "+973 (البحرين)",
    "+961 (لبنان)", "+212 (المغرب)", "+213 (الجزائر)", "+90 (تركيا)"
]

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """تحميل البيانات من ملف CSV، مع التأكد من وجود كل الأعمدة."""
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            # التأكد من وجود كل الأعمدة المطلوبة
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            return df[COLUMNS]
        except Exception:
            return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(columns=COLUMNS)

def append_record(record: dict):
    """إضافة سجل جديد إلى ملف CSV."""
    df = load_data()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    # مسح الـ cache لعرض البيانات الجديدة فوراً
    load_data.clear()

@st.cache_data(show_spinner=False)
def get_today_data(df: pd.DataFrame) -> pd.DataFrame:
    """فلترة البيانات لعرض سجلات اليوم الحالي فقط."""
    if df.empty:
        return df
    try:
        d = pd.to_datetime(df["timestamp"])
        today = pd.Timestamp.now().date()
        return df[d.dt.date == today]
    except Exception:
        return df.tail(50)

# --------------------------- Form UI -------------------------------

# وضع الشعار داخل البطاقة البيضاء (باستخدام كلاس CSS الجديد)
st.markdown(
    '<div class="form-logo-wrapper"><svg viewBox="0 0 512 512"><circle cx="256" cy="256" r="200" fill="#f0f0f0"/><text x="50%" y="53%" text-anchor="middle" font-size="140" font-family="sans-serif">📝</text></svg></div>',
    unsafe_allow_html=True
)

st.header("📋 تسجيل حضور الماستر كلاس")

name = st.text_input("الاسم الكامل")
email = st.text_input("البريد الإلكتروني")

# استخدام عمودين لحقل الهاتف وكود الدولة
col_phone_code, col_phone_num = st.columns([1, 2], gap="small")

with col_phone_code:
    phone_code = st.selectbox("كود الدولة", COUNTRY_CODES, index=0)
    
with col_phone_num:
    phone_number = st.text_input("رقم الهاتف", placeholder="أدخل رقم الهاتف")


masterclass = st.selectbox("اختر الماستر كلاس", MASTERCLASSES, index=1)
session = st.selectbox("اختر اليوم / الجلسة", SESSIONS, index=0)

# استخدام عمودين لأزرار الإرسال والتفريغ
col_submit, col_clear = st.columns([2,1], gap="small")

with col_submit:
    submit = st.button("تسجيل الحضور", use_container_width=True)
with col_clear:
    clear = st.button("تفريغ الحقول", use_container_width=True)

if clear:
    # لإعادة تحميل الصفحة ومسح جميع الحقول
    st.experimental_rerun()

if submit:
    # التحقق من المدخلات الأساسية
    if not name.strip() or not email.strip() or not phone_number.strip():
        st.warning