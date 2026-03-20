import os
import requests
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables from a .env file if it exists
load_dotenv()

# Replace these with your actual GitHub credentials or load them via .env
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "<YOUR_GITHUB_USERNAME>")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>")
GITHUB_API_URL = "https://api.github.com"

MODEL = os.getenv("MODEL2", "claude-sonnet-4-5-20251001")

def create_github_repo(repo_name: str, description: str = "", private: bool = False) -> str:
    """Creates a new GitHub repository for the authenticated user.
    Args:
        repo_name: The name of the new repository.
        description: A short description of the repository.
        private: Either true to create a private repository or false to create a public one.
    """
    url = f"{GITHUB_API_URL}/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": private
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return f"Successfully created repository: {repo_name} at {response.json().get('html_url')}"
    else:
        return f"Failed to create repository. Status: {response.status_code}, Response: {response.text}"

def delete_github_repo(repo_name: str) -> str:
    """Deletes an existing GitHub repository for the authenticated user.
    Args:
        repo_name: The exact name of the repository to delete.
    """
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{repo_name}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        return f"Successfully deleted repository: {repo_name}"
    else:
        return f"Failed to delete repository. Status: {response.status_code}, Response: {response.text}"


root_agent = Agent(
    name="github_manager_agent",
    model=MODEL,
    description="An agent that manages a user's GitHub repositories.",
    tools=[create_github_repo, delete_github_repo],
    instruction='''
    You are a GitHub management assistant. Your job is to help the user create and delete GitHub repositories.
    
    - Always confirm the exact name of the repository the user wants to interact with.
    - If they ask to create a repository, use the `create_github_repo` tool.
    - If they ask to delete a repository, use the `delete_github_repo` tool.
    
    **WARNING**: Deleting a repository is a destructive action. Never delete a repository unless the user explicitly and clearly confirms they want to delete it.
    ''',
)
