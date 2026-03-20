import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
NPX_PATH = "/Users/jijoshjoshua/.nvm/versions/node/v24.14.0/bin/npx"
MODEL = os.getenv("MODEL2", "claude-sonnet-4-5-20251001")

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

    When asked to find environment variables in a file or repo, look for:
    - os.getenv(...) calls
    - os.environ.get(...) calls
    - load_dotenv() usage
    - Any .env references

    Always clarify the repo name and file path if not provided by the user.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=NPX_PATH,
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-github",
                    ],
                    env={
                        "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
                    }
                ),
                timeout=30.0
            )
        )
    ]
)