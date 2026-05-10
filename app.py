import streamlit as st
import os
import git
from support import is_git_initialized as check_git


features = ["Start Here", "Vocabulary","Initialize Git", "Status & Stage Files"]
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

if feature == "Vocabulary":
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

    if feature == "Status & Stage Files":
        st.header("Status & Stage Files")
        
        st.write("Before you save your work with Git, it's helpful to check what's changed. Think of it like reviewing your edits before hitting save.")
        st.write("Here are the commands you'd normally use:")
        st.code("git status\ngit add file_name", language="bash")
        
        st.info("Let me handle this for you. Just pick your project folder and use the tools below.")

        repo_dir = st.text_input("Where's your project?", value=os.getcwd())

        if st.button("See What Changed"):
            try:
                if os.path.isdir(repo_dir):
                    if check_git(repo_dir):
                        repo = git.Repo(repo_dir)
                        status = repo.git.status()
                        st.code(status)
                    else:
                        st.warning("Looks like Git isn't set up here yet. Want to initialize it first?")
                else:
                    st.error("That path doesn't seem to exist. Can you double-check it?")
            except Exception as e:
                st.error(f"Oops, something went wrong: {e}")

        if os.path.isdir(repo_dir) and check_git(repo_dir):
            repo = git.Repo(repo_dir)
            changed_files = repo.git.status("--short").splitlines()
            file_names = [file[3:] for file in changed_files]

            if file_names:
                selected_files = st.multiselect("Which files do you want to save?", file_names)
                if st.button("Save These Files"):
                    if selected_files:
                        repo.git.add(selected_files)
                        st.success("All set! Your files are ready to be committed.")
                    else:
                        st.warning("Pick at least one file first.")
            else:
                st.success("Everything's up to date. Nothing new to save!")

        st.subheader("Here's what's happening:")
        st.write("You get to see all the files you've modified in your project.")
        st.write("You pick and choose which ones you want to include in your next save.")
        st.write("This is just a prep step—you're not actually saving anything yet, just getting ready.")

