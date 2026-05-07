import streamlit as st

st.title("GitPilot")

# I will try to make level 4 project and this should help all the beginners and also me.

st.sidebar.header("Select a feature")
feature = st.sidebar.selectbox("Choose a feature", ["Help"])

# first before going any deeper I will add "help" as a feature and then I will add more features later on. It wil also help me to shape the project in a better way.

if feature == "Help":
    pass
