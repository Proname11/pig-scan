import streamlit as st
import google.generativeai as genai
from PIL import Image
from fill_excel import save_to_sheet
import json

# ตั้งค่า AI
genai.configure(api_key=st.secrets["api_keys"]["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# ตั้งค่า ID ไฟล์
SHEET_IDS = {
    "N1": "1BYH07Wdv-Us2Ke45U7D2zk8_ZXDTMEDJQlLylOhz5ow",
    "Pre-Pik": "1AnkQmZwn8GiOKaXeVYseqhDtogRYPHmD9_JPhQUMrV0"
}

st.title("Pig Scan Data Processor")

# 1. เลือกไฟล์ที่จะบันทึก
target_sheet = st.selectbox("เลือกไฟล์ปลายทาง:", list(SHEET_IDS.keys()))

# 2. อัปโหลดไฟล์
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])

if uploaded_file and st.button("Process & Save"):
    with st.spinner("AI กำลังอ่านข้อมูล..."):
        image = Image.open(uploaded_file)
        
        # 3. ให้ AI อ่านข้อมูล (ปรับ Prompt ตามหัวตารางของคุณ)
        prompt = "อ่านข้อมูลจากภาพนี้ แล้วตอบกลับมาเป็น List ของข้อมูลตามลำดับหัวตาราง (ห้ามเขียนคำอธิบายเพิ่ม ให้ตอบแค่ข้อมูลเป็น List เช่น ['data1', 'data2'])"
        response = model.generate_content([prompt, image])
        
        try:
            # แปลงข้อความที่ AI ตอบมาเป็น list
            data_to_save = eval(response.text) 
            
            # 4. บันทึกลง Sheet
            save_to_sheet(SHEET_IDS[target_sheet], data_to_save)
            st.success(f"บันทึกข้อมูลเรียบร้อยแล้วไปที่ {target_sheet}!")
            st.write("ข้อมูลที่อ่านได้:", data_to_save)
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
            st.write("สิ่งที่ AI ตอบกลับมา:", response.text)
