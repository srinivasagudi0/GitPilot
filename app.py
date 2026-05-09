import streamlit as st
import os
import git
from support import summarize_change

st.sidebar.markdown("# **:blue[GitPilot]**")
feature = st.sidebar.selectbox(
    "Choose a feature", ["Help"]
)

if feature == "Help":
    st.header("Help")
    st.write("""
A one-time learning app designed to help complete beginners confidently understand and use Git and file commits through simple, interactive guidance.
By the end of the course, users will be able to commit and manage files independently without confusion, fear, or self-doubt.

    """)
