import os
from dotenv import load_dotenv
from google.adk.agents import Agent
# from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# --- Model Configuration ---
# Option 1: Google Gemini (uncomment to use)
# MODEL = os.getenv("MODEL1", "gemini-2.5-flash")

# Option 2: Anthropic Claude via LiteLLM (active)
MODEL = LiteLlm(model=os.getenv("MODEL2", "anthropic/claude-sonnet-4-6"))

def morning_greet(name: str) -> str:
    return f"Good Morning {name}"

def evening_greet(name: str) -> str:
    return f"Good Evening {name}"

root_agent = Agent(
    name="google_search_agent",
    model=MODEL,
    tools=[morning_greet, evening_greet],
    instruction="""
    First ask users name and greet them using users greet.
    If user says Good Morning or Good Evening, then use morning_greet or evening_greet to greet them respectively.
    After Greeting, answer the user query using google_search tool.
    """,
)