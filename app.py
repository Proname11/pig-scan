import json # อย่าลืม import json ไว้บนสุด

# ... (โค้ดก่อนหน้านี้เหมือนเดิม)

    if st.button("🚀 ประมวลผลและบันทึกข้อมูล"):
        with st.spinner("AI กำลังวิเคราะห์ข้อมูล..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # ปรับ Prompt ให้บังคับตอบเป็น JSON เท่านั้น
                prompt = """
                วิเคราะห์ใบส่งสินค้าในรูปภาพนี้
                สกัดข้อมูลเฉพาะรายการสินค้าออกมาเป็นรูปแบบ JSON เท่านั้น โดยมีโครงสร้างดังนี้:
                {
                    "items": [
                        {"date": "วันที่", "product": "ชื่อสินค้า", "weight": "น้ำหนัก", "qty": "จำนวน"}
                    ]
                }
                ห้ามใส่ข้อความอื่นนอกจาก JSON นี้
                """
                
                response = model.generate_content([prompt, image])
                
                # --- ส่วนสำคัญ: แปลงเป็น JSON ---
                # ตัดส่วนที่เป็น Markdown ออก (ถ้ามี)
                json_text = response.text.replace("```json", "").replace("```", "").strip()
                data = json.loads(json_text)
                
                # บันทึกข้อมูลทีละบรรทัด (Loop items)
                client = get_sheet_client()
                sheet_id = SHEET_CONFIG[target]
                sheet = client.open_by_key(sheet_id).sheet1
                
                count = 0
                for item in data['items']:
                    row = [item['date'], item['product'], item['weight'], item['qty']]
                    sheet.append_row(row)
                    count += 1
                
                st.success(f"✅ บันทึกข้อมูลสำเร็จ {count} รายการ!")
                st.json(data) # โชว์ให้ดูว่า AI อ่านอะไรมา
                        
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการประมวลผล: {e}")
                st.write("สิ่งที่ AI ตอบมา:", response.text)
