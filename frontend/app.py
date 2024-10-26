import streamlit as st
import os
from dotenv import load_dotenv
import logging

# Import pages from the new directory structure
from pages import signup, login, home  # Import home page

# Load environment variables from .env file
load_dotenv()

# Get the backend URL from the environment variable
backend_url = os.environ.get('Backend_url')

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="nosu",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.yourapp.com/help',
        'Report a bug': "https://www.yourapp.com/bug",
        'About': "# This is the nosu app. An AI-powered platform for evaluating business ideas!",
    }
)

# Initialize session state for page selection if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'signup'  # Default to signup

def set_style():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #6A0DAD;  /* Added # for hex color */
            font-family: Open Sans, sans-serif;
            text-align: center;
            color: white;  /* Optional: Set text color to white */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    set_style()

    # Sidebar navigation
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Initialize logged_in state

    # Render sidebar based on login status
    with st.sidebar:
        if st.session_state.logged_in:
            st.button("Home", on_click=lambda: set_page("home"))
            st.button("Logout", on_click=lambda: logout())
        else:
            st.button("Signup", on_click=lambda: set_page("signup"))
            st.button("Login", on_click=lambda: set_page("login"))

    # Render pages based on session state
    if st.session_state.page == "signup":
        signup.show_signup_page()  # Render the signup page
    elif st.session_state.page == "login":
        login.show_login_page()  # Render the login page
    elif st.session_state.page == "home":
        home.show_home_page()  # Render the home page after login

def set_page(page_name):
    st.session_state.page = page_name  # Change the current page
     # Refresh to show the selected page

def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.page = 'login'  # Redirect to login page
    #st.rerun()  # Refresh to show the login page



# Set up logging to file
# Determine if the app is in production or development  Development: Set FLASK_ENV=development
#Production: Set FLASK_ENV=production
if os.getenv("FLASK_ENV") == "production":
    # Disable logging in production
    logging.basicConfig(level=logging.WARNING)  # Set to WARNING or higher to ignore DEBUG and INFO
else:
    # Enable detailed logging in development
    logging.basicConfig(
        filename='debug.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Example log messages
logging.debug("This will be logged in development but not in production.")
logging.info("Informational message.")



if __name__ == "__main__":
    main()