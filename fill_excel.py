import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def get_client():
    # กำหนดสิทธิ์
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def get_sheet_data(spreadsheet_id):
    # เชื่อมต่อและดึงข้อมูล
    client = get_client()
    sheet = client.open_by_key(spreadsheet_id).sheet1
    return sheet.get_all_values()
