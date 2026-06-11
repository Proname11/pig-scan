import gspread
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

def get_client():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

def save_to_sheet(spreadsheet_id, data_list):
    client = get_client()
    sheet = client.open_by_key(spreadsheet_id).sheet1
    sheet.append_row(data_list)
