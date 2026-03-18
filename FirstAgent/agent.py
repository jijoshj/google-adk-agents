from google.adk.agents import Agent
from google.adk.tools import google_search

def morning_greet(name:str) -> str:
    return f"Good Morning {name}"

def evening_greet(name:str) -> str:
    return f"Good Evening {name}"

root_agent = Agent(
    name="google_search_agent",
    model="gemini-2.5-flash",
    tools=[morning_greet, evening_greet],
    instruction="""


    First ask users name and greet them using users greet.

    If user says Good Morning or Good Evening, then use morning_greet or evening_greet to greet them respectively.

    After Greeting, answer the user query using google_search tool.
    
    """,
)