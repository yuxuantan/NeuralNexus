from .broker_controller import BrokerController
from .gsheet_controller import GsheetController
from .db_controller import DbController
from .yfinance_controller import YFinanceController
import telebot
from telebot import util


bc = BrokerController()
gc = GsheetController()
yfc = YFinanceController()

'''chatbot'''
my_chat_id = 27392018
bot=telebot.TeleBot("5244204118:AAFLg6BjMqgfv6WNclKVDaIEgKcZhPnK818")

'''get all positions'''
def telegram_get_recommend():
    
    
    print('writing gsheets.. ')
    gc.write(pos_with_recommendations, "open pos")    
    print('gsheets written!')

    
    print('Sent to telegram!')
    print('Completed!')

    return str(pos_with_recommendations)

'''get all filled orders'''
def telegram_get_filled_orders():
    filled_orders = bc.get_filled_orders()
    gc.write(filled_orders, "all trades")

    msg = bc.convert_pretty_table(filled_orders)

    splitted_msg = util.split_string(str(msg), 4000)
    for m in splitted_msg:
        bot.send_message(my_chat_id, m)

    print(msg)

if __name__ == "__main__":
    telegram_get_recommend()
