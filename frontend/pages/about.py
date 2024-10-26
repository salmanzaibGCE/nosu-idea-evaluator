import streamlit as st

# Set up the page title and layout
st.set_page_config(page_title="About - nosu", layout="wide")

# About Page Content
st.title("About nosu")
st.write("""
### AI Business Idea Validator

nosu is an AI-powered platform designed to help you evaluate your business ideas efficiently and effectively. 
Our system leverages advanced AI algorithms to provide insightful feedback on various aspects of your ideas, 
including feasibility, market potential, and more.

Whether you're a budding entrepreneur or an experienced business owner, nosu is here to guide you on your journey to success.
""")

# Navigation Links
st.markdown(
    """
    [Back to Home](/app)
    """
)
