import streamlit as st
import pandas as pd

def open_positions_options(tc):
    # Open position options
    st.subheader("Open Positions Options")

    open_positions_options = tc.get_open_positions_options()
    open_positions_options_data = [
        {
            "contract": position.contract,
            "quantity": position.quantity,
            "average_cost": round(position.average_cost, 2),
            "market_price": round(position.market_price, 2),
            "market_value": position.market_price * position.quantity * 100,
            "pnl": (
                position.market_price * position.quantity
                - position.average_cost * position.quantity
            )
            * 100,
        }
        for position in open_positions_options
    ]

    total_pnl_options = round(
        sum([position["pnl"] for position in open_positions_options_data]), 2
    )
    total_market_value_options = round(
        sum([position["market_value"] for position in open_positions_options_data]), 2
    )

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    col1.metric("Unrealised PnL Options", total_pnl_options)
    col2.metric("Total Market Value Options", total_market_value_options)

    st.dataframe(
        pd.DataFrame(open_positions_options_data), hide_index=True
    )
    return total_market_value_options