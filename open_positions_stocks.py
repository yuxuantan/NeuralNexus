import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime


def open_positions_stocks(tc, risk_management_settings):
    baseline_portfolio_size_usd = risk_management_settings[
        "baseline_portfolio_size_usd"
    ]  # 50k sgd
    max_loss_percentage_per_trade = risk_management_settings[
        "max_loss_percentage_per_trade"
    ]  # 0.02
    target_profit_percentage_per_trade = risk_management_settings[
        "target_profit_percentage_per_trade"
    ]  # 0.04

    stk_orders_dict = tc.get_orders(
        "STK", datetime.datetime.strptime("2018-01-01", "%Y-%m-%d").date()
    )
    stk_orders_dict = [
        {
            "contract": order.contract,
            "qty_filled": -order.filled if order.action == "SELL" else order.filled,
            "avg_fill_price": order.avg_fill_price,
            "trade_time": datetime.datetime.fromtimestamp(order.trade_time / 1000),
            "profit_usd": -(-order.filled if order.action == "SELL" else order.filled)* order.avg_fill_price,
        }
        for order in stk_orders_dict
    ]

    # TODO: fix the open_date to be the first trade_time after the last time that the contract net_qty=0
    df = pd.DataFrame(stk_orders_dict)
    df["contract"] = df["contract"].astype(str)
    
    # Calculate net_qty and open_date
    def calculate_open_date(group):
        group = group.sort_values("trade_time")
        net_qty = 0
        last_zero_qty_time = None
        for i, row in group.iterrows():
            net_qty += row["qty_filled"]
            if net_qty == 0:
                last_zero_qty_time = row["trade_time"]
        open_date = group[group["trade_time"] > last_zero_qty_time]["trade_time"].min() if last_zero_qty_time else group["trade_time"].min()
        return pd.Series({"net_qty": net_qty, "open_date": open_date})
    
    df = df.groupby("contract").apply(calculate_open_date).query("net_qty != 0")
    
    import yfinance as yf
    # add the max value of the stock after the trade_time until now
    df = df.reset_index()  # Reset the index to access 'contract' as a column
    df["max_value"] = df.apply(
        lambda row: yf.Ticker(row["contract"].replace("/STK/USD", "")).history(start=row["open_date"]).High.max(),
        axis=1
    )


    # get the data
    open_positions_stocks = tc.get_open_positions_stocks()
    open_positions_stocks_data = [
        {
            "contract": str(position.contract).replace("/STK/USD", ""),
            "quantity": position.quantity,
            "average_cost": round(position.average_cost, 2),
            "market_price": round(position.market_price, 2),
            "market_value": position.market_price * position.quantity,
            "open_date": df[df["contract"] == str(position.contract)]["open_date"].values[0] if not df[df["contract"] == str(position.contract)].empty else None,
            "max_value_since_open": df[df["contract"] == str(position.contract)]["max_value"].values[0] if not df[df["contract"] == str(position.contract)].empty else None,
            "pnl": position.market_price * position.quantity
            - position.average_cost * position.quantity,
            "stop_loss_px": round(
                position.average_cost
                - baseline_portfolio_size_usd
                * max_loss_percentage_per_trade
                / position.quantity,
                2,
            ),
            "stop_loss_explanation": "based on risk management settings max_loss_percentage_per_trade",
            "min_take_profit_px": round(
                position.average_cost
                + baseline_portfolio_size_usd
                * target_profit_percentage_per_trade
                / position.quantity,
                2,
            ),
            "notes": None
            
            
        }
        for position in open_positions_stocks
    ]

    # Adjust stop_loss_px if market_price is above min_take_profit_px
    for position in open_positions_stocks_data:
        if position["market_price"] > position["min_take_profit_px"]:
            position["stop_loss_px"] = position["min_take_profit_px"]
            position["stop_loss_explanation"] = "market price is above min_take_profit_px"
            if (position['max_value_since_open']*0.8 > position['stop_loss_px']):
                position["stop_loss_px"] = position['max_value_since_open']*0.8
                position["stop_loss_explanation"] = "market price is >20% above min_take_profit_px, stop loss adjusted to 20% retracement of max value since open"

    # CUSTOM NOTES
    for position in open_positions_stocks_data:
        # HOOD notes
        if position["contract"] == "HOOD":
            position["notes"] = "Covered call. dont stop loss"
        if position["contract"] == "RIVN":
            position["notes"] = "Covered call. dont stop loss"


    # drop the min_take_profit_px, open_date column that are not needed
    open_positions_stocks_data = [
        {k: v for k, v in position.items() if k not in ["min_take_profit_px", "open_date", "max_value_since_open"]}
        for position in open_positions_stocks_data
    ]
    


   

    total_pnl = round(
        sum([position["pnl"] for position in open_positions_stocks_data]), 2
    )
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
