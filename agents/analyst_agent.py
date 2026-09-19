import os

from crewai import Agent, LLM
from tools.stock_research_tool import get_stock_price

GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/qwen/qwen3.8-27b")

# initialize the agent
llm = LLM(
    model=GROQ_MODEL,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=300,
)

# create an agent 
stock_analyst = Agent(
    # define the role and goal of the agent
    role = "your role is to be a stock analyst, you will provide stock information and analysis based on the user's queries." 
           " You will use the get_stock_price tool to fetch live stock information.",

    goal = "Your goal is to provide accurate and up-to-date stock information and analysis to the user based on their queries.",

    # define the backstory of the agent
    backstory = "You are a stock analyst with expertise in financial markets and stock analysis. " 
                "You have access to live stock information through the get_stock_price tool.",

    # define the llm for the agent
    llm = llm,

    # define the tools for the agent
    tools = [get_stock_price],

    # define the verbosity of the agent
    verbose = True
)