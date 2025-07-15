import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from triage import triage_agent
from runner import run_agent
from usecases import get_use_cases
# from agents.extensions.visualization import draw_graph  # Module not found - commented out
import datetime

# Load environment variables from .env file
load_dotenv()

st.title("Multi-Agent Demo")

# --- Agent Visualization ---
# Display and save the agent graph every time the app runs
# st.header("Agent Flow Visualization")
# filename = f"agent_graph_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
# draw_graph(triage_agent, filename=filename)  # This saves as PNG
# st.image(f"{filename}.png", caption="Agent Flow Graph", use_container_width=True)

st.header("Use Cases")
use_cases = get_use_cases()
for case in use_cases:
    st.markdown(f"**{case['name']}**: {case['description']}\n- _Example_: `{case['example']}`")

user_input = st.text_input("Ask a question:")

if user_input:
    with st.spinner("Thinking..."):
        result = asyncio.run(run_agent(triage_agent, user_input))
        st.write("**Agent Response:**")
        st.write(result.final_output) 