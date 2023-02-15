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
my_chat_id = 27392018
bot=telebot.TeleBot("5244204118:AAFLg6BjMqgfv6WNclKVDaIEgKcZhPnK818")

'''get all positions'''
def telegram_get_recommend():
    pos = bc.get_my_open_pos()
    
    ''' incorporate retracement profit taking - get all recommendations'''
    pos_with_recommendations = bc.get_my_recommended_actions(pos)
    print(pos_with_recommendations)

    gc.write(pos_with_recommendations, "open pos")

    msg = bc.convert_pretty_table(pos_with_recommendations)
    print(msg)

    output_msg = ''
    for pos in pos_with_recommendations:
        if pos.get('recommendation') is not None:
            output_msg = output_msg + '\n' + pos.get('recommendation') + ' at ' + str(pos.get('stop_loss')) + ', reason: ' + pos.get('reason') 
    bot.send_message(my_chat_id, output_msg)
    # splitted_msg = util.split_string(str(tele_msg), 4000)
    
    # for m in splitted_msg:

'''get all filled orders'''
def telegram_get_filled_orders():
    filled_orders = bc.get_filled_orders()
    gc.write(filled_orders, "all trades")

    msg = bc.convert_pretty_table(filled_orders)

    splitted_msg = util.split_string(str(msg), 4000)
    for m in splitted_msg:
        bot.send_message(my_chat_id, m)

    print(msg)

    
telegram_get_recommend()
