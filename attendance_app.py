import streamlit as st
import requests
from datetime import datetime
import html
import streamlit.components.v1 as components
import base64
from pathlib import Path


def load_image_base64(img_path: str) -> str:
    img_bytes = Path(img_path).read_bytes()
    return base64.b64encode(img_bytes).decode("utf-8")

logo_base64 = load_image_base64("edraak_logo.png")  # غيّر المسار لو ملفك في مكان تاني

# -----------------------------------------------------

# -----------------------------------------------------
# هيدر الصفحة (لوجو + زر تسجيل)
# -----------------------------------------------------
st.markdown(
    f"""
    <div class="app-header">
        <div class="header-logo">
            <img src="data:image/png;base64,{logo_base64}" class="logo-img" />
        </div>
        <div class="cta-box">
            <span  class="header-cta">سجل حضورك في ماستر كلاس أكاديمية ادراك للإعلام</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
<style>

    /* تغيير لون ال-placeholder في selectbox */
    div[data-baseweb="select"] div[role="button"] span[data-testid="placeholder"] {
        color: #ffffff !important;
        opacity: 1 !important;
    }

    /* بعض النسخ بتحط الـ placeholder داخل div مش span */
    div[data-baseweb="select"] div[role="button"] div[data-testid="placeholder"] {
        color: #ffffff !important;
        opacity: 1 !important;
    }

    /* تغيير لون السهم */
    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------

# إعداد الصفحة العامة


# -----------------------------------------------------
st.set_page_config(
    page_title="تسجيل الحضور في ماستر كلاس اكاديمية ادراك للإعلام",
    page_icon="📝",
    layout="centered"
)

# -----------------------------------------------------
# تحميل CSS من ملف خارجي
# -----------------------------------------------------
def load_css():
    # تحميل خط Tajawal من Google Fonts
    st.markdown("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    # تحميل ملف CSS المخصص
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ ملف style.css غير موجود في نفس مجلد التطبيق.")


load_css()

# -----------------------------------------------------
# رابط Google Apps Script
# -----------------------------------------------------
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzSDT_YWKb-kttfuE8LD0di3fjHmN0fpr_q7EE6tSsdnbgaOdOWbG1338xwZ44jwq8GRg/exec"  # عدّل هذا بالرابط الصحيح

# -----------------------------------------------------
# قائمة أكواد الدول
# -----------------------------------------------------
country_codes = {
    "🇦🇪 الإمارات": "00971",
    "🇸🇦 السعودية": "00966",
    "🇪🇬 مصر": "0020",
    "🇸🇩 السودان": "00249",
    "🇯🇴 الأردن": "00962",
    "🇧🇭 البحرين": "00973",
    "🇶🇦 قطر": "00974",
    "🇰🇼 الكويت": "00965",
}

# -----------------------------------------------------
# القيم الافتراضية للمستخدم
# -----------------------------------------------------
defaults = {
    "name": "",
    "email": "",
    "selected_country": "🇦🇪 الإمارات",
    "phone_number": "",
    "masterclass": "",
    "session": "",
    "submission_status": None,
}

# -----------------------------------------------------
# تهيئة session_state بالقيم الافتراضية
# -----------------------------------------------------
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# فضي قيمة الماستر كلاس مرة واحدة أول تحميل
if "page_loaded" not in st.session_state:
    st.session_state["page_loaded"] = True
    st.session_state["masterclass"] = None

# -----------------------------------------------------
# جدول ربط كل ماستر كلاس باليوم/الوقت
# -----------------------------------------------------
MASTERCLASS_SCHEDULE = {
    "مهارات ذكاء إصطناعي لا يمكنك تجاهلها - فهمي متولي": "الإثنين 8 ديسمبر، 11:30 صباحاً",
    "تصميم العلامة التجارية في عصر الذكاء الإصطناعي - حذيفة تاج السر": "الإثنين 8 ديسمبر، 02:00 ظهراً",
    "فن صناعة المحتوى الإنساني - محمد الشريف وشهاب الهاشمي في ضيافة سارة الرفاعي": "الإثنين 8 ديسمبر، 03:00 عصراً",

    "كيف تكتب محتوى فيديو ناجح؟ - أشرف سالم الطنطاوي": "الثلاثاء 9 ديسمبر، 11:30 صباحاً",
    "خرافات التسويق - يحيى نايل": "الثلاثاء 9 ديسمبر، 02:00 ظهراً",
    "صناعة المحتوى التراثي – يوسف بالحمر ومحمد البلوشي وهزاع الشرياني": "الأربعاء 9 ديسمبر، 03:00 مساءاً",
}

MASTERCLASS_OPTIONS = list(MASTERCLASS_SCHEDULE.keys())

# أسماء مختصرة لعرضها داخل الكروت
MASTERCLASS_SHORT_NAMES = {
    "مهارات ذكاء إصطناعي لا يمكنك تجاهلها - فهمي متولي": "الذكاء الاصطناعي",
    "تصميم العلامة التجارية في عصر الذكاء الإصطناعي - حذيفة تاج السر": "العلامات التجارية",
    "فن صناعة المحتوى الإنساني - محمد الشريف وشهاب الهاشمي في ضيافة سارة الرفاعي": "صناعة المحتوى الإنساني",

    "كيف تكتب محتوى فيديو ناجح؟ - أشرف سالم الطنطاوي": "كتابة المحتوى",
    "خرافات التسويق - يحيى نايل": "خرافات التسويق",
    "صناعة المحتوى التراثي – يوسف بالحمر ومحمد البلوشي وهزاع الشرياني": "المحتوى التراثي",
}


# -----------------------------------------------------
# تهيئة session_state بالقيم الافتراضية
# -----------------------------------------------------
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -----------------------------------------------------
# دالة جلب عدد المسجلين (GET)
# -----------------------------------------------------
# -----------------------------------------------------
# دالة جلب كل الأعداد (الإجمالي + كل ماستر كلاس) في طلب واحد
# -----------------------------------------------------
@st.cache_data(ttl=30, show_spinner=False)
def get_all_counts():
    """
    تجيب عدد المسجلين الإجمالي + عدد كل ماستر كلاس
    من Google Apps Script (اللي بيرجع JSON).
    """
    try:
        r = requests.get(GOOGLE_SHEET_URL, timeout=5)
        if r.status_code == 200:
            return r.json()  # متوقَّع يرجّع dict فيه total وباقي الماستر كلاس
        return {}
    except Exception:
        return {}


# -----------------------------------------------------
# دالة الإرسال إلى Google Sheet (POST)
# -----------------------------------------------------
def send_to_google_sheet(record: dict) -> bool:
    try:
        res = requests.post(GOOGLE_SHEET_URL, json=record, timeout=8)
        return res.status_code == 200
    except Exception:
        return False


# -----------------------------------------------------
# دالة الإرسال وإعادة التعيين
# -----------------------------------------------------
def submit_and_reset_form():
    name = st.session_state["name"].strip()
    email = st.session_state["email"].strip()
    phone_number = st.session_state["phone_number"].strip()
    selected_country = st.session_state["selected_country"]
    masterclass = st.session_state.get("masterclass")

    # التحقق من اختيار الماستر كلاس
    if not masterclass:
        st.session_state["submission_status"] = "no_masterclass"
        return

    # تحديد اليوم/الوقت تلقائيًا بناءً على الماستر كلاس
    session = MASTERCLASS_SCHEDULE.get(masterclass, "")

    # التحقق من اكتمال البيانات الأساسية
    if not name or not email or not phone_number:
        st.session_state["submission_status"] = "incomplete"
        return


    # تجهيز رقم الهاتف مع كود الدولة
    full_phone = f"{country_codes[selected_country]} {phone_number}"

    # تجهيز البيانات لإرسالها إلى Google Sheet
    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "email": email,
        "phone": full_phone,
        "masterclass": masterclass,
        "session": session,
    }

    # إرسال البيانات
    if send_to_google_sheet(payload):
        st.session_state["submission_status"] = "success"

        # إعادة تعيين القيم بعد نجاح الإرسال
        st.session_state["name"] = ""
        st.session_state["email"] = ""
        st.session_state["phone_number"] = ""
        st.session_state["selected_country"] = defaults["selected_country"]

    st.session_state["masterclass"] = None
    st.session_state["session"] = ""


# -----------------------------------------------------
# اختيار الماستر كلاس + عرض الموعد (خارج الفورم)
# -----------------------------------------------------

MASTERCLASS_OPTIONS = list(MASTERCLASS_SCHEDULE.keys())

selected_masterclass = st.selectbox(
    label="اختر الماستر كلاس أو الجلسة الحوارية",
    options=MASTERCLASS_OPTIONS,
    index=None,                   # ما فيش اختيار افتراضي
    placeholder="اضغط هنا",  # يظهر داخل البوكس نفسه
    key="masterclass",
)

session_info = MASTERCLASS_SCHEDULE.get(selected_masterclass or "", "")

if session_info:
    st.info(
        f"""🕒 موعد هذا الماستر كلاس: {session_info}.

📍المكان: مركز أبوظبي الوطني للمعارض - جناح إدراك ميديا أكاديمي.
""",
    )


# -----------------------------------------------------
# نموذج إدخال البيانات (باستخدام st.form)
# -----------------------------------------------------
with st.form(key="attendance_form"):
    st.text_input("الاسم الكامل", key="name")
    st.text_input("البريد الإلكتروني", key="email")

    col_code, col_phone = st.columns([1, 2])
    with col_code:
        st.selectbox(
            "كود الدولة",
            list(country_codes.keys()),
            index=0,
            key="selected_country",
        )
    with col_phone:
        st.text_input("رقم الموبايل", placeholder="5xxxxxxxx", key="phone_number")

    st.form_submit_button(
        "تسجيل الحضور",
        use_container_width=True,
        on_click=submit_and_reset_form,
    )

# -----------------------------------------------------
# عرض رسالة الحالة بعد الإرسال
# -----------------------------------------------------
status = st.session_state["submission_status"]

if status == "success":
    st.success("✅ تم تسجيل حضورك بنجاح!")
    st.session_state["submission_status"] = None

elif status == "error":
    st.error(
        "⚠️ حدث خطأ أثناء الإرسال إلى Google Sheet. تأكد أن السكربت منشور كـ Web App ومتاح (Anyone)."
    )
    st.session_state["submission_status"] = None

elif status == "incomplete":
    st.warning("⚠️ الرجاء إدخال الاسم والبريد الإلكتروني ورقم الموبايل.")
    st.session_state["submission_status"] = None

elif status == "no_masterclass":
    st.warning("⚠️ الرجاء اختيار الماستر كلاس من القائمة أولاً.")
    st.session_state["submission_status"] = None


# -----------------------------------------------------
# ملاحظة أسفل الصفحة
# -----------------------------------------------------
st.markdown(
    """
    <div style='text-align:center; margin-top:40px; color:#666; font-size:0.9rem'>
        يتم حفظ جميع البيانات مباشرة في Google Sheet.<br>
        تأكد من أن رابط Google Apps Script مفعل للوصول العام (Anyone).
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("""
<style>
/* أي عنصر فيه كلمة viewerBadge */
div[class*="viewerBadge"],
a[class*="viewerBadge"],
div[class*="Badge"],
a[class*="Badge"] {
    display: none !important;
}

/* إخفاء link container */
div[class*="link_gzau3"],
a[class*="link_gzau3"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
