import os
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Create the LangChain Wikipedia tool wrapped for ADK
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

root_agent = Agent(
    name="langchain_tool_agent",
    model=os.getenv("MODEL_NAME", "gemini-2.5-flash"),
    instruction="""You are a helpful assistant. 
    Research the topic suggested by the user using Wikipedia and 
    answer the question.""",
    description="Answers questions using Wikipedia",
    tools=[wikipedia_tool],
)
