import streamlit as st
import pyrebase
from user_interface import render_user_interface
from firebase_config import firebaseConfig


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
    st.success('Successfully logged out!')
    st.rerun()
    

def view_insights():
    st.write("Viewing user's previous insights")

def render_authentication():
    st.title('Login/Register')
    authenticate()
    if st.checkbox('Show Register Form'):
        register()

if st.session_state.get('user_authenticated'):
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('View Previous Insights'):
            view_insights()  
    with col2:
        if st.button('Logout'):
            logout()
    st.write("Welcome to Financial Clarity Hub! Enter your information below to generate personalized financial insights.")
    render_user_interface()
else:
    render_authentication()
