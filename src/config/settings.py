import streamlit as st

APP_TITLE = "Business Metrics Analysis Chatbot"
APP_ICON = "📊"

def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'processor' not in st.session_state:
        st.session_state.processor = None