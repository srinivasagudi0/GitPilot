import git
import streamlit as st
import os

def rollback_commit(repo_dir):
    repo = git.Repo(repo_dir)
    
    st.subheader("Undo unstaged changes")
    unstaged_files = repo.git.status("--short").splitlines()
    file_names = [file[3:] for file in unstaged_files if file.startswith(" M")]
    
    if file_names:
        selected_file = st.selectbox("Which file to restore?", file_names)
        if st.button("Restore File"):
            try:
                repo.git.restore(selected_file)
                st.success(f"Restored {selected_file} to last commit.")
            except Exception as e:
                st.error(f"Could not restore because of {e}")
    else:
        st.info("No unstaged changes to restore.")
    
    st.subheader("Undo last commit")
    try:
        last_commit = repo.head.commit.message.strip()
        st.write(f"Last commit: {last_commit}")
        if st.button("Undo Last Commit"):
            repo.git.reset("--soft", "HEAD~1")
            st.success("Commit undone. Files are staged again.")
            st.warning("Even thoough the commit can be undone, it is recommended to not do this on commits that have been pushed to GitHub because it can cause issues for other collaborators. Use `git revert HEAD` instead to create a new commit that undoes the changes.") # really cool fact btw that I just learned and added to the app.
    except Exception:
        st.info("No commits to undo yet.") 
    else:
        st.warning("Git is not initialized in this folder.")
    try:
        if os.path.exists(repo_dir):
            st.warning("This folder exists but Git isn't set up here yet. Want to initialize it first?")
        else:
            st.error("That path doesn't seem to exist. Can you double-check it?")
    except Exception as e:
        st.error(f"An error occurred: {e}")
