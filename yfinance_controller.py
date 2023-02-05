import yfinance as yf
import datetime

class YFinanceController():

    # ONLY accept stock for now
    def get_extreme_stock_price(self, from_date, stock, action):
        num_days = (datetime.datetime.now() - datetime.datetime.strptime(from_date, "%Y-%m-%d")).days
        num_days_str = str(num_days) + "d"
        data = yf.download(tickers=stock, period=num_days_str, interval="1d")   
        if action == 'BUY':
            return data['Close'].max()
        elif action == 'SELL':
            return data['Close'].min()
    
    
    def get_current_stock_price(self, stock):
        data = yf.Ticker(stock).history()['Close'].iloc[-1]
        return data

# yfc = YFinanceController()
# print(yfc.get_current_stock_price('None'))