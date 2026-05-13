import git
import os
import streamlit as st

def clone_repo(remote_url, save_path):
    if os.path.exists(save_path) and os.listdir(save_path):
        st.warning(f"The directory '{save_path}' already exists and is not empty. Please choose a different path.")
    else:
        git.Repo.clone_from(remote_url, save_path)
        st.success(f"Repository cloned successfully to '{save_path}'!")