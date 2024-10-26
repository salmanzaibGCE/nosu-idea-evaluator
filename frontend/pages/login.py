import streamlit as st 
import requests
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend URL from environment variable
backend_url = os.getenv("Backend_url")
login_url = f"{backend_url}/login"  # Replace with your Flask login URL

def show_login_page():
    # Custom CSS to style the page
    st.markdown(
        f"""
        <style>
        body {{
            background-color: #2C2F33; /* Purple background */
        }}
        .stApp {{
            font-family: Open Sans, sans-serif;
            color: #FFFFFF; /* White text */
            text-align: center;
        }}
        .stTitle {{
            font-weight: bold;
            font-size: 48px; /* Larger title font */
            margin-bottom: 10px;
        }}
        .stSubtitle {{
            font-size: 24px; /* Subtitle font size */
            margin-bottom: 50px;
        }}
        .stTextInput {{
            border-radius: 5px;
            padding: 10px;
            width: 50%; /* Reduced width to match design */
            margin: 20px auto;
            border: 1px solid #CCC;
            display: block; /* Center align input */
        }}
        .stButton {{
            background-color: #7289DA; /* Login button color */
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .stButton:hover {{
            background-color: #5B6EBD; /* Slightly darker on hover */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title and subtitle
    st.markdown("<h1 class='stTitle'>nosu</h1>", unsafe_allow_html=True)
    st.markdown("<p class='stSubtitle'>your AI-powered idea evaluator</p>", unsafe_allow_html=True)

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        # Login button
        submit_button = st.form_submit_button("Login")

        # Form validation and backend login call
        if submit_button:
            if not email or not password:
                st.error("Email and password cannot be empty.")
            else:
                with st.spinner("Logging in..."):
                    # Send data as JSON
                    response = requests.post(login_url, json={"email": email, "password": password})

                    if response.status_code == 200:
                        st.success(f"Welcome back, {email}!")
                        st.session_state.logged_in = True  # Set logged-in state
                        st.session_state.user_email = email  # Store user email
                        # Store the session cookie here
                        logging.info("Response Cookies:", response.cookies)
                        session_cookie = response.cookies.get('session')  # Replace with actual cookie name
                        if session_cookie:
                            st.session_state.session_cookie = session_cookie
                        st.session_state.page = 'home'  # Change to app page after successful login
                        st.rerun()  # Refresh to show the app page
                    else:
                        error_message = response.json().get("error", "Invalid email or password.")
                        st.error(error_message)

    # Link to signup page for new users
    st.markdown(
        """
        Don't have an account? <a class="link" onclick="goToPage('signup')">Sign up here</a>
        """,
        unsafe_allow_html=True
    )

