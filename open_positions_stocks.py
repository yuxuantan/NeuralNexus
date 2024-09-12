import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def open_positions_stocks(tc):
    st.subheader("Open Positions Stocks")
    st.divider()
    # get the data
    open_positions_stocks = tc.get_open_positions_stocks()
    open_positions_stocks_data = [
        {
            "contract": position.contract,
            "quantity": position.quantity,
            "average_cost": round(position.average_cost, 2),
            "market_price": round(position.market_price, 2),
            "market_value": position.market_price * position.quantity,
            "pnl": position.market_price * position.quantity
            - position.average_cost * position.quantity,
        }
        for position in open_positions_stocks
    ]

    total_pnl = round(sum([position["pnl"] for position in open_positions_stocks_data]), 2)
    total_market_value = round(
        sum([position["market_value"] for position in open_positions_stocks_data]), 2
    )

    # write the data
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    col1.metric("Unrealised PnL", total_pnl)
    col2.metric("Total Market Value", total_market_value)

    st.dataframe(pd.DataFrame(open_positions_stocks_data), hide_index=True)

    # plot the pie chart of open positions
    labels = [position["contract"] for position in open_positions_stocks_data]
    sizes = [position["market_value"] for position in open_positions_stocks_data]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    return total_market_value