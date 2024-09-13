import streamlit as st 
from utils.crypto_controller import get_wallet_token_balances_price
from utils.cb_controller import get_coinbase_balance
import pandas as pd


sideb = st.sidebar
crypto_wallet_labels = []
crypto_wallet_addresses = []

crypto_wallets = {}

crypto_wallet_address1 = sideb.text_input(
    "Crypto wallet 1 address", "0x42490ba4d1ab3dc1a0780e18fdc3b900059e9966"
)
crypto_wallet_label1 = sideb.text_input("Crypto wallet 1 label", "metamask")
if crypto_wallet_label1 and crypto_wallet_address1:
    crypto_wallets[crypto_wallet_address1] = crypto_wallet_label1

crypto_wallet_address2 = sideb.text_input(
    "Crypto wallet 2 address", "0x26f36257245FF5E86024370A51e17Df7a4c1eF77"
)
crypto_wallet_label2 = sideb.text_input("Crypto wallet 2 label", "ledger")
if crypto_wallet_label2 and crypto_wallet_address2:
    crypto_wallets[crypto_wallet_address2] = crypto_wallet_label2

crypto_wallet_labels = list(crypto_wallets.values())
crypto_wallet_addresses = list(crypto_wallets.keys())


def open_positions_crypto():
    placeholder_overall_value = st.empty()
    st.divider()
    # COINBASE
    coinbase_balances_df = pd.DataFrame(get_coinbase_balance())
    total_market_value_coinbase = round(coinbase_balances_df["usd_value"].sum(), 2)
    st.metric("Total Market Value Coinbase", total_market_value_coinbase)
    st.dataframe(coinbase_balances_df, hide_index=True)
    st.divider()
    # OTHERS
    crypto_balances_df = pd.DataFrame(
        get_wallet_token_balances_price(crypto_wallet_addresses)
    )
    crypto_balances_df["wallet_label"] = crypto_balances_df["wallet_address"].map(
        crypto_wallets
    )
    total_market_value = round(crypto_balances_df["usd_value"].sum(), 2)
    st.metric("Total Market Value Others", total_market_value)
    st.dataframe(
        crypto_balances_df[
            ["wallet_label", "chain", "symbol", "balance", "usd_price", "usd_value"]
        ],
        hide_index=True,
    )


    

    total_market_value_all_usd = total_market_value + total_market_value_coinbase
    placeholder_overall_value.metric("Total Market Value USD", total_market_value_all_usd)


    return total_market_value_all_usd