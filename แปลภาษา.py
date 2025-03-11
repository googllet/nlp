import streamlit as st
import os
from pdf_processing import translate_text, save_text_to_pdf
from googletrans import LANGUAGES

TRANSLATED_FOLDER = "translated_pdfs"
os.makedirs(TRANSLATED_FOLDER, exist_ok=True)

st.set_page_config(page_title="🌍 แปลภาษา", layout="wide")
st.title("🌍 แปลภาษาเอกสาร PDF")

lang_options = {f"{lang_name} ({lang_code})": lang_code for lang_code, lang_name in LANGUAGES.items()}
selected_lang = st.selectbox("📌 เลือกภาษาที่ต้องการแปล:", list(lang_options.keys()))

uploaded_file = st.file_uploader("📎 อัปโหลดไฟล์ PDF ของคุณ", type=["pdf"])

if uploaded_file is not None:
    pdf_path = os.path.join(TRANSLATED_FOLDER, uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ อัปโหลดไฟล์สำเร็จ: `{uploaded_file.name}`")

    with st.spinner("🌍 กำลังแปลภาษา..."):
        translated_lines = translate_text(pdf_path, target_lang=lang_options[selected_lang])

    st.markdown(f"## 🌍 ข้อความที่ถูกแปล ({selected_lang})")
    st.text_area("📜 ข้อความที่แปลแล้ว", "\n".join(translated_lines), height=200)
