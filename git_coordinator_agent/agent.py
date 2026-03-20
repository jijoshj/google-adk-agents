import os
import subprocess
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

# --- Model Configuration ---
# Option 1: Google Gemini (uncomment to use)
# MODEL = os.getenv("MODEL1", "gemini-2.5-flash")

# Option 2: Anthropic Claude via LiteLLM (active)
MODEL = LiteLlm(model=os.getenv("MODEL2", "anthropic/claude-sonnet-4-6"))

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
NPX_PATH = "/Users/jijoshjoshua/.nvm/versions/node/v24.14.0/bin/npx"
REPO_PATH = "/Users/jijoshjoshua/Desktop/AIAgents"


# ─────────────────────────────────────────
# Local Git tools (from git_local_agent)
# ─────────────────────────────────────────

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
    return _run(["git", "log", f"--max-count={max_count}", "--oneline", "--decorate"])


def git_diff(staged: bool = False) -> str:
    """Shows the diff of changes in the repository.
    Args:
        staged: If True, shows diff of staged changes. If False, shows unstaged changes.
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
    """Creates a new git branch and switches to it.
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


# ─────────────────────────────────────────
# Sub-agent: git_mcp_agent (remote GitHub reader)
# ─────────────────────────────────────────

git_mcp_sub_agent = Agent(
    name="git_mcp_sub_agent",
    model=MODEL,
    description="""A specialist agent that reads and analyses GitHub repositories
    remotely using the GitHub MCP server. Use this agent for:
    - Reading file contents from GitHub repos
    - Listing files and folder structures
    - Searching for code patterns or content
    - Getting repo information and metadata
    - Comparing remote vs local changes
    """,
    instruction=f"""
    You are a GitHub repository reader. The GitHub username is: {GITHUB_USERNAME}
    Read files, list structures, and search content in GitHub repositories.
    Always clarify the repo name and file path if not provided.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=NPX_PATH,
                    args=["-y", "@modelcontextprotocol/server-github"],
                    env={"GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN}
                ),
                timeout=30.0
            )
        )
    ]
)


# ─────────────────────────────────────────
# Coordinator agent
# ─────────────────────────────────────────

root_agent = Agent(
    name="git_coordinator_agent",
    model=MODEL,
    description="A coordinator agent that manages both local git operations and remote GitHub reading.",
    tools=[
        # Remote GitHub reading via MCP
        AgentTool(agent=git_mcp_sub_agent),
        # Local git operations via Python functions
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
    You are a powerful Git coordinator assistant for the AIAgents project at {REPO_PATH}.

    You have two sets of capabilities:

    1. LOCAL GIT OPERATIONS (direct tools):
       - Check status, logs, diffs
       - Stage, commit, push, pull
       - Create, switch, delete branches

    2. REMOTE GITHUB READING (via git_mcp_sub_agent):
       - Read file contents from GitHub
       - List repo structure
       - Search code and content
       - Get repo metadata

    Routing rules:
    - User asks to READ from GitHub → delegate to git_mcp_sub_agent
    - User asks to PUSH, COMMIT, STAGE, PULL → use local git tools directly
    - User asks to do BOTH (e.g. read a file then update it) → use both in sequence

    Always follow this workflow for commits and pushes:
    1. git_status → show what has changed
    2. git_diff → summarise changes if needed
    3. git_add → stage files
    4. git_commit → commit with a conventional message (feat:, fix:, docs:, chore:)
    5. git_push → only after user confirms

    Never push without user confirmation.
    Never delete a branch without explicit user confirmation.
    """,
)