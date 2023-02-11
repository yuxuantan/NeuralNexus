from broker_controller import BrokerController
from gsheet_controller import GsheetController
from db_controller import DbController
from yfinance_controller import YFinanceController
import telebot
from telebot import util


bc = BrokerController()
gc = GsheetController()
yfc = YFinanceController()

'''chatbot'''
# only privatise my chat id
whitelist = [27392018]
bot=telebot.TeleBot("5244204118:AAFLg6BjMqgfv6WNclKVDaIEgKcZhPnK818")
'''get all positions'''
@bot.message_handler(commands=['recommended'])
def telegram_get_recommend(message):
    pos = bc.get_my_open_pos()
    ''' incorporate retracement profit taking - get all recommendations'''
    pos_with_recommendations = bc.get_my_recommended_actions(pos)
    gc.write(pos_with_recommendations, "open pos")

    msg = bc.convert_pretty_table(pos_with_recommendations)
    splitted_msg = util.split_string(str(msg), 4000)
    if message.chat.id in whitelist:
        for m in splitted_msg:
            bot.send_message(message.chat.id, m)
    print(msg)

'''get all filled orders'''
@bot.message_handler(commands=['filled'])
def telegram_get_filled_orders(message):
    filled_orders = bc.get_filled_orders()
    gc.write(filled_orders, "all trades")

    msg = bc.convert_pretty_table(filled_orders)

    splitted_msg = util.split_string(str(msg), 4000)
    if message.chat.id in whitelist:
        for m in splitted_msg:
            bot.send_message(message.chat.id, m)

    print(msg)

bot.polling()

# '''get options extreme price'''
# print(bc.get_extreme_option_price(1666324800000, 'TSLA  230210P00180000', 'SELL'))
# print(bc.get_current_option_price('TSLA  230210P00180000'))

# '''(fix) get filled orders - ONLY those that are not closed yet'''
# open_filled_orders = bc.get_open_filled_orders()
# print(bc.convert_pretty_table(open_filled_orders))





'''(DEV) db'''
# dbController.create_table('hello')
# dbController.select_all_from_table('hello')
# dbController.insert_into_table('hello', '4,2,3,4')
# dbController.select_all_from_table('hello')



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

