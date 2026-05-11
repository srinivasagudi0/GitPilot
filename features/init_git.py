
import os
import git
import streamlit as st

from support import is_git_initialized as check_git


def initialize_git(repo_dir):
    try:
        if os.path.isdir(repo_dir):
            if check_git(repo_dir):
                st.warning("Git is already initialized in this folder.")
            else:
                git.Repo.init(repo_dir)
                st.success("Git has been initialized successfully!")
        else:
            st.error("The specified path does not exist. Please enter a valid path.")
    except Exception as e:
        st.error(f"An error occurred while initializing Git: {e}")
    
