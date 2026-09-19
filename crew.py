from crewai import Crew

from tasks.trade_task import trade_decision
from tasks.analyze_agent import get_stock_analysis
from agents.analyst_agent import stock_analyst
from agents.traderagent import trader_agent

stock_crew = Crew(
    agents = [stock_analyst, trader_agent],
    tasks = [get_stock_analysis, trade_decision],
    verbose = True
)