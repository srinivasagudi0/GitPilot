import streamlit as st
import os
import git
from support import is_git_initialized as check_git


features = ["Start Here", "Initialize Git"]
st.sidebar.markdown("# **:blue[GitPilot]**")
feature = st.sidebar.selectbox(
    "Choose a feature", [feature for feature in features]
)

# first 
if feature == "Start Here":
    st.header("Welcome to GitPilot!")
    st.write("""**GitPilot** is a one-time learning app designed to help complete beginners confidently understand and use Git and file commits through simple, interactive guidance.
By the end of the course, users will be able to commit and manage files independently without confusion, fear, or self-doubt.""")
    st.write("Let's get started!")
    st.info("Choose a feature from the sidebar to begin your Git learning journey.")

    
if feature == "Initialize Git":
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Initialize Git")
    st.write("Initializing git is one of the `very important` steps to start using git commands.")
    st.write("To initialize git, you can use the following command in your terminal:")
    st.code("git init", language="bash")
    st.info("I will do this for you. Choose your project directory, then click the button below.")

    repo_dir = st.text_input("Project directory", value=os.getcwd())

    if st.button("Initialize Git"):
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
    st.subheader("What this does:")
    st.write("Starts Git tracking in this folder.")
    st.write("Creates a hidden `.git` directory for version control (lets you track changes to your files, save different versions, and collaborate with others safely).")
    st.write("After this, you can start using Git commands to manage your project.")
