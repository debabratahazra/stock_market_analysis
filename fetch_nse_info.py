import streamlit as st
import time
from datetime import date, timedelta
from update_nse_list import download_file
import pandas as pd
from read_extract_df import read_extract_company


def get_nse_data():
    # Create a spinner
    with st.spinner("Wait for it...", show_time=True):
         # Update NSE List from API
        file_url = "https://raw.githubusercontent.com/imanojkumar/NSE-India-All-Stocks-Tickers-Data/refs/heads/main/Ticker_List_NSE_India.csv"
        file_name = "resources/nse_lists.csv"
        download_file(file_url, file_name)
        
        # Create a dropdown for company selection
        df = read_extract_company(file_name)
        return df
        