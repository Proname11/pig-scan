import google.generativeai as genai
import os

# ใส่ API Key ตรงๆ (เพื่อทดสอบว่าที่พังเป็นเพราะ Secrets หรือเพราะ API Key)
API_KEY = "ใส่_API_KEY_ของคุณตรงนี้"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
try:
    response = model.generate_content("Hello, are you working?")
    print("AI เชื่อมต่อสำเร็จ! คำตอบคือ:", response.text)
except Exception as e:
    print("AI เชื่อมต่อไม่สำเร็จ:", e)
