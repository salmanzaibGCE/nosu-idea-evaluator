import streamlit as st
import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Backend URL from environment variable
backend_url = os.getenv("Backend_url")
evaluate_url = f"{backend_url}/evaluate"

def show_home_page():
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False  # Default to not logged in

    # Check for a valid session cookie
    if 'session_cookie' in st.session_state and st.session_state.session_cookie:
        try:
            # Verify the session cookie with a backend call
            response = requests.get(f"{backend_url}/verify_session", headers={'Cookie': f'session={st.session_state.session_cookie}'})
            if response.status_code == 200:
                st.session_state.logged_in = True  # Set to true if cookie is valid
            else:
                st.session_state.logged_in = False  # Invalid cookie
        except Exception as e:
            st.error(f"Error verifying session: {e}")
            st.session_state.logged_in = False  # Assume not logged in on error

    if not st.session_state.logged_in:
        st.error("You must be logged in to submit an idea.")
        return

    # Custom CSS to match Figma design
    st.markdown(
        f"""
        <style>
        body {{ background-color: #4B0082; }}
        .stApp {{ font-family: Open Sans, sans-serif; color: #FFFFFF; text-align: center; }}
        .stTitle {{ font-weight: bold; font-size: 48px; margin-top: 30px; margin-bottom: 10px; }}
        .welcome {{ font-size: 24px; margin-bottom: 20px; }}
        .prompt {{ font-size: 18px; margin-bottom: 30px; }}
        .feedback-section {{ margin-top: 40px; text-align: left; }}
        .feedback-label {{ font-weight: bold; font-size: 20px; }}
        .feedback-content {{ font-size: 18px; color: #CCCCCC; }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Navigation links with logout functionality
    st.markdown(
        """
        <div class="nav-links">
            <a href="#dashboard">Dashboard</a>
            <a href="#about">About</a>
            <a href="#sign-out" onclick="logout()">Sign Out</a>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Header
    st.markdown("<h1 class='stTitle'>nosu</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='welcome'>Welcome, {st.session_state.user_email}!</p>", unsafe_allow_html=True)
    st.markdown("<p class='prompt'>Submit your hackathon idea for evaluation</p>", unsafe_allow_html=True)

    # Idea submission input
    idea = st.text_area("Your idea...", placeholder="Your idea...", key="idea_input", height=150)

    # Submit button and backend interaction
    if st.button("Submit", key="submit_button"):
        if idea:
            with st.spinner("Generating feedback..."):
                feedback = evaluate_idea(idea)
                if feedback:
                    display_feedback(idea, feedback)
                else:
                    st.error("An error occurred while generating feedback.")
        else:
            st.error("Please enter your idea.")


def evaluate_idea(idea):
    payload = {"idea": idea}
    headers = {}

    if 'session_cookie' in st.session_state:
       headers['Cookie'] = f"session={st.session_state.session_cookie}"
    
    logging.info(f"Sending POST request to: {evaluate_url}")
    logging.info(f"Payload: {payload}")
    logging.info(f"Headers: {headers}")

    try:
        response = requests.post(evaluate_url, json=payload, headers={'Cookie': f'session={st.session_state.session_cookie}'})
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Text: {response.text}")

        if response.status_code == 200:
            return response.json().get("feedback")
        else:
            st.error(f"Error from backend: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return None

def display_feedback(idea, feedback):
    st.markdown("<div class='feedback-section'>", unsafe_allow_html=True)
    st.markdown(f"<p class='feedback-label'>Your Idea:</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='feedback-content'>{idea}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='feedback-label'>Feedback from Nosu AI:</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='feedback-content'>{feedback}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.page = 'login'  # Redirect to login page
    #st._rerun()




"""
def evaluate_idea(idea):
    payload = {"idea": idea}
    headers = {}
    
    if 'session_cookie' in st.session_state:
        headers = {'Cookie': f'session={st.session_state.session_cookie}'}
        headers['Cookie'] = st.session_state.session_cookie
    
    try:
        response = requests.post(evaluate_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("feedback")
        else:
            st.error(f"Error from backend: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return None"""
