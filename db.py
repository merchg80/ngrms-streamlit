
import os
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

def _get_db_url():
    # Prefer Streamlit secrets; fall back to env var
    db_url = st.secrets.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    if not db_url:
        st.error("DATABASE_URL is not set. Add it in Streamlit Secrets or as an environment variable.")
        st.stop()
    return db_url

@st.cache_resource
def get_engine():
    return create_engine(_get_db_url(), pool_pre_ping=True)

def query_df(sql: str, params: dict | None = None) -> pd.DataFrame:
    with get_engine().begin() as conn:
        return pd.read_sql(text(sql), conn, params=params or {})

def execute(sql: str, params: dict | None = None):
    with get_engine().begin() as conn:
        conn.execute(text(sql), params or {})
