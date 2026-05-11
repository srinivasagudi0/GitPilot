import streamlit as st
import git
import os
from support import is_git_initialized as check_git
from support import summarize_git_status as summarize_status

def show_git_status(repo_dir):
    if os.path.isdir(repo_dir):
            if check_git(repo_dir):
                repo = git.Repo(repo_dir)
                status = repo.git.status()
                st.code(status)
                if os.getenv("OPENAI_API_KEY"):
                    with st.spinner("Summarizing changes..."):
                        summary = summarize_status(status)
                    st.info(f"Summary: {summary}")
            else:
                st.warning("Looks like Git isn't set up here yet. Want to initialize it first?")
    else:
        st.error("That path doesn't seem to exist. Can you double-check it?")

def show_what_changed(repo_dir):
     if os.path.isdir(repo_dir) and check_git(repo_dir):
        repo = git.Repo(repo_dir)
        changed_files = repo.git.status("--short").splitlines()
        file_names = [file[3:] for file in changed_files]

        if file_names:
            selected_files = st.multiselect("Which files do you want to save?", file_names)
            if st.button("Save These Files"):
                if selected_files:
                    repo.git.add(*selected_files)
                    st.success("All set! Your files are ready to be committed.")
                else:
                    st.warning("Pick at least one file first.")
        else:
            st.success("Everything's up to date. Nothing new to save!")

