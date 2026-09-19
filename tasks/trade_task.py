from crewai import Task
from agents.traderagent import trader_agent

trade_decision = Task(
    agent=trader_agent,
    description=(
        "Please provide me with a trading recommendation for {stock}. "
        "Analyze the stock's current price, recent news, and any relevant financial metrics to give a "
        "comprehensive overview of its current status and potential future trends. "
        "Based on your analysis, please provide a clear recommendation on whether to buy, sell, or hold."
    ),

    expected_output = (
        "a clear bullet point summary of the stock's current price"
        "daily price change and performance,"
        "volume and volatility metrics,"
        "and a clear recommendation on whether to buy, sell, or hold the stock."
    )
)