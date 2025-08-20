import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import matplotlib.pyplot as plt
import datetime
from datetime import date, timedelta
import yfinance as yf
import plotly.express as px

def make_ui(df):
    
    # Set the page layout to "wide" mode
    st.set_page_config(layout="wide")
    
    # Set the title of the Streamlit app
    st.title("Stock Market Analysis App")
    st.write("")
    st.write("")
    
    colX, colY = st.columns([0.75, 0.25])
    
    with colX:        
    
        # Select the Stock Market Company
        st.subheader("Select Company Name for Stock Analysis")
        
        # Create a dictionary for lookup
        company_symbol_dict = dict(zip(df["NAME OF COMPANY"], df["YahooEquiv"]))
        companies = []

        # Create a dropdown list
        selected_company = st.selectbox("Select a company", df["NAME OF COMPANY"])

        # Get the corresponding symbol
        if selected_company:
            symbol = company_symbol_dict[selected_company]
            # st.write(f"The symbol for {selected_company} is: {symbol}")
        
        
        # Calculate the first day of the current month
        today = date.today()

        # Calculate the same date of the previous month
        if today.month == 1:
            first_date = date(today.year - 1, 12, today.day)
        else:
            first_date = date(today.year, today.month - 1, today.day)

        # Ensure the day exists in the previous month (e.g., February 30 doesn't exist)
        if first_date.day > 28:
            last_day_of_prev_month = (date(today.year, today.month, 1) - timedelta(days=1)).day
            first_date = date(today.year, today.month - 1, min(first_date.day, last_day_of_prev_month))
            
        # Initialize session state
        if 'selected_companies' not in st.session_state:
            st.session_state.selected_companies = []

        
        # Create a form for date range selection
        with st.form("date_range_form"):
            # Create a sub-heading
            st.subheader("Select Date Range for Stock Analysis")
            col1, col2 = st.columns(2)
            start_date = col1.date_input("Start Date", value=first_date)
            end_date = col2.date_input("End Date", value=today, min_value=start_date, max_value=today)
            
            st.write("")
            submitted = st.form_submit_button("Submit")
            
        if submitted:
            
            formated_sdate = start_date.strftime("%d-%m-%Y")
            formated_sdate = end_date.strftime("%d-%m-%Y")
            st.write(f"Selected date range: {formated_sdate} to {formated_sdate}")
        
        
            # Get data from yfinance
            if symbol:
                # Add selected company to session state
                if selected_company not in st.session_state.selected_companies:
                    st.session_state.selected_companies.append(selected_company)
                
                
            
                # Create a spinner
                with st.spinner("Fetching data...", show_time=True):
                    # Fetch historical data for the selected company
                    ticker_data = yf.Ticker(symbol)
                    start_date = datetime.date(start_date.year, start_date.month, start_date.day)
                    end_date = datetime.date(end_date.year, end_date.month, end_date.day)
                    ticker_df= ticker_data.history(start= start_date,end=end_date)
                    st.dataframe(ticker_df)
                    
                    # Plot the closing price
                    st.subheader("Closing Price")

                    fig = px.line(ticker_df, x=ticker_df.index, y='Close', title=f"{selected_company} Closing Price", markers=True)
                    fig.update_layout(xaxis_title="Date", yaxis_title="Price (Rs.)")
                    fig.update_yaxes(range=[0, max(ticker_df['Close'])*1.1])
                    st.plotly_chart(fig, use_container_width=True)


    with colY:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # Create a selectbox for selected companies
        selected_company_history = st.selectbox("Select a company from history", st.session_state.selected_companies + companies)
                
        # If a company is selected from history, auto select it in the original selectbox
        if selected_company_history in st.session_state.selected_companies:
            selected_company = selected_company_history