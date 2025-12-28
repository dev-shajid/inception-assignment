import streamlit as st
from config.settings import settings
from jarvis.assistant import Agent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="centered"
)

@st.cache_resource
def get_agent():
    try:
        return Agent(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Agent: {e}")
        return None

agent = get_agent()

# Sidebar
with st.sidebar:
    st.title("⚙️ Controls")
    
    selected_role = st.selectbox(
        "Select Assistant Role",
        ["Tutor", "Coder", "Mentor"],
        index=0
    )
    
    if st.button("🗑️ Clear Memory"):
        if agent:
            agent.clear_memory()
            st.success("Memory cleared!")
            st.rerun()

    st.markdown("---")
    st.markdown("*Powered by Google Gemini*")

# Main Interface
st.title("🤖 JARVIS AI Assistant")

if not agent:
    st.error("Application failed to initialize. Please check your logs.")
    st.stop()

# Display Chat History
history = agent.get_history()

for msg in history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["message"])

# Chat Input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response with streaming
    try:
        with st.chat_message("assistant"):
            # st.write_stream consumes a generator and streams the output to the UI
            response_stream = agent.respond_stream(prompt, role=selected_role)
            st.write_stream(response_stream)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        logger.error(f"Error during response generation: {e}")
