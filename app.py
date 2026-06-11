import streamlit as st
import google.generativeai as genai
from fill_excel import get_client, save_to_sheet # ตรวจสอบการ import ให้ตรง

st.title("Debug Mode")

if st.button("Start Debug"):
    try:
        st.write("1. กำลังโหลด Secrets...")
        # ลองดึงค่าออกมาดูว่ามีไหม
        api_key = st.secrets["api_keys"]["GOOGLE_API_KEY"]
        st.write("   Secrets โหลดสำเร็จ")

        st.write("2. กำลังเชื่อมต่อ AI...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        st.write("   เชื่อมต่อ AI สำเร็จ")

        st.write("3. กำลังทดสอบส่งข้อความหา AI...")
        response = model.generate_content("Hello")
        st.write("   AI ตอบกลับมาว่า:", response.text)

        st.success("ทุกอย่างปกติดี!")
    except Exception as e:
        st.error(f"ค้างที่จุดนี้: {e}")
