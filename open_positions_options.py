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
            "market_value": position.market_price * position.quantity * 100,
            "pnl": (
                position.market_price * position.quantity
                - position.average_cost * position.quantity
            )
            * 100,
            "market_price": round(position.market_price, 2),
            "stop_loss_px": round(
                position.average_cost
                - baseline_portfolio_size_usd
                * max_loss_percentage_per_trade
                / position.quantity
                / 100,
                2,
            ),
            "target_profit_px": round(
                position.average_cost * 0.25, 2
            )  # 75% profit of premium if short
            if position.quantity < 0
            else round(  # follow target profit if long
                position.average_cost
                + baseline_portfolio_size_usd
                * target_profit_percentage_per_trade
                / position.quantity
                / 100,
                2,
            ),
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
        if (
            position["quantity"] < 0
            and position["market_price"] < position["target_profit_px"]
        ):  # shorts # take profit! = collect 75% of premium
            position["notes"] = (
                "⚠️ [target_profit_px] - already hit target profit of 75% premium"
            )
        elif (
            position["quantity"] > 0
            and position["market_price"] > position["target_profit_px"]
        ):  # longs = after hitting target price, take profit
            # TODO: profit retracement strategy for long positions not done yet.
            position["notes"] = (
                "⚠️ [target_profit_px] - market price is above target_profit_px"
            )
        elif (
            position["quantity"] < 0
            and position["target_profit_px"]
            <= position["market_price"]
            <= position["stop_loss_px"]
        ) or (
            position["quantity"] > 0
            and position["target_profit_px"]
            >= position["market_price"]
            >= position["stop_loss_px"]
        ):
            position["notes"] = (
                "[stop_loss_px] - market price is between target_profit_px and stop_loss_px"
            )
        else:
            position["notes"] = (
                "DANGER ⚠️ [stop_loss_px] - market price is outside of stop_loss_px. Need to close this position"
            )

    # plot bar graph of long positions vs short positions
    long_positions = abs(
        sum(
            position["market_value"]
            for position in open_positions_options_data
            if position["quantity"] > 0
            and position["type"] == "CALL"
            or position["quantity"] < 0
            and position["type"] == "PUT"
        )
    )
    short_positions = abs(
        sum(
            position["market_value"]
            for position in open_positions_options_data
            if position["quantity"] < 0
            and position["type"] == "CALL"
            or position["quantity"] > 0
            and position["type"] == "PUT"
        )
    )

    # CUSTOM NOTES
    for position in open_positions_options_data:
        if position["ticker"] == "COIN" and position["type"] == "PUT":
            position["notes"] = (
                "dont mind owning coin at 170. dont set SL. long term exp"
            )
        elif position["ticker"] == "COIN" and position["type"] == "CALL":
            position["notes"] = (
                "dont mind selling coin at 182.5 for 0 stock loss. short term exp = low risk"
            )
        elif position["ticker"] == "RIVN":
            position["notes"] = "dont mind owning rivn at 11. dont set SL"
        elif position["ticker"] == "MARA":
            position["notes"] = "dont mind getting rid of MARA at 17.5"

    st.dataframe(pd.DataFrame(open_positions_options_data), hide_index=True)
    st.bar_chart(
        pd.DataFrame(
            {
                "Position Type": ["Long", "Short"],
                "Market Value": [long_positions, short_positions],
            }
        ).set_index("Position Type"),
        use_container_width=False,
        width=500,
        horizontal=True,
    )
    return total_market_value_options, open_positions_options_data
