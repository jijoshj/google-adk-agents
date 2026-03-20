# 🤖 Google ADK Agents

A collection of AI agents built using [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/), powered by **Gemini 2.5 Flash**. Each agent demonstrates a different tool integration pattern — from custom Python functions to LangChain tools and MCP (Model Context Protocol) servers.

---

## 📁 Project Structure

```
AIAgents/
├── FirstAgent/                  # Greeting + Google Search agent
│   ├── __init__.py
│   └── agent.py
├── function_tool_agent/         # GitHub repo manager via Python functions
│   ├── __init__.py
│   └── agent.py
├── langchain_tool_agent/        # Wikipedia Q&A via LangChain tool
│   ├── __init__.py
│   └── agent.py
├── git_mcp_agent/               # GitHub repo reader via MCP server
│   ├── __init__.py
│   └── agent.py
├── .env                         # Environment variables (not committed)
├── .gitignore
└── requirements.txt
```

---

## 🧠 Agents Overview

### 1. `FirstAgent` — Greeting + Google Search
A simple agent that greets users by name and answers queries using Google Search.

**Tools used:**
- `morning_greet(name)` — custom Python function
- `evening_greet(name)` — custom Python function
- `google_search` — built-in ADK tool

**Run:**
```bash
adk web
# Select 'FirstAgent' in the UI
```

---

### 2. `function_tool_agent` — GitHub Repository Manager
An agent that creates and deletes GitHub repositories using the GitHub REST API via custom Python function tools.

**Tools used:**
- `create_github_repo(repo_name, description, private)` — custom Python function
- `delete_github_repo(repo_name)` — custom Python function

**Required env vars:**
```
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
```

**Run:**
```bash
adk web
# Select 'function_tool_agent' in the UI
```

---

### 3. `langchain_tool_agent` — Wikipedia Q&A
An agent that answers questions by searching Wikipedia, using a LangChain tool wrapped for ADK compatibility.

**Tools used:**
- `WikipediaQueryRun` via `LangchainTool` ADK adapter

**Run:**
```bash
adk web
# Select 'langchain_tool_agent' in the UI
```

---

### 4. `git_mcp_agent` — GitHub Repository Reader (MCP)
An agent that reads and analyses GitHub repositories using the official GitHub MCP (Model Context Protocol) server. Unlike `function_tool_agent`, this agent auto-discovers all available GitHub tools via the MCP protocol — no manual API calls needed.

**Tools used:**
- `@modelcontextprotocol/server-github` — GitHub MCP server via `npx`

**Required env vars:**
```
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
```

**Prerequisites:**
- Node.js (v18+) — [install via nvm](https://github.com/nvm-sh/nvm)

**Run:**
```bash
adk web
# Select 'git_mcp_agent' in the UI
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (for `git_mcp_agent`)
- A Google Gemini API key — [get one here](https://aistudio.google.com/apikey)
- A GitHub Personal Access Token — [generate here](https://github.com/settings/tokens)

### Installation

```bash
# Clone the repo
git clone https://github.com/jijoshj/google-adk-agents.git
cd google-adk-agents

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Model Configuration
# Option 1: Google Gemini (active)
MODEL1=gemini-2.5-flash

# Option 2: Anthropic Claude (uncomment to use)
# MODEL2=claude-sonnet-4-5
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Gemini
GOOGLE_API_KEY=your_gemini_api_key_here

# GitHub (required for function_tool_agent and git_mcp_agent)
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_personal_access_token
```

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## 🚀 Running the Agents

Start the ADK web interface from the project root:

```bash
cd google-adk-agents
source .venv/bin/activate
adk web
```

Open [http://localhost:8000](http://localhost:8000) in your browser, then select an agent from the dropdown.

---

## 🔧 Tool Integration Patterns

This project demonstrates three different ways to give an ADK agent tools:

| Pattern | Agent | Description |
|---|---|---|
| Custom Python functions | `FirstAgent`, `function_tool_agent` | Write plain Python functions, pass them as tools |
| LangChain tool adapter | `langchain_tool_agent` | Wrap any LangChain tool using `LangchainTool` |
| MCP server (Stdio) | `git_mcp_agent` | Connect to an MCP server running as a local subprocess |

---

## 🔄 Switching Models

To switch from Gemini to Claude across all agents:

1. Update `.env`:
```bash
# MODEL1=gemini-2.5-flash   ← comment this out
MODEL2=claude-sonnet-4-5    # ← uncomment this
ANTHROPIC_API_KEY=your_key
```

2. In each `agent.py`, comment out the Gemini line and uncomment the Claude line in the model configuration block.

---

## 📦 Dependencies

```
google-adk
google-generativeai
langchain-community==0.3.28
wikipedia==1.4.0
pandas==2.2.3
litellm==1.76.0
python-dotenv==1.0.1
requests>=2.32.5
```

---

## 📄 Licence

MIT
