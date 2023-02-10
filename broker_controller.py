from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key

from tigeropen.trade.trade_client import TradeClient
from tigeropen.common.util.contract_utils import stock_contract, option_contract_by_symbol
from tigeropen.common.util.order_utils import market_order, limit_order

from tigeropen.quote.quote_client import QuoteClient
from prettytable import PrettyTable
from datetime import datetime, date, timedelta
import pandas as pd

from yfinance_controller import YFinanceController
from db_controller import DbController

class BrokerController():
    def __init__(self, sandbox=False):
        self._client_config = TigerOpenClientConfig(sandbox_debug=sandbox)
        # client_config.private_key = read_private_key('path of rsa private key')
        
        '''PAPER ACC'''
        self._client_config.private_key = "MIICXQIBAAKBgQDJ5SnACzP/YeWp2Sd3nDFmT4zmZfr/9/PDi+q7wYPUJBbJ4OsA7tcBduCAwPqLjEPKZ4aO46QfUAzqRH1b7Hlp9JgPn2EykL11lKjbQxjy3itx8IyiGiaU/O+nZtNWWJtGWkmphwnJAroopXtO6c69AH3pwrfokloQlfeRiZIAYQIDAQABAoGBAKBWZXzFqOrlhW4JLkXYfobhIGYNkXPdJ/MhWC76NUaxzoNPI3MfOxNHpG28VH2kzGWfKAaslLflbAxUjjYFrDlnQ+by+05gNWSeEibkKUH8ooIu1NXhAyqwTDn46OJd50lAMrDynns3EOb7982+p29dAAm7q3cmieki8xjI18cBAkEA55lH/Sq1446NnHDll7ucJsBPDiLRxOwa3d1MjKj3OfDefV3TuQWP/9hih4pQP+PnB0x6BvvZetUOrsDVr4Gk8QJBAN8qtkQ7NknRc/dg7pmLLf2hKJLYND2sQZvjJkLz5ro9Hi3zd9o6M1jjdzU/NRTLGwxsSMY4W8sBScAUfJazUnECQE8aG2xs2hMO7W8xYDmi6oKRzG6Xle4cdlCw9SRV0ZsImfVXxqi7LaPE1GJW63Hm9VGY3VTlUDKT8p/dXR7EuQECQGka4rEL+iuWHDn8SyPBqy1zA3r1nNUXFednehO6b4ZzVo1px57eHmTU7MYFOOjMJ7cYIMZKsODRgHyYqX0Ig+ECQQDeqwc6WsfeQ9QOW9du0ObgI5PCuDz6ybp773sgAaegai+bQjVNEDReYM2DqpIDEyTmRs6Nd6CgIW+eual8Kar8"
        self._client_config.tiger_id = '20151980'
        self._client_config.account = '20221219001727127' 
        '''ACTUAL ACC'''
        # self._client_config.private_key = "MIICXQIBAAKBgQDJ5SnACzP/YeWp2Sd3nDFmT4zmZfr/9/PDi+q7wYPUJBbJ4OsA7tcBduCAwPqLjEPKZ4aO46QfUAzqRH1b7Hlp9JgPn2EykL11lKjbQxjy3itx8IyiGiaU/O+nZtNWWJtGWkmphwnJAroopXtO6c69AH3pwrfokloQlfeRiZIAYQIDAQABAoGBAKBWZXzFqOrlhW4JLkXYfobhIGYNkXPdJ/MhWC76NUaxzoNPI3MfOxNHpG28VH2kzGWfKAaslLflbAxUjjYFrDlnQ+by+05gNWSeEibkKUH8ooIu1NXhAyqwTDn46OJd50lAMrDynns3EOb7982+p29dAAm7q3cmieki8xjI18cBAkEA55lH/Sq1446NnHDll7ucJsBPDiLRxOwa3d1MjKj3OfDefV3TuQWP/9hih4pQP+PnB0x6BvvZetUOrsDVr4Gk8QJBAN8qtkQ7NknRc/dg7pmLLf2hKJLYND2sQZvjJkLz5ro9Hi3zd9o6M1jjdzU/NRTLGwxsSMY4W8sBScAUfJazUnECQE8aG2xs2hMO7W8xYDmi6oKRzG6Xle4cdlCw9SRV0ZsImfVXxqi7LaPE1GJW63Hm9VGY3VTlUDKT8p/dXR7EuQECQGka4rEL+iuWHDn8SyPBqy1zA3r1nNUXFednehO6b4ZzVo1px57eHmTU7MYFOOjMJ7cYIMZKsODRgHyYqX0Ig+ECQQDeqwc6WsfeQ9QOW9du0ObgI5PCuDz6ybp773sgAaegai+bQjVNEDReYM2DqpIDEyTmRs6Nd6CgIW+eual8Kar8"
        # self._client_config.tiger_id = '20151980'
        # self._client_config.account = '50971581' 

        self._client_config.timezone = 'US/Eastern' # default timezone 

        self._trade_client = TradeClient(self._client_config)
        self._quote_client = QuoteClient(self._client_config)
        self._yfc = YFinanceController()
        self._dbc = DbController()



    def convert_pretty_table(self, data):
        
        table = PrettyTable()
        table.field_names = data[0].keys()

        for item in data:
            table.add_row(item.values())

        return table
        

    def get_extreme_option_price(self, purchase_date, contract, qty):

        dt = datetime.strptime(str(purchase_date), "%Y-%m-%d %H:%M:%S")
        purchase_date_unix = int(dt.timestamp() * 1000)
        df = self._quote_client.get_option_bars([contract])
        if qty > 0:
            extreme_price = df.loc[df['time'] > purchase_date_unix, 'close'].max()
        elif qty < 0:
            extreme_price = df.loc[df['time'] > purchase_date_unix, 'close'].min()
        return extreme_price

    def get_current_option_price(self, identifier):
        opt = self._quote_client.get_option_briefs([identifier])
        return opt['latest_price'].iloc[0]
    
    def get_time_segments_for_filled_orders (self):    
        start_date = date(2021, 5, 1)
        end_date = datetime.now().date()
        max_segment_length = 90
        segments = []
        current_start_date = start_date
        while current_start_date <= end_date:
            current_end_date = current_start_date + timedelta(days=max_segment_length - 1)
            if current_end_date > end_date:
                current_end_date = end_date

            segments.append((str(current_start_date), str(current_end_date)))

            current_start_date = current_end_date + timedelta(days=1)
        return segments

    
    # TODO: doing now
    def get_my_recommended_actions(self, positions):
        for pos in positions:
            price = pos.get('price')
            cost = pos.get('cost')
            qty = pos.get('qty')
            contract = pos.get('contract')
            identifier = contract.split('/')[0]
            contract_type = pos.get('contract').split('/')[1]
            pl_perc = pos.get('pl_perc')
            entered_date = self._dbc.run_query(f"select entered_date from tbl where contract = '{contract}'")
            if entered_date is None:
                entered_date = {datetime.now().date()}
                self._dbc.run_dml(f"INSERT INTO tbl VALUES ('{contract}','{datetime.now().date()}','{datetime.now().date()}')")
            else:
                entered_date = entered_date[0]
                self._dbc.run_dml(f"update tbl set last_updated_date = '{datetime.now().date()}' where contract = '{contract}'")

            self._dbc.run_dml(f"delete from tbl where last_updated_date < '{datetime.now().date()}'")

            if contract_type == 'STK':
                max_profit_price = self._yfc.get_extreme_stock_price(entered_date, identifier, qty)
            elif contract_type == 'OPT':
                max_profit_price = self.get_extreme_option_price(entered_date, identifier, qty)
            
            if qty > 0:
                pos['stop_loss'] = round(cost * 0.95,2)
                target_profit_taking_price = (max_profit_price - price) * 0.7 + price
            elif qty < 0:
                pos['stop_loss'] = round(cost * 1.05, 2)
                target_profit_taking_price = price - (price - max_profit_price) * 0.7

            pos['max_profit_px'] = round(max_profit_price, 2)
            pos['recommendation'] = None
            pos['reason'] = None

            if qty < 0:
                action = 'BUYBACK'
            else:
                action = 'SELL'
            # stop loss R
            
            if pl_perc < -5:
                pos['recommendation'] = f"{action} {qty} {identifier} {contract_type}"
                pos['reason'] = "loss of > 5%"
            # exit when profit >2R  + retraced 30 percent from high - IF ALL TIME HIGH + profit 2R --> FIX stop loss value -- write in gsheets?
            elif pl_perc > 10:
                pos['stop_loss'] = round(target_profit_taking_price, 2)
                if price <= target_profit_taking_price:
                    pos['recommendation'] = f"{action} {qty} {identifier} {contract_type}"
                    pos['reason'] = "profit > 10% + retrace 30%"        
        
        return positions
        
    def get_my_open_pos(self):
        positions = self._trade_client.get_positions()
        positions_dict = []
        
        for pos in positions:
            contract = str(pos.contract)
            qty = int(pos.quantity)
            cost = round(float(pos.average_cost), 2)
            price = float(pos.market_price)
            pl_abs = round((price - cost) * qty, 2)

            if qty < 0 :
                pl_perc = round((cost - price) / cost * 100, 2)
            else:
                pl_perc = round((price - cost) / cost * 100, 2)
            
            position = {
                'contract': contract,
                'qty': qty,
                'cost': cost,
                'price': price,
                'pl_abs': pl_abs,
                'pl_perc': pl_perc
            }
            positions_dict.append(position)
        return positions_dict
    

    def get_open_filled_orders(self):
        segments = self.get_time_segments_for_filled_orders()
        filled_orders = []
        for s in segments:
            start = s[0]
            end = s[1]
            filled_orders = filled_orders + self._trade_client.get_filled_orders(start_time = start, end_time = end) 
            
        filled_orders = [{
                    'id': order.id,
                    'trade_time': datetime.fromtimestamp(order.trade_time/1000),
                    'action' : order.action,
                    'qty' : order.filled,
                    'avg_fill_price' : order.avg_fill_price,
                    'contract' : str(order.contract)
                } for order in filled_orders ]
        filled_orders = sorted(filled_orders, key=lambda x: x['trade_time'])
        open_orders = filled_orders.copy()
        
        for i, fo in enumerate(filled_orders):
            # print('looping..' + fo['contract']+' ' +str(fo['id']))
            for j, oo in enumerate(filled_orders[i+1:]):                
                # print('comparing..' + oo['contract'] +' ' +str(oo['id']))
                if fo['contract'] == oo['contract'] and fo['id'] != oo['id'] and fo['action'] != oo['action'] and fo['qty'] == oo['qty']:  
                    # print('MATCH! removing..'+ str(fo['id']) +' & '+ str(oo['id']))
                    open_orders.remove(oo)
                    open_orders.remove(fo)
                    filled_orders.remove(oo)
                    break

        open_orders = [o for o in open_orders if o.get('contract').split('/')[1] != "OPT" or (o.get('contract').split('/')[1] == "options" and  datetime.now().strftime("%y%m%d")> o.get('contract').split('/')[0].split(' ')[1][:6])]

        return open_orders


    '''
    def trade_100_tsla_stocks(self, buy_or_sell):
        contract = stock_contract(symbol='TSLA', currency='USD')
        order = market_order(account=self._client_config.account, contract=contract, action=buy_or_sell, quantity=100)
        return self._trade_client.place_order(order)


    # def get_my_assets(self):
    #     return self._trade_client.get_assets()

    def get_my_assets(self):
        # https://github.com/tigerfintech/openapi-python-sdk/blob/master/tigeropen/trade/domain/account.py#L11
        return self._trade_client.get_assets()[0].summary

    def sell_1_tsla_option_atm(self):
        df = self._quote_client.get_option_chain(symbol = 'TSLA', expiry = '2022-12-30')
        # df = df.loc[df['put_call'] == 'PUT', 'strike']
        value = yf.Ticker("TSLA").info['ask']
        df['diff'] = df['strike'].apply(lambda x: abs(float(x) - float(value)))
        idx = df['diff'].idxmin()
        # Print the value in the 'values' column at the index of the minimum value
        strike_price = df.loc[idx, 'strike']
        contract = option_contract_by_symbol(symbol = 'TSLA', expiry = '2022-12-30', strike = strike_price, put_call = 'PUT', currency = 'USD')
        order = market_order(account=self._client_config.account, contract=contract, action='SELL', quantity=1)
        self._trade_client.place_order(order)
    
    def close_1_tsla_option(self):    
        # only buy back when profit
        contract = option_contract_by_symbol(symbol = 'TSLA', expiry = '2022-12-23', strike = 100, put_call = 'PUT', currency = 'USD')
        order = market_order(account=self._client_config.account, contract=contract, action='SELL', quantity=1, limit_price = '100')
        self._trade_client.place_order(order)

    '''