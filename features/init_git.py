import git


def initialize_git(repo_dir):
    git.Repo.init(repo_dir)
    
