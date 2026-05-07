import streamlit as st

top, bottom = st.columns(2)
with top:
    left, right = st.columns(2)
    with left:
        st.title("GitPilot")
    with right:
        st.write("Thinking what to write here")
# I will try to make level 4 project and this should help all the beginners and also me.

st.sidebar.header("Select a feature")
feature = st.sidebar.selectbox("Choose a feature", ["Help"])

# first before going any deeper I will add "help" as a feature and then I will add more features later on. It wil also help me to shape the project in a better way.

if feature == "Help":
    st.header("Help")
    st.info("This is the help section. Here you can find information about how to use GitPilot and get assistance with any issues you may encounter.")
    st.subheader("Getting Started")
    st.write("To get started with GitPilot, simply select a feature from the sidebar and follow the instructions provided. If you have any questions or need further assistance, read the documentation.")
