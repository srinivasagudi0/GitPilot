import git
import os
import streamlit as st

def practice_git():
    practice_dir = os.path.join(os.path.expanduser("~"), "GitPilot_Practice")
    
    if st.button("Create Practice Repo"):
        try:
            if not os.path.exists(practice_dir):
                os.makedirs(practice_dir)
            git.Repo.init(practice_dir) # STEP 1
            st.success(f"Practice repo created at: {practice_dir}")
        except Exception as e:
            st.error(f"Could not create practice repo: {e}")
    
    if os.path.exists(practice_dir) and check_git(practice_dir):
        st.info(f"Practice repo location: `{practice_dir}`")
        
        repo = git.Repo(practice_dir) # STEP 2
        
        st.subheader("Create a test file")
        test_filename = st.text_input("File name", value="test.txt")
        test_content = st.text_area("File content", value="i am learning git wiht Gitpilot! and it is so so cool!")
        
        if st.button("Create File"):
            try:
                with open(os.path.join(practice_dir, test_filename), "w") as f:
                    f.write(test_content)
                st.success(f"Created {test_filename}")
            except Exception as e:
                st.error(f"Could not create file: {e}")
        
        st.subheader("Try Git commands")
        if st.button("Show Status"):
            status = repo.git.status() # STEP 3
            st.code(status)
        
        if st.button("Reset Everything"):
            try:
                repo.git.reset("--hard")
                st.success("Practice repo reset to clean state.")
            except Exception as e:
                st.error(f"Could not reset: {e}")
    