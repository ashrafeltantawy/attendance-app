import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Attendance App", page_icon="📝", layout="centered")

# تحميل CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# خلفية الموجة
st.markdown("<div class='wave-bg'></div>", unsafe_allow_html=True)

# مسافة علشان المحتوى يظهر بعد الموجة
st.markdown("<div style='height:180px'></div>", unsafe_allow_html=True)

# عرض الشعار
from pathlib import Path
logo_path = Path("static/logo.svg")
if logo_path.exists():
    with open(logo_path, "r") as f:
        logo_data = f.read()
    st.markdown(
        f"""
        <div style='text-align:center; margin-bottom:10px;'>
            {logo_data}
        </div>
        """,
        unsafe_allow_html=True
    )

# العنوان الرئيسي
st.title("نموذج تسجيل الحضور")

st.write("املأ البيانات التالية. النموذج متجاوب ويعمل باللمس على الآيباد أو الهاتف.")

# -------------------- ملف حفظ البيانات --------------------
DATA_FILE = "attendance.xlsx"

# -------------------- دوال التحقق --------------------
phone_re = re.compile(r"^\+?\d{7,15}$")
email_re = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_phone(p):
    return bool(phone_re.match(p.strip()))

def validate_email(e):
    return bool(email_re.match(e.strip()))

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_excel(DATA_FILE)
        except Exception:
            return pd.DataFrame(columns=["الاسم", "التليفون", "الإيميل", "تاريخ التسجيل"])
    else:
        return pd.DataFrame(columns=["الاسم", "التليفون", "الإيميل", "تاريخ التسجيل"])

def save_data(df: pd.DataFrame):
    df.to_excel(DATA_FILE, index=False)

# -------------------- نموذج الإدخال --------------------
with st.form(key="attendance_form"):
    name = st.text_input("👤 الاسم الكامل")
    phone = st.text_input("📞 التليفون (مثال: +971501234567 أو 0501234567)")
    email = st.text_input("✉️ الإيميل")
    submitted = st.form_submit_button("✅ سجّل الحضور")

if submitted:
    errors = []
    if not name.strip():
        errors.append("الاسم مطلوب.")
    if not phone.strip() or not validate_phone(phone):
        errors.append("أدخل رقم تليفون صالح (7-15 رقم).")
    if not email.strip() or not validate_email(email):
        errors.append("أدخل إيميل صالح.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        df = load_data()
        new_row = {
            "الاسم": name.strip(),
            "التليفون": phone.strip(),
            "الإيميل": email.strip(),
            "تاريخ التسجيل": pd.Timestamp.now()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        try:
            save_data(df)
            st.success("تم التسجيل بنجاح ✅")
        except Exception as ex:
            st.error(f"حصل خطأ أثناء الحفظ: {ex}")

# -------------------- زر تحميل البيانات فقط --------------------
df = load_data()

if not df.empty:
    towrite = BytesIO()
    with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='attendance')
    towrite.seek(0)

    st.download_button(
        label="⬇️ تحميل قاعدة البيانات كـ Excel",
        data=towrite,
        file_name=DATA_FILE,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

st.markdown("---")
st.markdown("""
**ملاحظات:**
- التطبيق متجاوب ويعمل على الشاشات اللمسية مثل iPad و iPhone.
- لتشغيله: `python3 -m pip install streamlit pandas openpyxl` ثم `python3 -m streamlit run attendance_app.py`.
""")
