import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()

# --- Model Configuration ---
# Option 1: Google Gemini (uncomment to use)
# MODEL = os.getenv("MODEL1", "gemini-2.5-flash")

# Option 2: Anthropic Claude via LiteLLM (active)
MODEL = LiteLlm(model=os.getenv("MODEL2", "anthropic/claude-sonnet-4-6"))

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

root_agent = Agent(
    name="langchain_tool_agent",
    model=MODEL,
    instruction="""You are a helpful assistant.
    Research the topic suggested by the user using Wikipedia and answer the question.""",
    description="Answers questions using Wikipedia",
    tools=[wikipedia_tool],
)