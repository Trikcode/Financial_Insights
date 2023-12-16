import streamlit as st
from user_interface import render_user_interface
from auth import render_authentication

st.set_page_config(page_title='Financial Clarity Hub', page_icon=':moneybag:', layout='wide')

st.title('Financial Clarity Hub: Financial Dashboard')

# Check if user is authenticated
authenticated = False  # Initially, assume user is not authenticated

# Render authentication form or user interface based on authentication status
if not authenticated:
    render_authentication()  # Render authentication form
else:
    render_user_interface()  # Render user interface
