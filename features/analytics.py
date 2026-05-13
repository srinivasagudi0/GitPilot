import git
import streamlit as st

def show_repo_analytics(repo_dir):
    try:
        repo = git.Repo(repo_dir)
        
        # Total commits
        commits = list(repo.iter_commits())
        total_commits = len(commits)
        
        # Contributor states
        contributors_data = repo.git.shortlog('-sne').split('\n')
        contributors_list = [c.strip() for c in contributors_data if c.strip()]
        
        # File and code churn analysis
        try:
            file_changes = repo.git.diff('HEAD~1', '--name-status').split('\n')
            insertions = repo.git.log('-1', '--pretty=format:%i').strip()
            deletions = repo.git.log('-1', '--pretty=format:%d').strip()
        except:
            file_changes, insertions, deletions = [], 0, 0
        
        # Commit frequency analysis (last 30 days)
        commit_dates = repo.git.log('--pretty=format:%cd', '--date=short', '--since=30.days').split('\n')
        commit_freq = len([d for d in commit_dates if d.strip()])
        
        # Language detection
        languages = repo.git.ls_files('--stage').split('\n')
        
        # Now the easiest part - just display the stuff.
        st.subheader("Repo Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Commits", total_commits)
        col2.metric("Contributors", len(contributors_list))
        col3.metric("Recent Changes", len([f for f in file_changes if f.strip()]))
        col4.metric("30-Day Frequency", commit_freq)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Contributors")
            for contrib in contributors_list[:5]:
                st.text(contrib)
        
        with col2:
            st.subheader("Recent Activity")
            for date in commit_dates[:5]:
                if date.strip():
                    st.text(f"{date}")

    except Exception as e:
        st.error(f"Oops, Error analyzing repository: {e}; \nplease check the repo path and try again.")
