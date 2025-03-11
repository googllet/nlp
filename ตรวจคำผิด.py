import streamlit as st
import os
import pandas as pd
from pdf_processing import extract_text_from_pdf, correct_text, save_text_to_pdf

UPLOAD_FOLDER = "uploads"
CORRECTED_FOLDER = "corrected_pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CORRECTED_FOLDER, exist_ok=True)

st.set_page_config(page_title="📝 ตรวจสอบคำผิด", layout="wide")
st.title("📝 ตรวจสอบคำผิดในเอกสาร PDF")

uploaded_file = st.file_uploader("📎 อัปโหลดไฟล์ PDF ของคุณ", type=["pdf"])

if uploaded_file is not None:
    pdf_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ อัปโหลดไฟล์สำเร็จ: `{uploaded_file.name}`")

    with st.spinner("📖 กำลังอ่านไฟล์..."):
        extracted_lines = extract_text_from_pdf(pdf_path)

    st.markdown("## 🔎 ข้อความจาก PDF")
    st.text_area("📃 ข้อความต้นฉบับ", "\n".join(extracted_lines), height=200)

    with st.spinner("🔍 กำลังตรวจคำผิด..."):
        corrected_lines, error_list = correct_text(extracted_lines)

    st.markdown("## 🛑 รายการคำผิดที่ตรวจพบ")

    if error_list:
        df_errors = pd.DataFrame(error_list, columns=["บรรทัดที่", "คำผิด", "ตัวเลือกทั้งหมด"])
        corrected_words = {}

        for index, row in df_errors.iterrows():
            col1, col2, col3 = st.columns([1, 2, 3])
            col1.write(f"📌 บรรทัดที่ {row['บรรทัดที่']}")
            col2.write(f"❌ {row['คำผิด']}")
            selected_correction = col3.selectbox(
                "เลือกคำที่ถูกต้อง",
                options=["(ไม่แก้ไข)"] + row["ตัวเลือกทั้งหมด"],
                key=f"correction_{index}"
            )
            if selected_correction != "(ไม่แก้ไข)":
                corrected_words[row["คำผิด"]] = selected_correction

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("✅ ใช้การแก้ไขที่เลือก"):
                for line_no in range(len(corrected_lines)):
                    for error, correction in corrected_words.items():
                        corrected_lines[line_no] = corrected_lines[line_no].replace(error, correction)
                st.text_area("📝 ข้อความที่ถูกต้อง", "\n".join(corrected_lines), height=200)

        with col_b:
            if st.button("🔄 แก้ไขอัตโนมัติ"):
                for line_no in range(len(corrected_lines)):
                    for error, suggestions in df_errors[["คำผิด", "ตัวเลือกทั้งหมด"]].values:
                        if suggestions:
                            corrected_lines[line_no] = corrected_lines[line_no].replace(error, suggestions[0])
                st.text_area("📝 ข้อความที่ถูกต้อง (อัตโนมัติ)", "\n".join(corrected_lines), height=200)

    else:
        st.success("✅ ไม่มีคำผิด!")
