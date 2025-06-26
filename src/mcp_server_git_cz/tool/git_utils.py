
import subprocess


def get_git_diff():
    """
    Gets the git diff for the current directory.
    It first tries to get the staged changes. If there are no staged changes,
    it gets all uncommitted changes.
    """
    try:
        # First, try to get staged changes
        staged_result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True
        )
        if staged_result.stdout.strip():
            return staged_result.stdout

        # If no staged changes, get all uncommitted changes
        all_changes_result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return all_changes_result.stdout

    except FileNotFoundError:
        # This case is unlikely if the script is run in a git repo
        return "Error: Git not found."
    except subprocess.CalledProcessError as e:
        return f"Error getting git diff: {e.stderr}"
