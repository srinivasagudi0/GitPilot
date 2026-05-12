import streamlit as st

def show_vocab():
    st.header("Git Vocabulary")
    st.write("Here are some key Git terms to know:")
    st.markdown("**Repository (Repo)**: A folder that holds all your project files and keeps track of every change you make.")
    st.markdown("**Commit**: A saved snapshot of your files at a specific moment. Think of it like taking a photo of your work.")
    st.markdown("**Branch**: A separate workspace where you can work on new ideas without changing your main project.")
    st.markdown("**Merge**: Combining changes from one branch back into another branch.")
    st.markdown("**Remote**: Your project stored online (like on GitHub) that you can share with others.")
    st.markdown("**Push**: Uploading your saved changes to the online version of your project.")
    st.markdown("**Pull**: Downloading the latest changes from the online project to your computer.")
    st.markdown("**Stage**: Selecting which files you want to save in your next commit.")
    st.markdown("**Clone**: Downloading a copy of someone's project to your computer.")
    st.markdown("**Fork**: Making your own personal copy of someone else's project on GitHub.")
    st.markdown("**Conflict**: When Git can't automatically combine changes and needs you to decide which version to keep.")
    
#  