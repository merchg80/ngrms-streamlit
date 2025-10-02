
import streamlit as st
from db import query_df, execute
from datetime import date
import uuid

st.title("📄 Trades")

with st.form("trade_form", clear_on_submit=True):
    st.subheader("Add a Trade")
    trade_date = st.date_input("Trade Date", value=date.today())
    start_date = st.date_input("Start Date", value=date.today())
    end_date   = st.date_input("End Date", value=date.today())
    buy_sell   = st.selectbox("Buy/Sell", ["Buy", "Sell"])
    product_type = st.selectbox("Product Type", ["Physical","Financial","Basis","Fixed-Price"])
    hub        = st.text_input("Hub (e.g., HSC, Henry)")
    qty        = st.number_input("Qty (Dth/d)", step=100.0, min_value=0.0)
    fixed_price = st.number_input("Fixed Price ($/Dth)", step=0.001, format="%.3f")
    basis       = st.number_input("Basis ($/Dth)", step=0.001, format="%.3f")
    counterparty_id = st.text_input("Counterparty ID (must exist in Counterparties)")
    location_id = st.text_input("Location ID (optional)")
    strategy_tag = st.text_input("Strategy Tag", value="")
    trader     = st.text_input("Trader", value="")
    broker     = st.text_input("Broker", value="")
    remarks    = st.text_area("Remarks", value="")
    submitted = st.form_submit_button("Save Trade")
    if submitted:
        trade_id = str(uuid.uuid4())
        execute(
            """INSERT INTO trades (
                trade_id, trade_date, start_date, end_date, counterparty_id, buy_sell,
                product_type, hub, location_id, index, fixed_price_usd_dth, basis_usd_dth,
                qty_dthd, curve_tenor, strategy_tag, trader, broker, fee_usd, deal_ticket_link, remarks, status
            ) VALUES (
                :trade_id, :trade_date, :start_date, :end_date, :counterparty_id, :buy_sell,
                :product_type, :hub, :location_id, NULL, :fixed_price, :basis,
                :qty, NULL, :strategy_tag, :trader, :broker, NULL, NULL, :remarks, 'open'
            )""",
            {
                "trade_id": trade_id,
                "trade_date": trade_date,
                "start_date": start_date,
                "end_date": end_date,
                "counterparty_id": counterparty_id or None,
                "buy_sell": buy_sell,
                "product_type": product_type,
                "hub": hub or None,
                "location_id": location_id or None,
                "fixed_price": None if fixed_price == 0 else fixed_price,
                "basis": None if basis == 0 else basis,
                "qty": qty or 0,
                "strategy_tag": strategy_tag or None,
                "trader": trader or None,
                "broker": broker or None,
                "remarks": remarks or None,
            }
        )
        st.success(f"Trade saved with ID {trade_id}")

st.divider()
st.subheader("Recent Trades")
df = query_df("SELECT trade_id, trade_date, start_date, end_date, buy_sell, product_type, hub, qty_dthd, fixed_price_usd_dth, basis_usd_dth, strategy_tag FROM trades ORDER BY trade_date DESC, trade_id DESC LIMIT 100")
st.dataframe(df, use_container_width=True)
