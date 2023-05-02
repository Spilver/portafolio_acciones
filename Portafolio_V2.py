
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import datetime as dt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
from yahoo_fin import stock_info as si
import plotly.graph_objects as go



def get_price(stock):
    try:
        return np.round(si.get_live_price(stock), decimals = 2)
    except:
        print(f"{stock.upper()} is not a valid ticker")


def get_data(stock, start, end):
    try:
        stock_data = pdr.data.DataReader(
            stock,
            "yahoo",
            start=start,
            end= end 
        )
        return stock_data["Adj Close"]
    except pdr._utils.RemoteDataError:
        print(f'No data found for {stock}.')



class Ledger:
    def __init__(self):
        self.transactions = {}
        self.holdings = {"USD": 0}
        
    def get_holdings(self):
        return self.holdings
    
    def get_transactions(self):
        return self.transactions


    def register_transaction(self, transaction, symbol, shares, price,date):
        pps = price
        total = pps*shares
        transaction_id = len(ledger.get_transactions())
        self.transactions.update({
               transaction_id: {
                    "type" : transaction,
                    "date": date,
                    "symbol": symbol.upper(),
                    "shares": shares,
                    "pps": pps,
                    "total" : total,
                } 
            })
        holdings = self.get_holdings()
        if transaction == "buy":
            if symbol in holdings.keys():
                holding = holdings[symbol]
                if holdings["USD"] > total:
                    holdings["USD"] -= total 
                else: 
                    holdings["USD"]
                holding["pps"] = (
                    (holding["pps"]*holding["shares"] + total) / 
                    (holding["shares"] + shares))
                holding["shares"] += shares
            else:
                holdings.update({
                    symbol: {
                        "shares": shares,
                        "pps": pps
                    }
                })
        if transaction == "sell":
            holding = holdings[symbol]
            holdings["USD"] += total
            holding["shares"] -= shares
            if holding["shares"] == 0:
                del holdings[symbol]
                
    def get_ts(self):
        def get_portfolio(portfolio, start, end):
            series = pd.Series(dtype="float64")
            for symbol in portfolio.keys():
                s = get_data(symbol, start, end) * portfolio[symbol]
                if symbol == "USD":
                    continue
                series = series.add(s, fill_value = 0)
            return series + portfolio["USD"]
        transactions = self.get_transactions()
        dates = [transactions[t]["date"] for t in transactions] + [dt.datetime.now().date().strftime("%Y-%m-%d")]
        portfolio = {"USD": 0}
        series = pd.Series(dtype="float64")
        for t in transactions:
            tr = transactions[t]
            adj = 0
            if tr["type"] == "buy":
                adj = -1*(tr["total"] if portfolio["USD"] > tr["total"]
                else portfolio["USD"])
                if tr["symbol"] in portfolio:
                    portfolio[tr["symbol"]] += tr["shares"] 
                else:
                    portfolio.update({tr["symbol"] : tr["shares"]})
            if tr["type"] == "sell":
                portfolio["USD"] += tr["total"]
                portfolio[tr["symbol"]] -= tr["shares"] 
            add = (tr["total"] - portfolio["USD"]) if tr["total"] > portfolio["USD"] else 0
            portfolio["USD"] += adj
            s = get_portfolio(portfolio, dates[t], dates[t+1])
            series = (series[:s.index[0]] + add).append(s) 

        return pd.Series([series.loc[x] 
             if isinstance(series.loc[x], np.float64) 
             else series.loc[x].values[0] for x in series.index.unique()],
                         index = series.index.unique())




ledger = Ledger()


ledger.register_transaction("buy", "VOO", 1, 328.93, "2020-09-09")
ledger.register_transaction("buy", "VTI", 1, 216.14, "2021-01-08")
ledger.register_transaction("buy", "ETH-USD", 0.102, 1305, "2021-01-31")
ledger.register_transaction("buy", "BTC-USD", 0.00179, 53269.2, "2021-03-26")
ledger.register_transaction("buy", "SKY", 2, 103.29, "2021-07-15")
ledger.register_transaction("buy", "BTC-USD", 0.0027, 45369.77, "2021-09-07")
ledger.register_transaction("buy", "BTC-USD", 0.00127, 51020.34, "2021-09-07")
ledger.register_transaction("buy", "ETH-USD", 0.03, 3542.71, "2021-09-07")
ledger.register_transaction("buy", "QQQ", 0.3415, 370.58, "2021-09-23")
ledger.register_transaction("buy", "BTC-USD", 0.00023, 58392.43, "2021-12-01")
ledger.register_transaction("buy", "VOO", 0.06, 424.17, "2021-12-01")

ledger.register_transaction("buy", "BTC-USD", 0.00179, 53398, "2021-12-03")
ledger.register_transaction("buy", "ETH-USD", 0.0278, 4314, "2021-12-03")


