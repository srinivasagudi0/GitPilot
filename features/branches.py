# the files name is kind of bad but ok.
import streamlit as st
from support import is_git_initialized as check_git
import os
import git

def show_current_branch(repo_dir):
    if os.path.isdir(repo_dir):
        if check_git(repo_dir):
            repo = git.Repo(repo_dir)

            try:
                st.write(f"Current branch: `{repo.active_branch.name}`")
            except Exception:
                st.warning("Make one commit first before using branches.")

            if st.button("Show Commit Log"):
                try:
                    st.code(repo.git.log("--oneline", "-5"))
                except Exception:
                    st.warning("No commits yet. Commit something first.")
            new_branch = st.text_input("New branch name")

            if st.button("Create Branch"):
                if new_branch:
                    try:
                        repo.git.checkout("-b", new_branch)
                        st.success(f"Created branch: {new_branch}")
                    except Exception as e:
                        st.error(f"Could not create branch: {e}")
                else:
                    st.warning("Type a branch name first.")
            else:
                st.warning("Git is not initialized in this folder.")
        else:
            st.error("That path doesn't seem to exist. Can you double-check it?")

# done i guess, but shoudl test it out.
