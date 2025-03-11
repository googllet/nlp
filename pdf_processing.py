import fitz  # PyMuPDF
import language_tool_python
from googletrans import Translator

tool = language_tool_python.LanguageTool('en-US')
translator = Translator()

def extract_text_from_pdf(pdf_path):
    """ ดึงข้อความจาก PDF และแยกเป็นบรรทัด """
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        text.extend(page.get_text("text").split("\n"))  # แยกเป็นบรรทัด
    return text  # คืนค่าข้อความเป็น list ของบรรทัด

def correct_text(lines):
    """ ตรวจคำผิด, ดึงเฉพาะคำผิด และให้ผู้ใช้เลือกตัวเลือกที่ถูกต้อง """
    corrected_lines = []
    error_list = []  # เก็บรายการคำผิด (บรรทัดที่, คำผิด, ตัวเลือกทั้งหมด)

    for line_no, line in enumerate(lines, start=1):
        matches = tool.check(line)  # ตรวจคำผิดทีละบรรทัด
        corrected_line = line

        for match in matches:
            if match.replacements:  # ตรวจเฉพาะคำผิดที่มีคำแนะนำ
                error_word = line[match.offset : match.offset + match.errorLength]  # ดึงคำผิดจากตำแหน่งจริง
                corrections = match.replacements  # คำที่ถูกต้องทั้งหมด
                error_list.append((line_no, error_word, corrections))  # บรรทัดที่, คำผิด, ตัวเลือกทั้งหมด

        corrected_lines.append(corrected_line)

    return corrected_lines, error_list  # คืนค่าทั้งข้อความที่ถูกแก้ไข และรายการคำผิด

def translate_text(text, target_lang="th"):
    """ แปลข้อความไปยังภาษาที่ต้องการ """
    translated = translator.translate("\n".join(text), dest=target_lang)
    return translated.text.split("\n")

def save_text_to_pdf(text, output_path):
    """ บันทึกข้อความลง PDF """
    doc = fitz.open()
    page = doc.new_page()
    y = 100  # เริ่มพิมพ์ที่ตำแหน่ง Y
    for line in text:
        page.insert_text((50, y), line)
        y += 20  # เพิ่มระยะห่างระหว่างบรรทัด
    doc.save(output_path)
    doc.close()
