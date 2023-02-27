import yfinance as yf
import datetime

class YFinanceController():

    # ONLY accept stock for now
    def get_extreme_stock_price(self, from_date, stock, qty):
        num_days = (datetime.datetime.now() - datetime.datetime.strptime(from_date, "%Y-%m-%d")).days
        num_days_str = str(num_days) + "d"
        data = yf.download(tickers=stock, period=num_days_str, interval="1d")   
        if qty > 0:
            return data['Close'].max()
        elif qty < 0:
            return data['Close'].min()
    
    
    def get_current_stock_price(self, stock):
        data = yf.Ticker(stock).history()['Close'].iloc[-1]
        return data

if __name__ == "__main__":    
    yfc = YFinanceController()
    print(yfc.get_extreme_stock_price('2023-01-01', 'TSLA', 200))
