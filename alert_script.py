from open_positions_stocks import open_positions_stocks
from open_positions_options import open_positions_options
from utils.tiger_controller import TigerController
import json

import utils.telegram_controller as telegram_controller

risk_management_settings = {
    "baseline_portfolio_size_usd": 38333,
    "max_loss_percentage_per_trade": 0.02,
    "target_profit_percentage_per_trade": 0.04,
}

mkt_value_stocks, stock_data = open_positions_stocks(TigerController(), risk_management_settings)
mkt_value_options, options_data = open_positions_options(TigerController(), risk_management_settings)


output_msg_stk = "*Stocks_data*"
for data in stock_data:
    output_msg_stk += f"""
Contract: {data["contract"]}
Quantity: {data["quantity"]}
Average Cost: {data["average_cost"]}
Market Value: {data["market_value"]}
PnL: {data["pnl"]}
Market Price: {data["market_price"]}
Stop Loss Price: {data["stop_loss_px"]}
Target Profit Price: {data["target_profit_px"]}
Notes: {data["notes"]}
"""
    
# Escape special characters in the message to avoid parsing errors
def escape_special_characters(text):
    escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

output_msg_stk = escape_special_characters(output_msg_stk)


telegram_controller.send_message(chat_id=27392018, message=output_msg_stk)

output_msg_opt = "*Options_data*"
for data in options_data:
    output_msg_opt += f"""
Ticker: {data["ticker"]}
Exp: {data["exp"]}
Type: {data["type"]}
Strike: {data["strike"]}
Quantity: {data["quantity"]}
Average Cost: {data["average_cost"]}
Market Value: {data["market_value"]}
PnL: {data["pnl"]}
Market Price: {data["market_price"]}
Stop Loss Price: {data["stop_loss_px"]}
Target Profit Price: {data["target_profit_px"]}
"""
    
output_msg_opt = escape_special_characters(output_msg_opt)
telegram_controller.send_message(chat_id=27392018, message=output_msg_opt)
