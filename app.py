import streamlit as st
import google.generativeai as genai
import gspread
from PIL import Image
import json

# --- ตั้งค่าหน้าจอ ---
st.set_page_config(page_title="Pig Scan AI Pro", layout="centered")

SHEET_CONFIG = {
    "N1": "1BYH07Wdv-Us2Ke45U7D2zk8_ZXDTMEDJQlLylOhz5ow",
    "Pre-Pik": "1AnkQmZwn8GiOKaXeVYseqhDtogRYPHmD9_JPhQUMrV0"
}

# --- ฟังก์ชันเชื่อมต่อ Google Sheets (แบบใหม่) ---
def get_sheet_client():
    creds_dict = st.secrets["gcp_service_account"]
    return gspread.service_account_from_dict(creds_dict)

# --- ส่วน UI ---
st.title("🐷 Pig Scan Data Automation")
target = st.selectbox("เลือกไฟล์ที่ต้องการบันทึก:", list(SHEET_CONFIG.keys()))
uploaded_file = st.file_uploader("อัปโหลดรูปภาพ:", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="รูปที่อัปโหลด", use_container_width=True)

    if st.button("🚀 ประมวลผลและบันทึกข้อมูล"):
        with st.spinner("AI กำลังวิเคราะห์..."):
            try:
                # ตั้งค่า AI
                genai.configure(api_key=st.secrets["api_keys"]["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = """
                วิเคราะห์ใบส่งสินค้าในรูปภาพนี้ ดึงรายการสินค้าออกมาเป็น JSON เท่านั้น
                โครงสร้าง: {"items": [{"date": "วันที่", "product": "ชื่อสินค้า", "weight": "น้ำหนัก", "qty": "จำนวน"}]}
                """
                
                response = model.generate_content([prompt, image])
                
                # ทำความสะอาดและแปลงเป็น JSON
                json_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(json_text)
                
                # บันทึกลง Sheet
                client = get_sheet_client()
                sheet = client.open_by_key(SHEET_CONFIG[target]).sheet1
                
                for item in data['items']:
                    sheet.append_row([item['date'], item['product'], item['weight'], item['qty']])
                
                st.success("✅ บันทึกข้อมูลสำเร็จ!")
                st.json(data)
                        
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
