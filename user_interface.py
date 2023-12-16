import streamlit as st
import pandas as pd
import plotly.express as px
from data_fetch import get_stock_price, get_stock_info
from predictions import render_predictions 
from dotenv import load_dotenv
import os
import pyrebase

load_dotenv()

# Firebase configuration using environment variables
firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

def render_user_interface():
    insights = None
    recommendation = None
    user_data = None
    user_df = None
    export_df = None
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()

    with st.form(key='user_input_form'):
        st.header('User Information')

        name = st.text_input('Full Name')
        age = st.number_input('Age', min_value=18, max_value=120, value=25)
        gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
        location = st.text_input('Location')

        st.header('Financial Information')

        currency_options = ['USD', 'EUR', 'GBP', 'JPY', 'INR']  # You can add more currencies as needed
        currency = st.selectbox('Select Currency', currency_options, index=0)
        
        monthly_income = st.number_input(f'Monthly Income ({currency})', value=0)
        expenses = st.number_input(f'Monthly Expenses ({currency})', value=0)
        assets = st.number_input(f'Total Assets ({currency})', value=0)
        liabilities = st.number_input(f'Total Liabilities ({currency})', value=0)

        st.header('Financial Goals')

        short_term_goal = st.text_input('Short-term Goal')
        mid_term_goal = st.text_input('Mid-term Goal')
        long_term_goal = st.text_input('Long-term Goal')

        st.header('Risk Tolerance')

        risk_tolerance = st.slider('Risk Tolerance', min_value=1, max_value=10, value=5)

        st.header('Stock Analysis')

        stock_symbol = st.text_input('Enter Stock Symbol (e.g., AAPL)')
        submitted = st.form_submit_button('Generate Insights')

        # Insights generation
        if submitted:
            insights = "Placeholder for insights based on user input"
            st.subheader('Insights')
            st.write(insights)

            recommendation = "A recommendation based on risk tolerance, financial goals, and user information."
            st.subheader('Recommendation')
            st.write(recommendation)

            if stock_symbol:
                st.subheader('Current Stock Price')
                stock_price = get_stock_price(stock_symbol)
                if stock_price:
                    st.write(f"The current price of {stock_symbol} is ${stock_price}")
                else:
                    st.write("Error fetching stock price. Please try again.")
            else:
                st.warning("Please enter a stock symbol.")

            if stock_symbol:
                st.subheader('Stock Information')
                stock_info = get_stock_info(stock_symbol)
                if stock_info:
                    st.write(f"Export stock information for {stock_symbol}: by clicking the button below.")
                else:
                    st.write("Error fetching stock information.")

            render_predictions(stock_symbol)

            user_data = {
                'Full Name': name,
                'Age': age,
                'Gender': gender,
                'Location': location,
                'Currency': currency,
                'Monthly Income': monthly_income,
                'Monthly Expenses': expenses,
                'Total Assets': assets,
                'Total Liabilities': liabilities,
                'Short-term Goal': short_term_goal,
                'Mid-term Goal': mid_term_goal,
                'Long-term Goal': long_term_goal,
                'Risk Tolerance': risk_tolerance,
            }
            # After collecting user_data
            if user_data is not None:
                db.child("user_data").push(user_data)

            user_df = pd.DataFrame.from_dict(user_data, orient='index', columns=['Value'])

            st.subheader('User Financial Data Visualization')
            fig = px.bar(user_df, x=user_df.index, y='Value', labels={'x': 'Category', 'y': 'Value'}, title='User Financial Data')
            st.plotly_chart(fig)

    if user_df is not None:
        export_data = {
            'Insights': insights,
            'Recommendation': recommendation,
            'User_Financial_Data': user_data, 
            'Stock_Information': stock_info  
        }
        export_df = pd.DataFrame.from_dict(export_data, orient='index', columns=['Value'])

    if export_df is not None and not export_df.empty:
        csv_export = export_df.to_csv().encode()
        st.download_button(
            label="Export Insights and Stock Information",
            data=csv_export,
            file_name='financial_insights.csv',
            mime='text/csv'
        )
