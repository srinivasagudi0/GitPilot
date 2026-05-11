# will later refactor the code into muliple modules and add more features but for now this is the basic structure of the app.
import streamlit as st
import os
import git
from support import is_git_initialized as check_git
from support import summarize_git_status as summarize_status


features = ["Start Here", "Vocabulary","Initialize Git", "Status & Stage Files", "Commit Files", "Log & Branch", "Add Remote & Push"]
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
    st.warning("Don't worry about making mistakes. I would recommend makeing a test repo and just trying things out. You can always reset your repo if you mess up. *The best way to learn is by doing!*")
    st.info("I also recommend going one feature at a time and really trying it out before moving on to the next one. You can always come back to review any feature as many times as you want.")

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
                    if os.getenv("OPENAI_API_KEY"):
                        with st.spinner("Summarizing changes..."):
                            summary = summarize_status(status)
                        st.info(f"Summary: {summary}")
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
                    repo.git.add(*selected_files)
                    st.success("All set! Your files are ready to be committed.")
                else:
                    st.warning("Pick at least one file first.")
        else:
            st.success("Everything's up to date. Nothing new to save!")

    st.subheader("Here's what's happening:")
    st.write("You get to see all the files you've modified in your project.")
    st.write("You pick and choose which ones you want to include in your next save.")
    st.write("This is just a prep step—you're not actually saving anything yet, just getting ready.")

if feature == "Commit Files":
    st.header("Commit Files")
    st.write("Committing is like taking a snapshot of your project at a specific moment. It saves your changes so you can look back or share them later.")
    st.write("Here's the command you'd use:")
    st.code('git commit -m "Your commit message here"', language="bash")
    
    st.info("Let's do this together! Just pick your project folder and write a message about what you've changed.")

    repo_dir = st.text_input("Where's your project?", value=os.getcwd())
    commit_message = st.text_input("What's this change about?", value="My commit message")

    if os.path.isdir(repo_dir) and check_git(repo_dir):
        repo = git.Repo(repo_dir)
        staged_files = repo.git.diff("--cached", "--name-only").splitlines()

        if staged_files:
            st.write("Files ready to commit:")
            st.write(staged_files)
        else:
            st.warning("No files are staged yet. Go to Status & Stage Files first.")

    if st.button("Commit Changes"):
        try:
            if os.path.isdir(repo_dir):
                if check_git(repo_dir):
                    repo = git.Repo(repo_dir)
                    staged_files = repo.git.diff("--cached", "--name-only").splitlines()

                    if not commit_message.strip():
                        st.warning("Write a commit message first.")
                    elif staged_files:
                        repo.git.commit("-m", commit_message)
                        st.success("Great job! Your changes have been committed.")
                    else:
                        st.warning("Stage at least one file before committing.")
                else:
                    st.warning("Git isn't set up here yet. Do you want to initialize it first?")
            else:
                st.error("That path doesn't seem to exist. Can you double-check it?")
        except Exception as e:
            st.error(f"Oops, something went wrong: {e}")

    st.subheader("Here's what's happening:")
    st.write("Git takes the files you staged and saves them as one commit.")
    st.write("Your commit message should briefly explain what changed.")
    st.write("After committing, you have a saved checkpoint you can return to later.")
    
    st.warning("Remember, committing doesn't upload your changes anywhere yet. It's just saving them on your computer. To share them online, you'll need to push them to a remote repository like GitHub.")

if feature == "Log & Branch":
    # this is not really useful begginners but good to know what it is
    st.header("Git Log & Branches")

    st.write("Git log shows your commits. Branches show different versions of your project.")
    st.write("Here are the commands you'd normally use:")
    st.code("git log --oneline\ngit branch\ngit checkout -b branch_name", language="bash")

    st.info("Let me handle this for you. Pick your project folder and use the tools below.")

    repo_dir = st.text_input("Where's your project?", value=os.getcwd())

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

    st.subheader("Here's what's happening:")
    st.write("The log shows saved commits.")
    st.write("A branch is a separate place to work on your project.")

