import streamlit as st
import pyrebase

# Firebase configuration (keep this code as is)

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
            # Proceed to user dashboard/profile
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
