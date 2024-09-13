import streamlit as st
import pandas as pd

def open_positions_options(tc, risk_management_settings):
    baseline_portfolio_size_usd = risk_management_settings[
        "baseline_portfolio_size_usd"
    ]  # 50k sgd
    max_loss_percentage_per_trade = risk_management_settings[
        "max_loss_percentage_per_trade"
    ]  # 0.02
    target_profit_percentage_per_trade = risk_management_settings[
        "target_profit_percentage_per_trade"
    ]  # 0.04

    open_positions_options = tc.get_open_positions_options()
    print(open_positions_options)
    open_positions_options_data = [
        {
            "ticker": str(position.contract).split(" ")[0],
            "exp": f"20{str(position.contract).split(' ')[-1][:6].lstrip('0')[:2]}-{str(position.contract).split(' ')[-1][:6].lstrip('0')[2:4]}-{str(position.contract).split(' ')[-1][:6].lstrip('0')[4:6]}",
            "type": "PUT"
            if str(position.contract).split(" ")[-1][6:7] == "P"
            else "CALL",
            "strike": int(
                str(position.contract)
                .split(" ")[-1][7:]
                .replace("/OPT/USD", "")
                .lstrip("0")
            )
            / 1000,
            "quantity": position.quantity,
            "average_cost": round(position.average_cost, 2),
            "market_price": round(position.market_price, 2),
            "market_value": position.market_price * position.quantity * 100,
            "stop_loss_px": round(
                position.average_cost
                - baseline_portfolio_size_usd
                * max_loss_percentage_per_trade
                / position.quantity
                / 100,
                2,
            ),
            "stop_loss_explanation": "based on risk management settings max_loss_percentage_per_trade",
            "target_profit_px": round(position.average_cost * 0.25, 2)
            if position.quantity < 0
            else round(
                position.average_cost
                + baseline_portfolio_size_usd
                * target_profit_percentage_per_trade
                / position.quantity
                / 100,
                2,
            ),
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


    for position in open_positions_options_data:
        if position["quantity"] < 0:  # shorts = collect premium = 75%
            if position["market_price"] < position["target_profit_px"]:
                position["stop_loss_px"] = position["target_profit_px"]
                position["stop_loss_explanation"] = (
                    "market price is below target_profit_px"
                )
        else:  # longs = after hitting target price, retrace 20% stop loss
            if position["market_price"] > position["target_profit_px"]:
                position["stop_loss_px"] = position["target_profit_px"]
                position["stop_loss_explanation"] = (
                    "market price is above target_profit_px"
                )

                if position["market_price"] * 0.8 > position["stop_loss_px"]:
                    position["stop_loss_px"] = position["market_price"] * 0.8
                    position["stop_loss_explanation"] = (
                        "market price is >20% above min_take_profit_px, stop loss adjusted to 20% retracement of market price"
                    )

    # remove unused columns
    open_positions_options_data = [
        {k: v for k, v in position.items() if k not in ["target_profit_px"]}
        for position in open_positions_options_data
    ]

    # CUSTOM NOTES
    for position in open_positions_options_data:
        if position["ticker"] == "COIN" and position["exp"] =='2024-09-27' and position["type"] == 'PUT':
            position["notes"] = "dont mind owning coin at 180. dont set SL"
        elif position["ticker"] == "RIVN" and position["exp"] =='2024-10-18' and position["type"] == 'CALL':
            position["notes"] = "dont mind selling at 15 dont SL"
        elif position["ticker"] == "HOOD" and position["exp"] =='2024-09-20' and position["type"] == 'CALL':
            position["notes"] = "dont mind selling at 21 dont SL"
        else:
            position["notes"] = "stop loss set✅"
    

    st.dataframe(pd.DataFrame(open_positions_options_data), hide_index=True)
    return total_market_value_options
