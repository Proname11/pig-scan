import streamlit as st
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
import json

# --- 1. การตั้งค่าเริ่มต้น (Configuration) ---
st.set_page_config(page_title="Pig Scan AI Pro", layout="centered")

# กำหนด ID ของ Google Sheets (ตรวจสอบให้ตรงกับไฟล์ของคุณ)
SHEET_CONFIG = {
    "N1": "1BYH07Wdv-Us2Ke45U7D2zk8_ZXDTMEDJQlLylOhz5ow",
    "Pre-Pik": "1AnkQmZwn8GiOKaXeVYseqhDtogRYPHmD9_JPhQUMrV0"
}

# --- 2. ฟังก์ชันเชื่อมต่อ Google Sheets ---
def get_sheet_client():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"เชื่อมต่อ Google Sheets ไม่สำเร็จ: {e}")
        return None

# --- 3. ส่วนหลักของแอป ---
st.title("🐷 Pig Scan Data Automation")
st.subheader("ระบบสแกนข้อมูลด้วย AI และบันทึกลง Google Sheets")

# เลือกไฟล์ปลายทาง
target = st.selectbox("เลือกไฟล์ที่ต้องการบันทึกข้อมูล:", list(SHEET_CONFIG.keys()))

# อัปโหลดรูปภาพ
uploaded_file = st.file_uploader("อัปโหลดรูปภาพข้อมูล (JPG/PNG):", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="รูปภาพที่อัปโหลด", use_container_width=True)

    if st.button("🚀 ประมวลผลและบันทึกข้อมูล"):
        with st.spinner("AI กำลังวิเคราะห์ข้อมูล..."):
            try:
                # --- ส่วน AI (Gemini) ---
                api_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]
                genai.configure(api_key=api_key)
                
                # ใช้ชื่อรุ่นที่แสดงผลใน Debug ของคุณ
                model = genai.GenerativeModel('gemini-2.5-flash') 
                
                # Prompt สำหรับสั่ง AI (ปรับเปลี่ยนตามหัวตารางของคุณได้)
                prompt = """
                วิเคราะห์รูปภาพนี้แล้วสกัดข้อมูลออกมาเพื่อบันทึกลงตาราง
                ตอบกลับเป็นรูปแบบ Python List เท่านั้น (เช่น ['data1', 'data2', 'data3'])
                ห้ามอธิบายเพิ่ม ห้ามมีข้อความอื่นนอกจาก List ข้อมูล
                """
                
                response = model.generate_content([prompt, image])
                
                # แปลงคำตอบจาก AI เป็น List
                try:
                    # ทำความสะอาดข้อความจาก AI (เอาพวก ```python ออกถ้ามี)
                    raw_text = response.text.strip().replace("```python", "").replace("```", "")
                    data_list = eval(raw_text) 
                    
                    if isinstance(data_list, list):
                        # --- ส่วนบันทึกข้อมูลลง Sheets ---
                        client = get_sheet_client()
                        if client:
                            sheet_id = SHEET_CONFIG[target]
                            sheet = client.open_by_key(sheet_id).sheet1
                            sheet.append_row(data_list)
                            
                            st.success(f"✅ บันทึกข้อมูลลงไฟล์ {target} สำเร็จ!")
                            st.write("ข้อมูลที่บันทึก:", data_list)
                    else:
                        st.error("AI ตอบกลับมาในรูปแบบที่ไม่ใช่ List")
                        
                except Exception as eval_err:
                    st.error("AI อ่านข้อมูลไม่ได้ หรือรูปแบบข้อมูลผิด")
                    st.write("สิ่งที่ AI ตอบมา:", response.text)

            except Exception as ai_err:
                st.error(f"เกิดข้อผิดพลาดที่ระบบ AI: {ai_err}")

# --- 4. ส่วนตรวจสอบสิทธิ์ (Footer) ---
st.divider()
st.caption("พัฒนาด้วย Streamlit + Gemini AI 1.5/2.5")
