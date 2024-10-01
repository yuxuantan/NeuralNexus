
from filled_options import filled_options
from filled_stocks import filled_stocks
from utils.tiger_controller import TigerController
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(layout="wide")
from open_positions_stocks import open_positions_stocks
from open_positions_options import open_positions_options
from open_positions_crypto import open_positions_crypto

tc = TigerController()

usd_to_sgd_exchange_rate = 1.30

st.title("Neural Nexus")

st.sidebar.subheader("Risk Management Settings")
baseline_portfolio_size_usd = st.sidebar.number_input("Baseline Portfolio Size USD", value=38333, step=1000)
max_loss_percentage_per_trade = st.sidebar.number_input("Max Loss Percentage Per Trade", value=0.02, step=0.01)
target_profit_percentage_per_trade = st.sidebar.number_input("Target Profit Percentage Per Trade", value=0.04, step=0.01)

risk_management_settings = {
    "baseline_portfolio_size_usd": baseline_portfolio_size_usd,
    "max_loss_percentage_per_trade": max_loss_percentage_per_trade,
    "target_profit_percentage_per_trade": target_profit_percentage_per_trade,
}

(
    overall_tab,
    open_pos_stks_tab,
    open_pos_options_tab,
    open_pos_crypto_tab,
    filled_opt_tab,
    filled_stk_tab,
) = st.tabs(
    [
        "Overall Portfolio",
        "Open Position Stocks",
        "Open Position Options",
        "Open Position Crypto",
        "Filled Options",
        "Filled Stocks",
    ]
)

with overall_tab:
    tiger_cash = round(tc.get_cash() * usd_to_sgd_exchange_rate, 2)
    ocbc_cash = 17095
    dbs_cash = 3437
    trust_cash = 150139

    portfolio_data = {
        "Category": ["Tiger Cash", "OCBC Cash", "DBS Cash", "Trust Cash"],
        "Amount_SGD": [tiger_cash, ocbc_cash, dbs_cash, trust_cash],
    }

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        placeholder_total_portfolio_value = st.empty()
        st.divider()
        st.metric("USD to SGD", usd_to_sgd_exchange_rate)
        st.divider()
        placeholder_portfolio_df = st.empty()
    with col2:
        placeholder_overall_pnl = st.empty()
        st.divider()
        # show vix price using yfinance
        vix = yf.Ticker("^VIX")
        vix_price = vix.history(period="1d")["Close"].values[0]
        st.metric("VIX Price", round(vix_price, 2))
        if vix_price >= 21:
            st.error("VIX is above 21! market is fearful. Time to go long")
        elif vix_price <= 13:
            st.error("VIX is below 13! market is greedy. Time to go short")
        else:
            st.success("VIX is between 13 and 21. Market is neutral")
        placeholder_pie_chart = st.empty()
    # with col3:
        # st.divider()

    st.divider()
    



with open_pos_stks_tab:
    mkt_value, df = open_positions_stocks(tc, risk_management_settings)
    stocks_value_sgd = round(mkt_value * usd_to_sgd_exchange_rate, 2)
    
with open_pos_options_tab:
    mkt_value, df = open_positions_options(tc, risk_management_settings)
    options_value_sgd = round(mkt_value * usd_to_sgd_exchange_rate, 2)

with open_pos_crypto_tab:
    crypto_value_sgd = round(open_positions_crypto() * usd_to_sgd_exchange_rate, 2)

with filled_opt_tab:
    pnl_options = round(filled_options() * usd_to_sgd_exchange_rate, 2)
    
with filled_stk_tab:
    pnl_stocks = round(filled_stocks(tc) * usd_to_sgd_exchange_rate, 2) 

total_portfolio_value = round(tiger_cash+ocbc_cash+dbs_cash+stocks_value_sgd+options_value_sgd+crypto_value_sgd, 2)
overall_pnl = round(pnl_options + pnl_stocks, 2)

placeholder_total_portfolio_value.metric("TOTAL portfolio SGD", str(total_portfolio_value))
placeholder_overall_pnl.metric("Overall PnL SGD (without crypto)", str(overall_pnl))
# draw pie chart for breakdown
# labels = ["Tiger Cash", "OCBC Cash", "DBS Cash", "Stocks Value", "Crypto Value"]
# sizes = [tiger_cash, ocbc_cash, dbs_cash, stocks_value_sgd, crypto_value_sgd]
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
# ax1.axis("equal")
# placeholder_pie_chart.pyplot(fig1)

portfolio_data["Category"].append("Stocks Value SGD")
portfolio_data["Amount_SGD"].append(stocks_value_sgd)
portfolio_data["Category"].append("Options Value SGD")
portfolio_data["Amount_SGD"].append(options_value_sgd)
portfolio_data["Category"].append("Crypto Value SGD")
portfolio_data["Amount_SGD"].append(crypto_value_sgd)
placeholder_portfolio_df.dataframe(pd.DataFrame(portfolio_data), hide_index=True)

monthly_burnrate_input = overall_tab.number_input("Monthly Burn Rate", value=2000, step=100)
overall_tab.subheader("Buffer Months: " + str(round(total_portfolio_value/monthly_burnrate_input, 2)))
overall_tab.subheader("Buffer Years: " + str(round(total_portfolio_value/monthly_burnrate_input/12, 2)))
