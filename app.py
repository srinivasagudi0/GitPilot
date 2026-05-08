import streamlit as st
import os
import git
from support import summarize_change

st.sidebar.markdown("# **:blue[GitPilot]**")
feature = st.sidebar.selectbox(
    "Choose a feature", ["Help", "The 'What' Changed Feature"]
)

if feature == "Help":
    st.header("Help")
    st.info("GitPilot helps you inspect local Git changes before staging them.")
    st.header("Getting Started")
    st.write("Choose a feature from the sidebar and enter the path to a Git repo.")
    st.subheader("The 'What' Changed Feature")
    st.info(
        "This shows staged, unstaged, and untracked changes with a short AI summary when available."
    )

if feature == "The 'What' Changed Feature":
    project_path = st.text_input("Enter your project folder path", value=os.getcwd())
    if st.button("Show Changes"):

        st.session_state.show_changes = True
    if st.session_state.get("show_changes"):

        if project_path:
            try:
                repo = git.Repo(project_path)
                st.success(
                    "Connected to the repository branch: " + repo.active_branch.name
                )

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
                                summary = summarize_change(file_diff)
                                st.write(summary)
                                st.code(file_diff, language="diff")
                            else:
                                st.write("No preview available for this file.")

                if all_changes:
                    st.subheader("Unsaved Changes:")
                    st.info(
                        "Open a file to review it, then select anything you want to stage."
                    )

                    selected_files = []
                    for file in all_changes:
                        if st.checkbox(file, key="stage_" + file):
                            selected_files.append(file)
                        with st.expander("What changed in " + file):
                            if file in untracked_files:
                                file_path = os.path.join(project_path, file)
                                try:
                                    with open(
                                        file_path,
                                        "r",
                                        encoding="utf-8",
                                        errors="replace",
                                    ) as opened_file:
                                        content = opened_file.read()
                                        summary = summarize_change(content)
                                        st.write(summary)
                                        st.code(content)

                                except Exception:
                                    st.warning(
                                        "This file cannot be shown, but you can still stage it."
                                    )
                            else:
                                file_diff = repo.git.diff("--", file)

                                if file_diff:
                                    summary = summarize_change(file_diff)
                                    st.write(summary)
                                    st.code(file_diff, language="diff")

                                else:
                                    st.write("No preview available for this file.")
                    if st.button("Stage Selected Files"):
                        if selected_files:
                            repo.git.add("--", *selected_files)
                            st.success(
                                "Staged " + str(len(selected_files)) + " file(s)."
                            )
                            st.rerun()
                        else:
                            st.warning("Select at least one file first.")
                if not staged_files and not all_changes:
                    st.write("Everything is up to date!")

            except git.exc.InvalidGitRepositoryError:
                st.warning("The repo doesn't exist.")

        else:
            st.error("Please enter project folder path first.")
