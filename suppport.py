import os


def is_git_initialized(repo_dir):
    if not os.path.isdir(repo_dir):
        return False

    git_dir = os.path.join(repo_dir, ".git")
    return os.path.exists(git_dir)

