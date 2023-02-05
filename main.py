from broker_controller import BrokerController
from gsheet_controller import GsheetController
from db_controller import DbController
from yfinance_controller import YFinanceController
import pandas as pd

bc = BrokerController()
gc = GsheetController()
dbc = DbController()
yfc = YFinanceController()

'''get options extreme price'''
# print(bc.get_extreme_option_price(1666324800000, 'TSLA  230210P00180000', 'SELL'))
# print(bc.get_current_option_price('TSLA  230210P00180000'))

# '''(fix) get filled orders - ONLY those that are not closed yet'''
open_filled_orders = bc.get_open_filled_orders()
print(bc.convert_pretty_table(open_filled_orders))


# '''(done) - incorporate retracement profit taking - get all recommendations'''
# actions = bc.get_my_recommended_actions(open_filled_orders)
# print(bc.convert_pretty_table(actions))



'''(DEV) db'''
# dbController.create_table('hello')
# dbController.select_all_from_table('hello')
# dbController.insert_into_table('hello', '4,2,3,4')
# dbController.select_all_from_table('hello')

'''get all positions'''
# pos_tbl = brokerController.get_my_open_pos()[0]
# print(pos_tbl)

# TODO: 
'''
# ** IMPT - EACH position traded should follow the same strategy (R percentage of each trade, not for open positions)
    # I must be able to break up my OPEN positions to the individual trades that contribute to the position, and the dates, and individual P&Ls
    # idea: write each filled orders into DB sqlite/ Gsheets when they are being executed. use this data to calculate P&L for each entry to market. 
    # we can get position regularly to check if they tally, if they dont, raise an error

# good to have 
    # calculate the trading fees
    # handle sql failures eg unique constraints

'''

