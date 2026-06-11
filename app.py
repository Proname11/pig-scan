import streamlit as st
import pandas as pd
from fill_excel import get_google_sheet_data

st.title("Pig Scan Data Processor")

# ดึงข้อมูลมาแสดงเป็นตัวอย่าง
if st.button("Load Template"):
    data = get_google_sheet_data("ชื่อไฟล์ในGoogleSheetsของคุณ")
    df = pd.DataFrame(data)
    st.write("ข้อมูลจาก Google Sheets:", df)

# ส่วนของการอัปโหลดรูปและรัน AI (ใส่โค้ดประมวลผลของคุณที่นี่)
uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png'])
if uploaded_file:
    st.write("Processing image...")
    # ใส่ logic การเรียกใช้ OpenAI หรือประมวลผลภาพที่นี่
