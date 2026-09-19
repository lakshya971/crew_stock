import os

from crewai import Agent, LLM
from tools.stock_research_tool import get_stock_price

GROQ_MODEL = os.getenv("GROQ_MODEL", "groq/qwen/qwen3.8-27b")

llm = LLM(
    model=GROQ_MODEL,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=300,
)

trader_agent = Agent(
    role = (
        "Your role is to be a stock trader, you will provide stock trading advice and analysis based on the user's queries." 
        "You will use the get_stock_price tool to fetch live stock information and provide trading recommendations."
    ),


    goal = (
        "Your goal is to provide accurate and up-to-date stock trading advice and analysis to the user based on their queries."
        "You will use the get_stock_price tool to fetch live stock information and provide trading recommendations."
    ),

    backstory = (
        "You are a stock trader with expertise in financial markets and stock trading. "
        "You have access to live stock information through the get_stock_price tool and will provide trading recommendations based on the user's queries."
    ),

    llm = llm,
    tools = [get_stock_price],
    verbose = True
)