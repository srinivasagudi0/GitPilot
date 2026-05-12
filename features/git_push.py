import streamlit as st
import git


def push_changes(repo_dir, remote_url):
    repo = git.Repo(repo_dir)

    try:
        current_branch = repo.active_branch.name
        st.write(f"Current branch: `{current_branch}`")
    except Exception:
        current_branch = ""
        st.warning("Make one commit first before pushing.")

    branches = [branch.name for branch in repo.branches]
    if branches:
        default_branch = "main" if "main" in branches else current_branch
        branch_to_push = st.selectbox(
            "Branch to push",
            branches,
            index=branches.index(default_branch),
        )
    else:
        branch_to_push = ""

    remotes = [remote.name for remote in repo.remotes]

    if remotes:
        st.write("Current remotes:")
        st.write(remotes)
    else:
        st.warning("No remote added yet.")

    if st.button("Add Remote"):
        if remote_url:
            try:
                if "origin" in remotes:
                    repo.git.remote("set-url", "origin", remote_url)
                    st.success("Updated origin remote.")
                else:
                    repo.git.remote("add", "origin", remote_url)
                    st.success("Added origin remote.")
            except Exception as e:
                st.error(f"Could not add remote: {e}")
        else:
            st.warning("Paste your GitHub repo URL first.")

        if st.button("Push to GitHub"):
            try:
                if not branch_to_push:
                    st.warning("Make one commit first before pushing.")
                else:
                    remotes = [remote.name for remote in repo.remotes]
                    if remote_url:
                        if "origin" in remotes:
                            repo.git.remote("set-url", "origin", remote_url)
                        else:
                            repo.git.remote("add", "origin", remote_url)
                    elif "origin" not in remotes:
                        st.warning("Paste your GitHub repo URL first.")
                        st.stop()

                    if current_branch != branch_to_push:
                        repo.git.checkout(branch_to_push)
                    repo.git.push("-u", "origin", branch_to_push)


                    st.success(f"Pushed `{branch_to_push}` to GitHub.")
            except Exception as e:
                st.error(f"Could not push: {e}")
            