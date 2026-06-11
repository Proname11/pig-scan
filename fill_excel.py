import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet_data(sheet_name):
    # เชื่อมต่อด้วย credentials จาก Streamlit Secrets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).sheet1
    return sheet.get_all_values()
