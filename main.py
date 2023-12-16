import streamlit as st
import pyrebase

from dotenv import load_dotenv
import os
from user_interface import render_user_interface

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

st.set_page_config(page_title='Financial Clarity Hub', page_icon=':moneybag:', layout='wide')

st.title('Financial Clarity Hub: Financial Dashboard')

# Function to handle authentication
def authenticate():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    login = st.button('Login')

    if login:
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success('Successfully logged in!')
            st.experimental_set_query_params(logged_in=True)
            st.rerun()
        except Exception as e:
            st.error('Login failed. Please check your credentials.')

    register = st.checkbox('Register')

    if register:
        new_email = st.text_input('New Email')
        new_password = st.text_input('New Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')
        signup = st.button('Sign Up')

        if signup:
            if new_password == confirm_password:
                try:
                    auth.create_user_with_email_and_password(new_email, new_password)
                    st.success('Successfully registered!')
                    # Proceed to login or redirect to login form
                except Exception as e:
                    st.error('Registration failed. Please try again.')
            else:
                st.warning('Passwords do not match.')

def render_authentication():
    st.title('Login/Register')
    authenticate()


# Get the query parameters
query_params = st.experimental_get_query_params()
logged_in = query_params.get('logged_in')

if logged_in:
    st.write("Welcome to Financial Clarity Hub! Enter your information below to generate personalized financial insights.")
    render_user_interface()
else:
    render_authentication()
