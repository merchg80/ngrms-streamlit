
import streamlit as st
from db import query_df
st.set_page_config(page_title="NGRMS", page_icon="🛢️", layout="wide")

st.title("🛢️ Natural Gas Risk Management System (NGRMS) — Starter")
st.write("Use the pages on the left to add **Trades**, upload **Scheduling**, add **Invoices**, and view **Reports**.")

st.subheader("Quick Stats (read-only)")
col1, col2, col3, col4 = st.columns(4)
try:
    trades = query_df("SELECT count(*) AS n FROM trades")
    sched  = query_df("SELECT count(*) AS n FROM scheduling")
    inv    = query_df("SELECT count(*) AS n FROM invoices")
    cp     = query_df("SELECT count(*) AS n FROM counterparties")
    col1.metric("Trades", int(trades['n'][0]))
    col2.metric("Scheduling rows", int(sched['n'][0]))
    col3.metric("Invoices", int(inv['n'][0]))
    col4.metric("Counterparties", int(cp['n'][0]))
except Exception as e:
    st.warning("Stats unavailable until the database is initialized. See README for setup.")
