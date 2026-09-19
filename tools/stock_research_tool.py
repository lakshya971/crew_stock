import yfinance as yf
from crewai.tools import tool


@tool("Live stock information tool")

def get_stock_price(stock_symbol: str) -> str:
    """
    Get the current stock price for a given stock symbol.

    Returns:
        str: The current stock price for the given stock symbol.
    """

    # this will fetch the stock data from Yahoo Finance using the yfinance library
    stock = yf.Ticker(stock_symbol)

    # get the stock info 
    info = stock.info

    # extract the current price, change, and change percent from the info dictionary
    current_price = info.get("regularMarketPrice", None)
    change = info.get("regularMarketChange", None)
    change_percent = info.get("regularMarketChangePercent", None)
    currency = info.get("currency", "USD")

    # check if the current price is None, if so return an error message
    if current_price is None:
        return f"Could not retrieve stock price for {stock_symbol}. Please check the stock symbol and try again."

    # format the output string with correct current price, change, and change percent
    return (
        f"stock:{stock_symbol.upper()}\n"
        f"current price: {current_price} {currency}\n"
        f"change: {change} ({round(change_percent, 2)}%)"

    )

# print(get_stock_price("AAPL"))  # Example usage

