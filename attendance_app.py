import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="نظام تسجيل الحضور", page_icon="📝", layout="centered")

def load_css():
    for path in ["static/style.css", "style.css"]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
                return
        except FileNotFoundError:
            continue
load_css()

GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw8cBRPqxDeBT2PMxdijsMApk1kqBvfHW_XzPzTfDGsn9TTiIut4xxwXgpkKPV0dr3d0Q/exec"

def get_registered_count():
    try:
        r = requests.get(GOOGLE_SHEET_URL, timeout=5)
        return int(r.text.strip()) if r.status_code == 200 else None
    except Exception:
        return None

# --------------------------
# default state
# --------------------------
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

if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

# --------------------------
# header
# --------------------------
st.markdown(
    '<div class="form-logo-wrapper"><svg viewBox="0 0 512 512"><circle cx="256" cy="256" r="200" fill="#f0f0f0"/><text x="50%" y="53%" text-anchor="middle" font-size="140">📝</text></svg></div>',
    unsafe_allow_html=True,
)
st.header("📋 تسجيل حضور الماستر كلاس")

count = get_registered_count()
if count is not None:
    st.markdown(f"<div style='text-align:center;font-size:18px;'>👥 عدد المسجلين: <b>{count}</b></div>", unsafe_allow_html=True)

country_codes = {
    "🇦🇪 الإمارات": "+971", "🇸🇦 السعودية": "+966", "🇪🇬 مصر": "+20",
    "🇶🇦 قطر": "+974", "🇰🇼 الكويت": "+965", "🇧🇭 البحرين": "+973",
    "🇴🇲 عمان": "+968", "🇯🇴 الأردن": "+962", "🇱🇧 لبنان": "+961",
}

# --------------------------
# form
# --------------------------
if not st.session_state.reset_flag:
    name = st.text_input("الاسم الكامل", key="name")
    email = st.text_input("البريد الإلكتروني", key="email")

    col1, col2 = st.columns([1,2])
    with col1:
        selected_country = st.selectbox("كود الدولة", list(country_codes.keys()), key="selected_country")
    with col2:
        phone_number = st.text_input("رقم الموبايل", placeholder="5xxxxxxxx", key="phone_number")

    masterclass = st.selectbox(
        "اختر الماستر كلاس",
        [
            "كيف تتحقق من الأخبار باستخدام الذكاء الاصطناعي - فهمي متولي",
            "كتابة المحتوى للسوشيال ميديا - أشرف سالم",
            "كتابة وصياغة الأخبار للسوشيال ميديا - محمد عواد",
            "تصحيح مفاهيم التسويق الرقمي - يحيى نايل",
        ],
        key="masterclass"
    )

    session = st.selectbox(
        "اختر اليوم / الجلسة",
        ["اليوم الأول", "اليوم الثاني", "اليوم الثالث"],
        key="session"
    )

    success_box = st.empty()

    if st.button("تسجيل الحضور", use_container_width=True):
        if not name.strip() or not email.strip() or not phone_number.strip():
            st.warning("⚠️ الرجاء إدخال جميع الحقول.")
        else:
            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name.strip(),
                "email": email.strip(),
                "phone": f"{country_codes[selected_country]} {phone_number.strip()}",
                "masterclass": masterclass,
                "session": session,
            }
            try:
                ok = requests.post(GOOGLE_SHEET_URL, json=record, timeout=5).status_code == 200
            except Exception:
                ok = False

            if ok:
                success_box.success("✅ تم تسجيل حضورك بنجاح!")
                st.session_state.reset_flag = True
                st.rerun()
            else:
                st.error("⚠️ لم يتم الاتصال بـ Google Sheet.")

# --------------------------
# clear state after rerun
# --------------------------
else:
    st.success("✅ تم تسجيل حضورك بنجاح!")
    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state.reset_flag = False

st.markdown(
    "<div style='text-align:center;margin-top:40px;color:#666;font-size:0.9rem'>يتم حفظ جميع البيانات مباشرة في Google Sheet.<br>تأكد أن الرابط متاح للجميع (Anyone can access).</div>",
    unsafe_allow_html=True,
)
