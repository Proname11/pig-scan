import streamlit as st
from fill_excel import get_sheet_data

# กำหนด ID ของไฟล์ (ที่ก๊อปปี้มาจาก URL)
ID_N1 = "1BYH07Wdv-Us2Ke45U7D2zk8_ZXDTMEDJQlLylOhz5ow"
ID_PRE_PIK = "1AnkQmZwn8GiOKaXeVYseqhDtogRYPHmD9_JPhQUMrV0"

st.title("Pig Scan Data Processor")

# ตัวอย่างการใช้งานดึงข้อมูล
if st.button("Load Data"):
    try:
        data_n1 = get_sheet_data(ID_N1)
        data_pre_pik = get_sheet_data(ID_PRE_PIK)
        
        st.success("โหลดข้อมูลสำเร็จ!")
        st.write("ข้อมูลจาก N1:", data_n1)
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
        st.info("ตรวจสอบให้แน่ใจว่าได้แชร์ไฟล์ให้ Email ของบอทแล้ว (ในขั้นตอน Share)")
