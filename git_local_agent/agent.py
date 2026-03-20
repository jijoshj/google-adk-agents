import os
import subprocess
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# --- Model Configuration ---
# Option 1: Google Gemini (uncomment to use)
# MODEL = os.getenv("MODEL1", "gemini-2.5-flash")

# Option 2: Anthropic Claude via LiteLLM (active)
MODEL = LiteLlm(model=os.getenv("MODEL2", "anthropic/claude-sonnet-4-6"))

# Path to the AIAgents project
REPO_PATH = "/Users/jijoshjoshua/Desktop/AIAgents"


def _run(cmd: list) -> str:
    """Internal helper to run a shell command in the repo directory."""
    try:
        result = subprocess.run(
            cmd,
            cwd=REPO_PATH,
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        if result.returncode != 0:
            return f"ERROR: {error or output}"
        return output or "Command completed successfully."
    except Exception as e:
        return f"Exception: {str(e)}"


def git_status() -> str:
    """Returns the current git status of the repository showing staged,
    unstaged, and untracked files."""
    return _run(["git", "status"])


def git_log(max_count: int = 10) -> str:
    """Returns the recent git commit history.
    Args:
        max_count: Number of recent commits to show. Defaults to 10.
    """
    return _run([
        "git", "log",
        f"--max-count={max_count}",
        "--oneline",
        "--decorate"
    ])


def git_diff(staged: bool = False) -> str:
    """Shows the diff of changes in the repository.
    Args:
        staged: If True, shows diff of staged changes. If False, shows
        unstaged changes.
    """
    cmd = ["git", "diff"]
    if staged:
        cmd.append("--staged")
    return _run(cmd)


def git_add(files: str = ".") -> str:
    """Stages files for commit.
    Args:
        files: Files to stage. Use '.' to stage all changes, or provide
        specific file paths separated by spaces e.g. 'README.md agent.py'.
    """
    return _run(["git", "add"] + files.split())


def git_commit(message: str) -> str:
    """Commits staged changes with a message.
    Args:
        message: The commit message describing the changes.
    """
    return _run(["git", "commit", "-m", message])


def git_push(remote: str = "origin", branch: str = "main") -> str:
    """Pushes committed changes to the remote repository.
    Args:
        remote: The remote name to push to. Defaults to 'origin'.
        branch: The branch name to push to. Defaults to 'main'.
    """
    return _run(["git", "push", remote, branch])


def git_pull(remote: str = "origin", branch: str = "main") -> str:
    """Pulls latest changes from the remote repository.
    Args:
        remote: The remote name to pull from. Defaults to 'origin'.
        branch: The branch name to pull from. Defaults to 'main'.
    """
    return _run(["git", "pull", remote, branch])


def git_branch_list() -> str:
    """Lists all local and remote branches in the repository."""
    return _run(["git", "branch", "-a"])


def git_branch_create(branch_name: str) -> str:
    """Creates a new git branch.
    Args:
        branch_name: The name of the new branch to create.
    """
    return _run(["git", "checkout", "-b", branch_name])


def git_branch_switch(branch_name: str) -> str:
    """Switches to an existing git branch.
    Args:
        branch_name: The name of the branch to switch to.
    """
    return _run(["git", "checkout", branch_name])


def git_branch_delete(branch_name: str) -> str:
    """Deletes a local git branch.
    Args:
        branch_name: The name of the branch to delete.
    """
    return _run(["git", "branch", "-d", branch_name])


root_agent = Agent(
    name="git_local_agent",
    model=MODEL,
    description="An agent that manages local git operations for the AIAgents project.",
    tools=[
        git_status,
        git_log,
        git_diff,
        git_add,
        git_commit,
        git_push,
        git_pull,
        git_branch_list,
        git_branch_create,
        git_branch_switch,
        git_branch_delete,
    ],
    instruction=f"""
    You are a local Git management assistant for the AIAgents project located at {REPO_PATH}.

    You help the user manage their git repository by running git operations on their behalf.

    Available operations:
    - Check repository status and recent history
    - Stage files for commit
    - Commit changes with meaningful messages
    - Push and pull from remote
    - Create, switch, list and delete branches
    - Show diffs of changes

    Important rules:
    - Always run git_status first before any commit or push operation
    - Always show the user what files are staged before committing
    - Never commit without a meaningful commit message - suggest one if the user doesn't provide one
    - Never push without confirming with the user first
    - Never delete a branch without explicit user confirmation
    - If git_diff shows a lot of changes, summarise them for the user before committing
    - Follow conventional commit message format: feat:, fix:, docs:, refactor:, chore: etc.

    Typical workflow you should follow:
    1. git_status → show what has changed
    2. git_diff → summarise the changes if needed
    3. git_add → stage the files
    4. git_commit → commit with a meaningful message
    5. git_push → push to remote after user confirms
    """,
)