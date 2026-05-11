import os


def is_git_initialized(repo_dir):
    if not os.path.isdir(repo_dir):
        return False

    git_dir = os.path.join(repo_dir, ".git")
    return os.path.exists(git_dir)


def summarize_git_status(status_output):
    if not status_output or not status_output.strip():
        return "No status output available."

    lowered = status_output.lower()
    if "nothing to commit" in lowered and "working tree clean" in lowered:
        return "Working tree clean. No changes to commit."

    counts = {
        "modified": 0,
        "new": 0,
        "deleted": 0,
        "renamed": 0,
        "untracked": 0,
    }

    in_untracked = False
    for raw_line in status_output.splitlines():
        line = raw_line.strip()
        if not line:
            in_untracked = False
            continue

        if line.startswith("Untracked files:"):
            in_untracked = True
            continue

        if in_untracked:
            if line.startswith("("):
                continue
            counts["untracked"] += 1
            continue

        if line.startswith("modified:"):
            counts["modified"] += 1
        elif line.startswith("new file:"):
            counts["new"] += 1
        elif line.startswith("deleted:"):
            counts["deleted"] += 1
        elif line.startswith("renamed:"):
            counts["renamed"] += 1

    summary_parts = []
    if counts["modified"]:
        summary_parts.append(f'{counts["modified"]} modified')
    if counts["new"]:
        summary_parts.append(f'{counts["new"]} new')
    if counts["deleted"]:
        summary_parts.append(f'{counts["deleted"]} deleted')
    if counts["renamed"]:
        summary_parts.append(f'{counts["renamed"]} renamed')
    if counts["untracked"]:
        summary_parts.append(f'{counts["untracked"]} untracked')

    if not summary_parts:
        return "Changes detected, but no file details were found."

    return "Changes: " + ", ".join(summary_parts) + "."
