from crewai import Task
from agents.analyst_agent import stock_analyst

get_stock_analysis = Task(
    agent=stock_analyst,
    description=(
        "Please provide me with the current stock price and analysis for {stock}. "
        "Analyze the stock's performance, recent news, and any relevant financial metrics to give a "
        "comprehensive overview of the stock's current status and potential future trends."
    ),

    expected_output=(
    "a clear bullet point summary of the stock's current price"
    "daily price change and performance,"
    "volume and volatility metrics,"
    ),
)