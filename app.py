import streamlit as st
import os
import git

# I will try to make level 4 project and this should help all the beginners and also me.

st.sidebar.markdown("# **:blue[GitPilot]**")
feature = st.sidebar.selectbox("Choose a feature", ["Help", "The 'What' Changed Feature"])

# first before going any deeper I will add "help" as a feature and then I will add more features later on. It wil also help me to shape the project in a better way.

if feature == "Help":
    st.header("Help")
    st.info("This is the help section. Here you can find information about how to use GitPilot and get assistance with any issues you may encounter.")
    st.header("Getting Started")
    st.write("To get started with GitPilot, simply select a feature from the sidebar and follow the instructions provided. If you have any questions or need further assistance, read the documentation.")
    st.subheader("The 'What' Changed Feature")
    st.info("This feature allows you to see what changes were made in a specific commit. You can view the differences between the current state of your code and the previous commit.")

if feature == "The 'What' Changed Feature":
    project_path = st.text_input("Enter your project folder path", value=os.getcwd())
    if st.button("Show Changes"):
        if project_path:
            try:
                repo = git.Repo(project_path)
                st.success("Connected to the repository branch: " + repo.active_branch.name)

                changed_files = [item.a_path for item in repo.index.diff(None)]
                untracked_files = repo.untracked_files
                all_changes = changed_files + untracked_files

                if all_changes:
                    st.subheader("Unsaved Changes:")
                    st.info("These files have changes. Select which ones you want to stage for commit.")

                    selected_files = []
                    for file in all_changes:
                        if st.checkbox(file, key=file):
                            selected_files.append(file, key=file)
                        if st.button("Stage Selected Files"):
                            repo.index.add(selected_files)
                            st.rerun()
                else:
                    st.write("Everything is up to date!")

            except git.exc.InvalidGitRepositoryError:
                st.warning("The repo doesn't exist.")
            except Exception as e:
                st.error("Unexpected Error" + e)
                

        else:
            st.error("Please enter project folder path first.")
