import streamlit as st
import requests
from datetime import datetime

# -----------------------------------------------------
# إعداد الصفحة
# -----------------------------------------------------
st.set_page_config(page_title="نظام تسجيل الحضور", page_icon="📝", layout="centered")

# -----------------------------------------------------
# تحميل CSS
# -----------------------------------------------------
def load_css():
    for path in ["static/style.css", "style.css"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                return
        except FileNotFoundError:
            continue
load_css()

# -----------------------------------------------------
# رابط Google Apps Script
# -----------------------------------------------------
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbz3hXsAawAMpu4LPj26-xntDvGWutZdjwl4dS-o570jKedIGRvyEizljrO5TvOMUCSt0Q/exec"

# -----------------------------------------------------
# دالة لجلب عدد المسجلين
# -----------------------------------------------------
def get_registered_count():
    try:
        response = requests.get(GOOGLE_SHEET_URL, timeout=5)
        if response.status_code == 200:
            return int(response.text.strip())
        return None
    except Exception:
        return None

# -----------------------------------------------------
# تحديث العدّاد كل 30 ثانية
# -----------------------------------------------------
st.autorefresh(interval=30000, key="auto_refresh_count")

# -----------------------------------------------------
# الشعار + العنوان
# -----------------------------------------------------
st.markdown(
    '<div class="form-logo-wrapper"><svg viewBox="0 0 512 512"><circle cx="256" cy="256" r="200" fill="#f0f0f0"/><text x="50%" y="53%" text-anchor="middle" font-size="140">📝</text></svg></div>',
    unsafe_allow_html=True,
)
st.header("📋 تسجيل حضور الماستر كلاس")

# -----------------------------------------------------
# عرض العدّاد
# -----------------------------------------------------
count = get_registered_count()
if count is not None:
    st.markdown(
        f"<div style='text-align:center; font-size:18px; margin-bottom:15px;'>👥 عدد المسجلين حتى الآن: <b>{count}</b></div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        "<div style='text-align:center; color:#999;'>جارٍ تحميل عدد المسجلين...</div>",
        unsafe_allow_html=True,
    )

# -----------------------------------------------------
# session_state الثابت
# -----------------------------------------------------
defaults = {
    "name": "",
    "email": "",
    "selected_country": "🇦🇪 الإمارات",
    "phone_number": "",
    "masterclass": "كتابة المحتوى للسوشيال ميديا - أشرف سالم",
    "session": "اليوم الأول",
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -----------------------------------------------------
# قائمة أكواد الدول
# -----------------------------------------------------
country_codes = {
    "🇦🇪 الإمارات": "+971",
    "🇸🇦 السعودية": "+966",
    "🇪🇬 مصر": "+20",
    "🇶🇦 قطر": "+974",
    "🇰🇼 الكويت": "+965",
    "🇧🇭 البحرين": "+973",
    "🇴🇲 عمان": "+968",
    "🇯🇴 الأردن": "+962",
    "🇱🇧 لبنان": "+961",
}

# -----------------------------------------------------
# واجهة الإدخال (بدون تصفير)
# -----------------------------------------------------
name = st.text_input("الاسم الكامل", key="name")
email = st.text_input("البريد الإلكتروني", key="emai_
