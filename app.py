import streamlit as st
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
import json

# --- 1. การตั้งค่าเริ่มต้น ---
st.set_page_config(page_title="Pig Scan AI Pro", layout="centered")

SHEET_CONFIG = {
    "N1": "1BYH07Wdv-Us2Ke45U7D2zk8_ZXDTMEDJQlLylOhz5ow",
    "Pre-Pik": "1AnkQmZwn8GiOKaXeVYseqhDtogRYPHmD9_JPhQUMrV0"
}

# --- 2. ฟังก์ชันเชื่อมต่อ Google Sheets ---
def get_sheet_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://spreadsheets.google.com/auth/drive']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# --- 3. ส่วนหลักของแอป ---
st.title("🐷 Pig Scan Data Automation")
target = st.selectbox("เลือกไฟล์ที่ต้องการบันทึกข้อมูล:", list(SHEET_CONFIG.keys()))
uploaded_file = st.file_uploader("อัปโหลดรูปภาพข้อมูล (JPG/PNG):", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="รูปภาพที่อัปโหลด", use_container_width=True)

    if st.button("🚀 ประมวลผลและบันทึกข้อมูล"):
        with st.spinner("AI กำลังวิเคราะห์ข้อมูล..."):
            try:
                # ตั้งค่า AI
                api_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash') 
                
                prompt = """
                วิเคราะห์ใบส่งสินค้าในรูปภาพนี้
                สกัดข้อมูลรายการสินค้าออกมาเป็นรูปแบบ JSON เท่านั้น โดยมีโครงสร้างดังนี้:
                {
                    "items": [
                        {"date": "วันที่", "product": "ชื่อสินค้า", "weight": "น้ำหนัก", "qty": "จำนวน"}
                    ]
                }
                ห้ามใส่ข้อความอื่นนอกจาก JSON นี้
                """
                
                response = model.generate_content([prompt, image])
                
                # แปลงผลลัพธ์
                json_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(json_text)
                
                # บันทึกลง Sheet
                client = get_sheet_client()
                sheet_id = SHEET_CONFIG[target]
                sheet = client.open_by_key(sheet_id).sheet1
                
                count = 0
                for item in data['items']:
                    row = [item['date'], item['product'], item['weight'], item['qty']]
                    sheet.append_row(row)
                    count += 1
                
                st.success(f"✅ บันทึกข้อมูลสำเร็จ {count} รายการ!")
                st.write(data)
                        
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
