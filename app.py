import streamlit as st


# I will try to make level 4 project and this should help all the beginners and also me.

st.sidebar.markdown("# **:blue[GitPilot]**")
feature = st.sidebar.selectbox("Choose a feature", ["Help"])

# first before going any deeper I will add "help" as a feature and then I will add more features later on. It wil also help me to shape the project in a better way.

if feature == "Help":
    st.header("Help")
    st.info("This is the help section. Here you can find information about how to use GitPilot and get assistance with any issues you may encounter.")
    st.subheader("Getting Started")
    st.write("To get started with GitPilot, simply select a feature from the sidebar and follow the instructions provided. If you have any questions or need further assistance, read the documentation.")
