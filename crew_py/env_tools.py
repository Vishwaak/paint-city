
from dotenv import load_dotenv
load_dotenv()
import os



from langchain_community.tools import DuckDuckGoSearchRun
from crewai_tools import DirectorySearchTool
from crewai.tools import tool


model_tools = [DuckDuckGoSearchRun(),DirectorySearchTool()]



@tool('DuckDuckGoSearch')
def model_tools(search_query: str):
    """
    Function to get the browserbase tool for internet searching capabilities.
    """
    return DuckDuckGoSearchRun().run(search_query)



