import streamlit as st
import google.generativeai as genai

st.title("Check Model Name")

try:
    genai.configure(api_key=st.secrets["api_keys"]["GOOGLE_API_KEY"])
    st.write("รายชื่อโมเดลที่ API Key นี้ใช้งานได้:")
    
    # ดึงรายชื่อโมเดลที่รองรับ generateContent
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.write(f"ชื่อที่ถูกต้องคือ: **{m.name}**")
            
except Exception as e:
    st.error(f"Error: {e}")
