import os
import git
from support import is_git_initialized as check_git
import streamlit as st

def show_staged_files(repo_dir):
    if os.path.isdir(repo_dir) and check_git(repo_dir):
        repo = git.Repo(repo_dir)
        staged_files = repo.git.diff("--cached", "--name-only").splitlines()
    if staged_files:
        st.write("Files ready to commit:")
        st.write(staged_files)
    else:
        st.warning("No files are staged yet. Go to Status & Stage Files first.")

def commit_changes(repo_dir, commit_message):
    if os.path.isdir(repo_dir):
        if check_git(repo_dir):
            repo = git.Repo(repo_dir)
            staged_files = repo.git.diff("--cached", "--name-only").splitlines()

            if not commit_message.strip():
                st.warning("Write a commit message first.")
            elif staged_files:
                repo.git.commit("-m", commit_message)
                st.success("Great job! Your changes have been committed.")
            else:
                st.warning("Stage at least one file before committing.")
        else:
            st.warning("Git isn't set up here yet. Do you want to initialize it first?")
    else:
        st.error("That path doesn't seem to exist. Can you double-check it?")
