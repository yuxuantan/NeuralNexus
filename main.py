
from filled_options import filled_options
from filled_stocks import filled_stocks
from open_positions_stocks import open_positions_stocks
from open_positions_options import open_positions_options
from open_positions_crypto import open_positions_crypto
from utils.tiger_controller import TigerController
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

tc = TigerController()

sgd_to_usd_exchange_rate = 1.30

st.title("Neural Nexus")
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
    st.header("Overall Portfolio")
    st.divider()
    tiger_cash = round(tc.get_cash() * sgd_to_usd_exchange_rate, 2)
    ocbc_cash = 167944
    dbs_cash = 1597

    portfolio_data = {
        "Category": ["Tiger Cash", "OCBC Cash", "DBS Cash"],
        "Amount_SGD": [tiger_cash, ocbc_cash, dbs_cash],
    }

    col1, col2 = st.columns([1, 1])
    with col1:
        placeholder_total_portfolio_value = st.empty()
        st.divider()
        placeholder_portfolio_df = st.empty()
    with col2:
        st.metric("USD to SGD", sgd_to_usd_exchange_rate)
        st.divider()
        placeholder_pie_chart = st.empty()

    st.divider()
    



with open_pos_stks_tab:
    stocks_value_sgd = round(open_positions_stocks(tc) * sgd_to_usd_exchange_rate, 2)
    
with open_pos_options_tab:
    options_value_sgd = round(open_positions_options(tc) * sgd_to_usd_exchange_rate, 2)

with open_pos_crypto_tab:
    crypto_value_sgd = round(open_positions_crypto() * sgd_to_usd_exchange_rate, 2)

with filled_opt_tab:
    filled_options()
    
with filled_stk_tab:
    filled_stocks(tc)

total_portfolio_value = round(tiger_cash+ocbc_cash+dbs_cash+stocks_value_sgd+options_value_sgd+crypto_value_sgd, 2)
placeholder_total_portfolio_value.metric("TOTAL portfolio SGD", str(total_portfolio_value))
# draw pie chart for breakdown
labels = ["Tiger Cash", "OCBC Cash", "DBS Cash", "Stocks Value", "Crypto Value"]
sizes = [tiger_cash, ocbc_cash, dbs_cash, stocks_value_sgd, crypto_value_sgd]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
placeholder_pie_chart.pyplot(fig1)

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