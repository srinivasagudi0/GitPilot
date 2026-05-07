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
       
        st.session_state.show_changes = True
    if st.session_state.get("show_changes"):
       
        if project_path:
            try:
                repo = git.Repo(project_path)
                st.success("Connected to the repository branch: " + repo.active_branch.name)

                staged_files = [item.a_path for item in repo.index.diff("HEAD")]
                changed_files = [item.a_path for item in repo.index.diff(None)]
                untracked_files = repo.untracked_files
                all_changes = changed_files + untracked_files

                if staged_files:
                    st.subheader("Staged Changes:")
                    st.info("These files are already staged and ready for a commit.")
                    for file in staged_files:
                        with st.expander("What changed in " + file):
                            file_diff = repo.git.diff("--cached", "--", file)
                            if file_diff:
                                st.code(file_diff, language="diff")
                            else:
                                st.write("No preview available for this file.")

                if all_changes:
                    st.subheader("Unsaved Changes:")
                    st.info("These files have changes. Open a file to see what changed, then select the files you want to stage.")

                    selected_files = []
                    for file in all_changes:
                        if st.checkbox(file, key="stage_" + file):
                            selected_files.append(file)
                        with st.expander("What changed in " + file):
                            if file in untracked_files:
                                file_path = os.path.join(project_path, file)
                                try:
                                    with open(file_path, "r", encoding="utf-8", errors="replace") as opened_file:
                                        st.code(opened_file.read(), language="text")
                                
                                except Exception:
                                    st.warning("This file cannot be shown, but you can still stage it.")
                            else:
                                file_diff = repo.git.diff("--", file)
                                
                                if file_diff:
                                    st.code(file_diff, language="diff")
                                
                                else:
                                    st.write("No preview available for this file.")
                    if st.button("Stage Selected Files"):
                        if selected_files:
                            repo.git.add("--", *selected_files)
                            st.success("Staged " + str(len(selected_files)) + " file(s).")
                            st.rerun()
                        else:
                            st.warning("Select at least one file first.")
                if not staged_files and not all_changes:
                    st.write("Everything is up to date!")

            except git.exc.InvalidGitRepositoryError:
                st.warning("The repo doesn't exist.")
            

        else:
            st.error("Please enter project folder path first.")
