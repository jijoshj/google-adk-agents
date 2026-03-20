import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
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

root_agent = Agent(
    name="git_mcp_agent",
    model=MODEL,
    description="An agent that reads GitHub repositories using the GitHub MCP server.",
    instruction=f"""
    You are a GitHub repository reader and analyser.
    The GitHub username is: {GITHUB_USERNAME}
    You can help the user:
    - Read files from any of their GitHub repositories
    - List files and folder structures in a repo
    - Search for specific content like environment variables, config values, or code patterns
    - Summarise what a file or repo does
    Always clarify the repo name and file path if not provided by the user.
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