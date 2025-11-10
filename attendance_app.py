import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# --------------------------- Page Config ---------------------------
st.set_page_config(page_title="نظام تسجيل الحضور", page_icon="📝", layout="centered")

# --------------------------- CSS Loader ----------------------------
# ... (الدالة load_css كما هي) ...
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
# 🆕 تحديث قائمة الأعمدة
COLUMNS = ["timestamp", "name", "email", "masterclass", "session", "phone_code", "phone_number"]

MASTERCLASSES = [
    "كيف تتحقق من الأخبار باستخدام الذكاء الاصطناعي - فهمي متولي",
    "كتابة المحتوى للسوشيال ميديا - أشرف سالم",
    "كتابة وصياغة الأخبار للسوشيال ميديا - محمد عواد",
    "تصحيح مفاهيم التسويق الرقمي - يحيى نايل",
]
SESSIONS = ["اليوم الأول", "اليوم الثاني", "اليوم الثالث"]

# 🆕 قائمة أكواد الدول (الأكثر شيوعاً)
COUNTRY_CODES = [
    "+966 (السعودية)", "+971 (الإمارات)", "+20 (مصر)",
    "+962 (الأردن)", "+965 (الكويت)", "+974 (قطر)", "+973 (البحرين)",
    "+961 (لبنان)", "+212 (المغرب)", "+213 (الجزائر)", "+90 (تركيا)"
]
# ... (بقية دوال load_data و append_record و get_today_data كما هي) ...
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
            # Ensure required columns
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""
            # Fill new phone columns with empty string if reading an old file
            if "phone_code" not in df.columns: df["phone_code"] = ""
            if "phone_number" not in df.columns: df["phone_number"] = ""
            return df[COLUMNS]
        except Exception:
            return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(columns=COLUMNS)

def append_record(record: dict):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    load_data.clear()

@st.cache_data(show_spinner=False)
def get_today_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    try:
        d = pd.to_datetime(df["timestamp"])
        today = pd.Timestamp.now().date()
        return df[d.dt.date == today]
    except Exception:
        return df.tail(50)

# --------------------------- Form UI -------------------------------

st.markdown(
    '<div class="form-logo-wrapper"><svg viewBox="0 0 512 512"><circle cx="256" cy="256" r="200" fill="#f0f0f0"/><text x="50%" y="53%" text-anchor="middle" font-size="140" font-family="sans-serif">📝</text></svg></div>',
    unsafe_allow_html=True
)

st.header("📋 تسجيل حضور الماستر كلاس")

name = st.text_input("الاسم الكامل")
email =