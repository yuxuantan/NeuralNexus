import streamlit as st
import datetime
import pandas as pd
import utils.utils as utils

def filled_stocks(tc):
    filled_stocks = tc.get_orders(
        "STK", datetime.datetime.strptime("2020-01-01", "%Y-%m-%d").date()
    )
    filled_stocks_data = [
        {
            "contract": order.contract,
            "qty_filled": -order.filled if order.action == "SELL" else order.filled,
            "avg_fill_price": round(order.avg_fill_price, 2),
            "trade_time": datetime.datetime.fromtimestamp(order.trade_time / 1000),
            "profit_usd": round(order.realized_pnl, 2),
        }
        for order in filled_stocks
    ]


    stk_col1, stk_col2 = st.columns([2, 1])
    with stk_col2:
        option2 = st.selectbox(
            "View", ("All", "Month on Month", "Year on Year"), key="option2"
        )


    total_pnl = round(sum([data["profit_usd"] for data in filled_stocks_data]), 2)
    filled_stocks_df = pd.DataFrame(filled_stocks_data)
    # Calculate PnL change compared to 30 days ago
    pnl_change = round(
        total_pnl - utils.get_cumulative_sum_x_days_ago(filled_stocks_df, 30), 2
    )
    st.metric("Total Filled Stocks PnL", total_pnl, pnl_change)


    col1, col2 = st.columns([1, 2])

    filled_stocks_month_df = filled_stocks_df.copy()
    filled_stocks_month_df["month"] = filled_stocks_month_df["trade_time"].dt.to_period("M")
    filled_stocks_month_df = (
        filled_stocks_month_df.groupby("month")["profit_usd"].sum().reset_index()
    )
    filled_stocks_month_df["month"] = filled_stocks_month_df["month"].astype(str)

    filled_stocks_year_df = filled_stocks_df.copy()
    filled_stocks_year_df["year"] = filled_stocks_year_df["trade_time"].dt.to_period("Y")
    filled_stocks_year_df = (
        filled_stocks_year_df.groupby("year")["profit_usd"].sum().reset_index()
    )
    filled_stocks_year_df["year"] = filled_stocks_year_df["year"].astype(str)

    if option2 == "Month on Month":
        with col1:
            st.dataframe(
                filled_stocks_month_df.sort_values(by="month", ascending=False),
                hide_index=True,
            )
        with col2:
            st.line_chart(filled_stocks_month_df, x="month", y="profit_usd")
    elif option2 == "Year on Year":
        with col1:
            st.dataframe(
                filled_stocks_year_df.sort_values(by="year", ascending=False),
                hide_index=True,
            )
        with col2:
            st.line_chart(filled_stocks_year_df, x="year", y="profit_usd")
    else:
        st.dataframe(
            filled_stocks_df.sort_values(by="trade_time", ascending=False), hide_index=True
        )

    return total_pnl