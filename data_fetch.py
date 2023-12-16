import yfinance as yf
# Fetch data from yfinance

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d')
    if not data.empty:
        return data['Close'].iloc[-1]
    return None

def get_stock_info(symbol):
    if symbol:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        return stock_info if stock_info else None
    return None




