
import streamlit as st
from db import query_df
from datetime import date, timedelta
import pandas as pd

st.title("📊 Reports")

st.subheader("Daily Position (Traded vs Allocated by Hub)")
start = st.date_input("Start", value=date.today() - timedelta(days=30))
end   = st.date_input("End (inclusive)", value=date.today())
# Build query
sql = """
WITH traded AS (
  SELECT gs::date AS gas_day, hub, SUM(qty_dthd) AS traded_dthd
  FROM trades
  CROSS JOIN LATERAL generate_series(start_date, end_date, interval '1 day') AS gs
  WHERE gs::date BETWEEN :start AND :end
  GROUP BY gas_day, hub
),
allocs AS (
  SELECT gas_day, delivery_loc AS hub, SUM(alloc_dth) AS allocated_dth
  FROM scheduling
  WHERE gas_day BETWEEN :start AND :end
  GROUP BY gas_day, delivery_loc
)
SELECT COALESCE(t.gas_day, a.gas_day) AS gas_day,
       COALESCE(t.hub, a.hub) AS hub,
       t.traded_dthd,
       a.allocated_dth,
       COALESCE(a.allocated_dth,0) - COALESCE(t.traded_dthd,0) AS variance_dth
FROM traded t
FULL OUTER JOIN allocs a
  ON t.gas_day = a.gas_day AND t.hub = a.hub
ORDER BY 1 DESC, 2;
"""

df = query_df(sql, {"start": start, "end": end})
st.dataframe(df, use_container_width=True)
st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "daily_position.csv", "text/csv")
