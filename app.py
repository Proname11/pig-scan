import streamlit as st
from google import genai
import gspread
from PIL import Image
import json

# --- ตั้งค่าหน้าจอ ---
st.set_page_config(page_title="Pig Scan AI Pro", layout="centered")

SHEET_CONFIG = {
    "N1": "1BYH07Wdv-Us2Ke45U7D2zk8_ZXDTMEDJQlLylOhz5ow",
    "Pre-Pik": "1AnkQmZwn8GiOKaXeVYseqhDtogRYPHmD9_JPhQUMrV0"
}

def get_sheet_client():
    creds_dict = st.secrets["gcp_service_account"]
    return gspread.service_account_from_dict(creds_dict)

# --- ส่วน UI ---
st.title("🐷 Pig Scan Data Automation")
target = st.selectbox("เลือกไฟล์ที่ต้องการบันทึก:", list(SHEET_CONFIG.keys()))
uploaded_file = st.file_uploader("อัปโหลดรูปภาพ:", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    # แก้ไขตรงนี้: เปลี่ยน use_container_width เป็น width='stretch'
    st.image(image, caption="รูปที่อัปโหลด", width='stretch')

    if st.button("🚀 ประมวลผลและบันทึกข้อมูล"):
        with st.spinner("AI กำลังวิเคราะห์..."):
            try:
                # แก้ไขตรงนี้: ใช้ Client แบบใหม่
                client = genai.Client(api_key=st.secrets["api_keys"]["GOOGLE_API_KEY"])
                
                prompt = """
                วิเคราะห์ใบส่งสินค้าในรูปภาพนี้ ดึงรายการสินค้าออกมาเป็น JSON เท่านั้น
                โครงสร้าง: {"items": [{"date": "วันที่", "product": "ชื่อสินค้า", "weight": "น้ำหนัก", "qty": "จำนวน"}]}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, image]
                )
                
                json_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(json_text)
                
                client_gs = get_sheet_client()
                sheet = client_gs.open_by_key(SHEET_CONFIG[target]).sheet1
                
                for item in data['items']:
                    sheet.append_row([item['date'], item['product'], item['weight'], item['qty']])
                
                st.success("✅ บันทึกข้อมูลสำเร็จ!")
                st.json(data)
                        
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
