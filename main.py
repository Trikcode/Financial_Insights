import streamlit as st
import pyrebase
from user_interface import render_user_interface
from dotenv import load_dotenv
import os

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

if 'user_authenticated' not in st.session_state:
    st.session_state['user_authenticated'] = False

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
            st.session_state['user_authenticated'] = True
            st.rerun()
        except Exception as e:
            st.error('Login failed. Please check your credentials.')

def register():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    new_email = st.text_input('New Email')
    new_password = st.text_input('New Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    signup = st.button('Sign Up')

    if signup:
        if new_password == confirm_password:
            try:
                auth.create_user_with_email_and_password(new_email, new_password)
                st.success('Successfully registered!')
                st.session_state['user_authenticated'] = True
                st.rerun()
            except Exception as e:
                st.error('Registration failed. Please try again.')
        else:
            st.warning('Passwords do not match.')

def logout():
    st.session_state['user_authenticated'] = False

def view_insights():
    # Add functionality to view insights from the database here
    st.write("Viewing user's previous insights")

def render_authentication():
    st.title('Login/Register')
    authenticate()
    register()

if st.session_state.get('user_authenticated'):
    col1, col2 = st.columns([1, 1])
    with col1:
        view_insights()
    with col2:
        logout()
    st.write("Welcome to Financial Clarity Hub! Enter your information below to generate personalized financial insights.")
    render_user_interface()
else:
    render_authentication()
