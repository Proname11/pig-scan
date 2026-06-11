import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials


def get_google_sheet_data(spreadsheet_id):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    # ต้องใช้ open_by_key เท่านั้น!
    sheet = client.open_by_key(spreadsheet_id).sheet1
    return sheet.get_all_values()