ledger.register_transaction("buy", "VOO", 0.06, 421.73, "2022-01-10")
ledger.register_transaction("buy", "ETH-USD", 0.0295, 3044.05, "2022-01-10")
#antm no esta en yahoo finance
#ledger.register_transaction("buy", "ANTM", 0.27, 451.9, "2022-01-19")
ledger.register_transaction("buy", "ETH-USD", 0.041007, 2803.63, "2022-01-21")
ledger.register_transaction("buy", "VOO", 0.474, 391.58, "2022-03-11")
ledger.register_transaction("buy", "MSFT", 0.065, 282.21, "2022-03-14")
ledger.register_transaction("buy", "QQQ", 0.5744, 321.65, "2022-03-14")
ledger.register_transaction("buy", "NVDA", 0.778, 241.19, "2022-04-06")
ledger.register_transaction("buy", "SOL-USD", 1, 121.2, "2022-04-07")
ledger.register_transaction("buy", "VOO", 0.30, 406.78, "2022-04-12")
ledger.register_transaction("buy", "NVDA", 0.55, 223.93, "2022-04-12")
ledger.register_transaction("buy", "GOOGL", 0.07, 2608.57, "2022-04-12")
ledger.register_transaction("buy", "VYM", 0.532, 114.78, "2022-04-20")
ledger.register_transaction("buy", "VYM", 0.539, 109.31, "2022-04-27")
ledger.register_transaction("buy", "BRK-B", 0.18, 331.71, "2022-04-27")
ledger.register_transaction("sell", "SKY", 2, 67.1, "2022-05-9")
ledger.register_transaction("buy", "ETH-USD", 0.034714, 1689.11, "2022-06-10")




holdings = ledger.get_holdings()
df = pd.DataFrame(holdings).transpose()
df["pps"].loc["USD"] = 1
df["current_price"] = [df.pps.loc["USD"]] + [get_price(x) for x in df.index[1:]]
df["equity"] = df.current_price * df.shares
df["total_cost"] = df.shares * df.pps


df["return"] = np.round(((df.current_price - df.pps)/ df.pps)*100, decimals = 4)
print(df)

def sp500():
    ts = ledger.get_ts()
    spy = get_data("SPY", ts.index[0], ts.index[-1])
    ts = ts[ts.index.isin(spy.index)]
    df = pd.DataFrame({"Portfolio" : ts.values, "SPY" : spy[ts.index[0]:].values}, index = spy.index)
    df.Portfolio = np.round((df.Portfolio - df.Portfolio[0]) / df.Portfolio[0], decimals = 4)
    df.SPY = np.round((df.SPY - df.SPY[0]) / df.SPY[0], decimals = 4)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = df.index, 
        y = df.Portfolio,
        mode = "lines",
        name = "Portfolio"
    ))
    fig.add_trace(go.Scatter( 
        x = df.index, 
        y = df.SPY,
        mode = "lines",
        name = "SPY"
    ))
    fig.update_layout(
        title = {
            "text" : f'Portfolio Performance',
            "y": .9,
            "x": .05,
            "xanchor": "left",
            "yanchor": "middle"
        },
        template = "plotly_dark",
        margin = dict(l = 60, t = 80, r = 60, b = 60),
        height = 500
    )
    fig.show()


def torta():
    fig = go.Figure(data = [
        go.Pie(
            values = df.equity, 
            labels = df.index,
            textposition = "inside", 
            textinfo = "percent+label",
            textfont_color = "#111111",
        )])
    fig.update_layout(
        template = "plotly_dark",
        title = {
            "text" : "Portfolio Holdings",
            "y" : .875,
            "x" : .05,
            "xanchor" : "left",
            "yanchor" : "bottom"
        },
        margin = dict(l = 60, t = 40, r = 60, b = 40),
        legend = dict(
            yanchor = "middle", 
            y = .5, 
            xanchor = "left", 
            x = .875)
    )
    fig.show()

def radar():
    fig = go.Figure(data = go.Scatterpolar(
        r = df["return"][1:].values,
        theta = df.index[1:],
        fill = 'toself',
    ))
    fig.update_layout(
        polar = dict(radialaxis = dict(visible = True)), 
        margin = dict(l = 40, t = 40, r = 40, b = 40),
        template = "plotly_dark",
        title = {
            "text" : "Individual Asset Returns",
            "y" : .875,
            "x" : .05,
            "xanchor" : "left",
            "yanchor" : "bottom"
        },
    )
    fig.show()

def transactions():
    transactions = ledger.get_transactions()
    df = pd.DataFrame(transactions).transpose()
    df.loc[df.type == "sell", "total"] = df.loc[df.type == "sell", "total"] * -1
    print(df)

def trading():
    transactions = ledger.get_transactions()
    df = pd.DataFrame(transactions).transpose()
    df.loc[df.type == "sell", "total"] = df.loc[df.type == "sell", "total"] * -1
    fig = go.Figure([
          go.Bar(
            x = df.symbol, 
            y = df.total,
            text = df.date,
            meta = df.shares,
            customdata = df.pps,
            marker_color= ["green" if x == "buy" else "red" for x in df.type],
            hovertemplate = ("Total: $%{y:,.2f}" +
                             "<br>Shares: %{meta}" +
                             "<br>PPS: $%{customdata:,.2f}" + 
                             "<br>Date: %{text}"))
        ],
    )
    fig.update_layout(
        template = "plotly_dark",
        title = {
            "text" : "Trading Activity",
            "y" : .9,
            "x" : .5,
            "xanchor" : "center",
            "yanchor" : "middle",
        },
        height = 400,
        margin = dict(t = 60, l = 60, r = 40, b = 40)
    )
    fig.show()

x = ""
while(x != 9):
    x = int(input("Ingresa un numero: 1 torta,  2 radar,   3 transacciones,    4 actividad trading,    5 comparacion sp500,     9 salir\n"))
    if (x == 1):
        torta()
    elif (x == 2):
        radar()
    elif (x == 3):
        transactions()
    elif (x == 4):
        trading()
    elif (x == 5):
        sp500()





