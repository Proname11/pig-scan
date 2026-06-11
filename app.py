import streamlit as st
import google.generativeai as genai
from fill_excel import get_client, save_to_sheet 

st.title("Debug Mode")

if st.button("Start Debug"):
    try:
        st.write("1. กำลังโหลด Secrets...")
        api_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]
        st.write("   Secrets โหลดสำเร็จ")

        st.write("2. กำลังเชื่อมต่อ AI...")
        genai.configure(api_key=api_key)
        
        # --- จุดแก้ไข: ต้องประกาศตัวแปร model ที่นี่ก่อนใช้งาน ---
        model_name = "gemini-1.5-flash" 
        model = genai.GenerativeModel(model_name) 
        st.write(f"   เชื่อมต่อ AI สำเร็จ (ใช้รุ่น: {model_name})")

        st.write("3. กำลังทดสอบส่งข้อความหา AI...")
        # ตอนนี้เรียกใช้ model ได้แล้วเพราะประกาศไว้บรรทัดบน
        response = model.generate_content("Hello, just confirm if you are working.")
        st.write("   AI ตอบกลับมาว่า:", response.text)

        st.success("ทุกอย่างปกติดี!")
    except Exception as e:
        st.error(f"ค้างที่จุดนี้: {e}")
