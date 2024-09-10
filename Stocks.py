import yfinance
import datetime
from urllib.parse import unquote

def getTickerInfo(ticker): #Disabled Caching so most up-to-date information is always retrieved
    print("Getting real response for ticker %s" % ticker)
    return getTickerInfoReal(ticker)

def getTickerInfoReal(tickerName):
    ticker = yfinance.Ticker(tickerName)
    info = ticker.info
    if not info:
        return None
        
    data = ticker.history(period='5d')
    open_price = data['Open'].iloc[0]
    current_price = data['Close'].iloc[-1]
    previous_close = data['Close'].iloc[-2]
    percentage_difference = ((current_price - previous_close) / previous_close) * 100
    price_change = current_price - previous_close
    
    
    info.update({"Open": float(open_price)})
    info.update({"currentPrice": float(round(current_price, 2))})
    info.update({"changepercent": float(round(price_change, 2)), "change": float(round(percentage_difference, 2))})
    
    
    info.update({"timestamp": datetime.datetime.now().strftime("%h")})
    info["noopen"] = False
    if not "open" in info:
        if 'regularMarketOpen' not in info:
            info["noopen"] = True
        else:
            info['open'] = info['regularMarketOpen']
    if not "volume" in info:
        info["volume"] = 0
    if not "marketCap" in info:
        info["marketCap"] = 0
    if not "dividendYield" in info:
        info["dividendYield"] = 0
    #print(info)
    return info

def sanitizeSymbol(s):
    return unquote(s)

def getTickerChartForRange(ticker, range):
    match range:
        case "1d":
            interval = "15m"
        case "5d":
            range = "5d"
            interval = "5m"
        case "1m":
            range = "1mo"
            interval = "1d"
        case "3m":
            range = "3mo"
            interval = "1d"
        case "6m":
            range = "6mo"
            interval = "1wk"
        case "1y":
            interval = "1wk"
        case "2y":
            interval = "1wk"
        case "5y":
            interval = "1wk"
        case "10y":
            interval = "1wk"
        case _:
            print("Unknown range: " + range)
            return None

    print("Interval = " + interval + " for range " + range)
    data_dict = yfinance.Ticker(ticker).history(period=range, interval=interval).to_dict()

    # Create the output data
    out = [{"open": data_dict["Open"][key], "high": data_dict["High"][key], "low": data_dict["Low"][key],
            "close": data_dict["Close"][key], "volume": data_dict["Volume"][key], "timestamp": key.timestamp()} for key
           in data_dict["Open"].keys()]

    return out