if feature == "Add Remote & Push":
    st.header("Add Remote & Push")

    st.write("A remote is the online version of your project, like a GitHub repo.")
    st.write("Pushing uploads your commits from your computer to that online repo.")
    st.write("Here are the commands you'd normally use:")
    st.code("git remote add origin URL\ngit push -u origin branch_name", language="bash")

    st.info("Let me handle this for you. Pick your project folder and paste your GitHub repo URL.")

    repo_dir = st.text_input("Where's your project?", value=os.getcwd())
    remote_url = st.text_input("GitHub repo URL")

    if os.path.isdir(repo_dir):
        if check_git(repo_dir):
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
                    if branch_to_push:
                        if current_branch != branch_to_push:
                            repo.git.checkout(branch_to_push)
                        repo.git.push("-u", "origin", branch_to_push)
                        st.success(f"Pushed `{branch_to_push}` to GitHub.")
                    else:
                        st.warning("Make one commit first before pushing.")
                except Exception as e:
                    st.error(f"Could not push: {e}")
        else:
            st.warning("Git is not initialized in this folder.")
    else:
        st.error("That path doesn't seem to exist. Can you double-check it?")

    st.subheader("Here's what's happening:")
    st.write("The remote connects your local project to GitHub.")
    st.write("Push sends your commits to GitHub so they are online.")



# ---test the below feature and add it to the sidebar if it works.

if feature == "Clone & Pull":
    st.header("Clone & Pull")
    st.write("Cloning is downloading a project from GitHub to your computer. \nPulling is getting the latest changes from GitHub to your computer.")

    st.code('#get the repo on to your computer\ngit clone URL \n#pull the latest changes\ngit pull origin main', language="bash")
    st.info("Let me handle this for you. Paste the GitHub repo URL and choose where to save it.")
    remote_url = st.text_input("GitHub repo URL")
    save_path = st.text_input("Where do you want to save the project?", value=os.getcwd())
    if st.button("Clone Repository"):
        try:
            if remote_url and save_path:
                if os.path.exists(save_path) and os.listdir(save_path):
                    st.warning("The save path is not empty. Please choose an empty folder or a new path.")
                else:
                    git.Repo.clone_from(remote_url, save_path)
                    st.success("Repository cloned successfully!")
            else:
                st.warning("Please enter both the GitHub repo URL and the save path.")
        except Exception as e:
            st.error(f"Could not clone repository: {e}")
    st.subheader("Here's what's happening:")
    st.write("Cloning creates a local copy of the GitHub project on your computer.")
    st.write("Pulling updates your local copy with the latest changes from GitHub.")

# Just a fun check and it willwork as expected but test it out afternoon and then add it to the sidebar.
if feature == "Graduation":
    st.header("Congratulations!")
    st.write("You've completed the GitPilot training program!")
    st.subheader("What You've Learned:")
    st.checkbox("Initialize Git in a project")
    st.checkbox("Check status and stage files")
    st.checkbox("Commit your changes")
    st.checkbox("View logs and create branches")
    st.checkbox("Add remote and push to GitHub")
    st.checkbox("Clone repositories")
    st.write("\nYou're ready to use Git confidently!")
    st.write("Keep practicing to become a Git pro!")
    st.warning("Remember, the best way to learn Git is by using it regularly. Don't be afraid to experiment and make mistakes. Happy coding!")

    if st.button("Celebrate with Confetti!"):
        st.balloons()
### Will now work on making the app more expert level whilst still being beginner friendly. 

# will test the beow feature before add it to the sidebar but it should wrk as expected.
if feature == "Undo & Rollback":
    st.header("Undo & Rollback")
    st.write("Made a mistake? Git lets you go back to earlier versions of your work.")
    st.write("Here are the commands you'd normally use:")
    
    st.code("git restore file_name\ngit revert HEAD\ngit reset --hard HEAD~1", language="bash")
    
    st.info("Let me help you undo changes safely. Pick your project folder.")
    
    repo_dir = st.text_input("Where's your project at?", value=os.getcwd())
    
    if os.path.isdir(repo_dir) and check_git(repo_dir):
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
        #st.warning("Git is not initialized in this folder.")
        try:
            if os.path.exists(repo_dir):
                st.info("This folder exists but Git isn't set up here yet. Want to initialize it first?")
            else:
                st.error("That path doesn't seem to exist. Can you double-check it?")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    st.subheader("Here's what's happening:")
    st.write("Restore: Takes a file back to its last saved state. Version Control's way of saying 'undo' for files.")
    st.write("Reset: Undoes a commit but keeps your changes.")


if feature == "Practice Mode":
    st.header("Practice Mode - Try Git Safely")
    st.write("Practice Git commands in a safe sandbox without affecting your real projects.")
    
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
    
    st.subheader("Why practice mode?")
    st.write("Experiment without worrying about breaking your real projects.")
    st.write("Try different Git commands and see what happens.")
