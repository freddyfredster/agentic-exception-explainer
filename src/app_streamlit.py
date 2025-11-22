import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.agent import run_agent

import streamlit as st


st.set_page_config(page_title="Exception Explainer", page_icon="📉")

st.title("📊 Agentic Exception Explainer")

st.markdown(
    "Ask why a KPI changed. For example:\n\n"
    "- `Why did Product B sales in the North drop in 2025-08?`\n"
    "- `What happened to Product B in the North between July and August 2025?`"
)

# Simple in-memory chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Render previous messages
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask a question about KPI changes...")

if user_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": user_input})

    # Call the agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = run_agent(
                user_message=user_input,
                history=st.session_state.history[:-1],  # everything except this latest user msg
            )
            st.markdown(answer)

    # Add assistant reply to history
    st.session_state.history.append({"role": "assistant", "content": answer})
