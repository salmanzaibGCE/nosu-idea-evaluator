import streamlit as st
import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend URL from environment variable
backend_url = os.environ.get('Backend_url')
signup_url = f"{backend_url}/signup"

def show_signup_page():
    # Custom CSS to match Figma design
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
            background-color: #7289DA; /* Signup button color */
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

    # Header
    st.markdown("<h1 class='stTitle'>nosu</h1>", unsafe_allow_html=True)
    st.markdown("<p class='stSubtitle'>your AI-powered idea evaluator</p>", unsafe_allow_html=True)

    # Signup form
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Enter your username", key="username")
        email = st.text_input("Email", placeholder="Enter your email", key="email")
        password = st.text_input("Password", placeholder="Enter your password", type="password", key="password")
        confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password", key="confirm_password")

        # Submit button
        submit_button = st.form_submit_button("Sign Up")

        # Form validation and backend integration
        if submit_button:
            if not username or not email or not password or not confirm_password:
                st.error("All fields are required.") 
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    with st.spinner("Creating account..."):
                        result = signup_user(username, email, password)
                        if result is True:
                            st.success(f"Account created successfully! Welcome, {username}.")
                            st.session_state.page = 'login'  # Change to login page after successful signup
                            st.rerun()  # Refresh to show the login page
                        else:
                            st.error(f"Signup failed: {result}")
                except Exception as e:
                    st.error(f"Signup failed: Unexpected error occurred. Details: {e}")

    st.markdown(
        """
        <style>
        .link {
            color: #7289DA;
            text-decoration: none;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
# Login link
    st.markdown(
        """
        already have account? <a class="link" onclick="goToPage('login')">Login here</a>
        """,
        unsafe_allow_html=True
    )

def signup_user(username, email, password):
    payload = {"username": username, "email": email, "password": password}
    
    try:
        response = requests.post(signup_url, json=payload)
        
        if response.status_code == 200:  # Assuming 201 for successful creation
            return True
        else:
            return response.json().get("error", "Signup failed")
    
    except Exception as e:
        return f"Signup failed: {e}"

