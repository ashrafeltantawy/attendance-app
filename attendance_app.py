import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# -------------------- إعداد الصفحة --------------------
st.set_page_config(
    page_title="Attendance Form",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- تحميل ملف CSS --------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("static/style.css")

# -------------------- عرض اللوجو --------------------
st.markdown(
    """
    <div style='text-align:center;'>
        <img src='static/logo.svg' class='logo' alt='logo'>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("📝 Attendance App Test")

st.write("If you can see this text, the rendering issue was caused by CSS or layout.")

name = st.text_input("Full Name")
phone = st.text_input("Phone")
email = st.text_input("Email")

if st.button("Submit"):
    st.success(f"Recorded: {name} - {phone} - {email}")
