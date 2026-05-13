from features.status_stage import show_git_status, show_what_changed
import streamlit as st
import os
from support import is_git_initialized as check_git
from support import summarize_git_status as summarize_status
from features.auth import require_login, show_logout_button
from features.vocab import show_vocab
from features.init_git import initialize_git    
from features.commit import show_staged_files, commit_changes
from features.branches import show_current_branch as current_branch
from features.git_push import push_changes
from features.clone_pull import clone_repo
from features.graduation import Graduate
from features.rollback import rollback_commit
from features.practice_git import practice_git
from features.article import article
from features.analytics import show_repo_analytics

require_login()


features = ["Start Here", "Vocabulary","Initialize Git", "Status & Stage Files", "Commit Files", "Log & Branch", "Add Remote & Push"]
st.sidebar.markdown("# **:blue[GitPilot]**")
show_logout_button()
st.sidebar.write("You can use the sidebar to navigate through the different learning sections of GitPilot.\n Each feature is designed to help you learn Git step by step or only what is required, with interactive tools and explanations.\n Just pick a feature to get started on your Git learning journey!")
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
    show_vocab()

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
        if os.path.isdir(repo_dir):
            if not check_git(repo_dir):
                try:
                    initialize_git(repo_dir)
                    st.success("Git initialized successfully!")
                except Exception as e:
                    st.error(f"Could not initialize Git: {e}")
            else:
                st.warning("Git is already initialized in this folder.")
        else:
            st.warning("That path doesn't seem to exist. Can you double-check it?")

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
                    show_git_status(repo_dir)
                else:
                    st.warning("Looks like Git isn't set up here yet. Want to initialize it first?")
            else:
                st.error("That path doesn't seem to exist. Can you double-check it?")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

    show_what_changed(repo_dir)

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

    if os.path.isdir(repo_dir):
        if check_git(repo_dir):
            show_staged_files(repo_dir)
        else:
            st.warning("Git isn't set up here yet. Want to initialize it first?")
    else:
        st.error("That path doesn't seem to exist. Can you double-check it?")

    if st.button("Commit Changes"):
        try:
            # dont need to check twice because i did it above and it is for the same directory.
            commit_changes(repo_dir, commit_message)
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
            current_branch(repo_dir)
        else:
            st.warning("Git isn't set up here yet. Want to initialize it first?")
    else:
        st.error("That path doesn't seem to exist. Can you double-check it?")
    #current_branch(repo_dir)
    
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
            try:
                push_changes(repo_dir, remote_url)
            except Exception as e:
                st.error(f"Oops, something went wrong: {e}")
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
                clone_repo(remote_url, save_path)
            else:
                st.warning("Please enter both the GitHub repo URL and the save path.")
        except Exception as e:
            st.error(f"Could not clone repository: {e}")
    st.subheader("Here's what's happening:")
    st.write("Cloning creates a local copy of the GitHub project on your computer.")
    st.write("Pulling updates your local copy with the latest changes from GitHub.")

# Just a fun check and it willwork as expected but test it out afternoon and then add it to the sidebar.
if feature == "Graduation":
    Graduate()
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
        rollback_commit(repo_dir)
    
    st.subheader("Here's what's happening:")
    st.write("Restore: Takes a file back to its last saved state. Version Control's way of saying 'undo' for files.")
    st.write("Reset: Undoes a commit but keeps your changes.")

if feature == "Practice Mode":
    st.header("Practice Mode - Try Git Safely")
    st.write("Practice Git commands in a safe sandbox without affecting your real projects.")
    practice_git()
    
    st.subheader("Why practice mode?")
    st.write("Experiment without worrying about breaking your real projects.")
    st.write("Try different Git commands and see what happens.")

if feature == "Progress Tracker":
    st.header("Your Learning Progress Tracker")
    st.write("Track what you've learned so far!")
    # this is better to be here insstead of refacotring somewhere
    progress_items = {
        "Initialize Git": False,
        "Check Status & Stage Files": False,
        "Commit Files": False,
        "View Logs & Branches": False,
        "Add Remote & Push": False,
        "Undo & Rollback": False,
        "Clone & Pull": False,
    } #### HEREEE###
    # I will add features, but for now, only features here are that from the sidebar. Once I add the testing features to sidebar, I willl add them abovee
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Completed")
        for item in progress_items:
            st.checkbox(item, value=False)
    
    with col2:
        completed = sum(1 for v in progress_items.values() if v)
        total = len(progress_items)
        st.metric("Lessons Completed", f"{completed}/{total}")
        st.progress(completed / total if total > 0 else 0)
    
    st.info("Come back to this page after completing each feature to check it off!")

if feature == "Quick Reference":
    st.header("Git Quick Reference")
    st.write("A handy guide for common Git commands and what they do.")
    # looks reakky bad here i know.
    with st.expander("Basic Commands"):
        st.code("git init          # Start Git in a folder\ngit status        # See what changed\ngit add file      # Stage a file\ngit commit -m msg # Save changes\ngit log           # View history", language="bash")
    
    with st.expander("Branches"):
        st.code("git branch                  # List branches\ngit branch new_branch      # Create branch\ngit checkout new_branch    # Switch branch\ngit merge branch_name      # Combine branches", language="bash")
    
    with st.expander("Remote & Push"):
        st.code("git remote add origin URL   # Connect to GitHub\ngit push -u origin main    # Upload changes\ngit pull origin main       # Download changes\ngit clone URL              # Copy a project", language="bash")
    
    with st.expander("Undo & Fix"):
        st.code("git restore file           # Undo file changes\ngit reset HEAD~1           # Undo last commit\ngit revert HEAD            # Create opposite commit", language="bash")
    with st.expander("Tips"):
        st.write("- Use `git status` often to see what's going on.")
        st.write("- Write clear commit messages to remember your changes.")
        st.warning("- Don't be afraid to experiment and make mistakes. That's how you learn!")

# now the below one is my very very personal faviorite, it is about github facts and it has nothing to do with learnong git but a wow fctor that i think i s really cool to share.

if feature == "GitHub Fun Facts":
    st.header('Github Fun Facts!')
    st.subheader("Ever Wondered How Github benefits from Your Code?")
    st.caption("Many people (inlcuding me) wonder why Github just gives unlimited free public repositories. How do they make money?")
    with st.expander("Read the Article"):
        article()

if feature == "Repo Analytics":
    st.header("Repository Analytics")
    st.write("Analyze your Git repository statistics and insights.")
    
    repo_dir = st.text_input("Where's your project?", value=os.getcwd())
    
    if st.button("Analyze Repository"):
        try:
            if os.path.isdir(repo_dir):
                if check_git(repo_dir):
                    show_repo_analytics(repo_dir)
                else:
                    st.warning("Git isn't set up here yet.")
            else:
                st.error("That path doesn't seem to exist.")
        except Exception as e:
            st.error(f"Error analyzing repository: {e}")
    
    st.subheader("Here's what you'll see:")
    st.write("Total commits in your project")
    st.write("Most active contributor")
    st.write("File change statistics")
    st.write("Commit frequency over time")
