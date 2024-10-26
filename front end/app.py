import streamlit as st
st.set_page_config(page_title="nosu",
    page_icon="🧊",
    layout="wide")
import requests
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the backend URL from the environment variable
backend_url = os.environ.get('Backend_url')

# Streamlit UI Layout
st.title("nosu")
#st.title("AI Business Idea Validator")




# Set background color
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: purple;
        text-align: center;
    }}
    .stTitle {{
        text-align: center;
    }}
    .stTextInput {{
        border-radius: 10px; 
        width: 40%; /* Adjust the width as needed */
        margin: 0 auto; /* Center the input field */
        border-radius: 10px; /* Adjust the border radius as needed */
    }}
    .stTextArea {{
        width: 40%; /* Adjust the width as needed */
        margin: 45 auto; /* Center the textarea */
        border-radius: 10px; /* Adjust the border radius as needed */
    }}
    </style>
    """,
    unsafe_allow_html=True,
)



st.write("""
### Validate Your Business Idea with AI
""")

# Input form for business idea with unique key
idea = st.text_area("Enter your business idea here:", key="idea_text_area")

# Optional input fields for additional details with unique keys
st.write("You can also provide more details to improve the evaluation accuracy (optional):")
target_market = st.text_input("Target Market (optional):", key="target_market_input")
initial_investment = st.text_input("Initial Investment (optional):", key="initial_investment_input")
industry = st.text_input("Industry or Sector (optional):", key="industry_input")

# Button to submit the idea
if st.button("Evaluate Idea"):
    if idea:
        with st.spinner('Analyzing your business idea...'):
            # Prepare the payload with additional data
            payload = {
                "idea": idea,
                "target_market": target_market,
                "initial_investment": initial_investment,
                "industry": industry
            }

            # Send the business idea to FastAPI for evaluation
            try:
                response = requests.post(backend_url, json=payload)
                
                # Check if the request was successful
                if response.status_code == 200:
                    feedback = response.json().get("feedback")
                    st.success("Here's your evaluation:")
                    st.markdown("### Detailed Report:")
                    st.write(feedback)
                else:
                    st.error(f"Error: Could not process your request. [Status Code: {response.status_code}]")

            except Exception as e:
                st.error(f"Failed to connect to the backend: {e}")
    else:
        st.warning("Please enter a business idea to evaluate.")
