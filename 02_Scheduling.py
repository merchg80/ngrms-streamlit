
import streamlit as st
from db import query_df, execute
from datetime import date
import uuid, pandas as pd, io

st.title("🚚 Scheduling")

tab1, tab2 = st.tabs(["Add Row", "Upload CSV"])

with tab1:
    with st.form("sched_form", clear_on_submit=True):
        gas_day = st.date_input("Gas Day", value=date.today())
        cycle = st.selectbox("Cycle", ["Timely","Evening","Intraday 1","Intraday 2","Intraday 3"])
        pipeline = st.text_input("Pipeline / LDC")
        receipt = st.text_input("Receipt Loc (hub or meter)")
        delivery = st.text_input("Delivery Loc (hub or meter)")
        nom = st.number_input("Nominated (Dth)", step=100.0, min_value=0.0)
        conf = st.number_input("Confirmed (Dth)", step=100.0, min_value=0.0)
        alloc = st.number_input("Allocated (Dth)", step=100.0, min_value=0.0)
        fuel_pct = st.number_input("Fuel % (e.g., 2.5 for 2.5%)", step=0.1, min_value=0.0)
        comments = st.text_area("Comments", value="")
        submit = st.form_submit_button("Save")
        if submit:
            sched_id = str(uuid.uuid4())
            imbalance = (alloc or 0) - (conf or 0)
            fuel_burn = (alloc or 0) * (fuel_pct or 0) / 100.0
            execute(
                """INSERT INTO scheduling (
                    sched_id, gas_day, cycle, pipeline, transport_id, receipt_loc, delivery_loc,
                    nom_dth, conf_dth, alloc_dth, imbalance_dth, fuel_pct, fuel_burn_dth, comments, status
                ) VALUES (
                    :sched_id, :gas_day, :cycle, :pipeline, NULL, :receipt, :delivery,
                    :nom, :conf, :alloc, :imbalance, :fuel_pct, :fuel_burn, :comments, 'actualized'
                )""", {
                    "sched_id": sched_id, "gas_day": gas_day, "cycle": cycle, "pipeline": pipeline or None,
                    "receipt": receipt or None, "delivery": delivery or None,
                    "nom": nom or 0, "conf": conf or 0, "alloc": alloc or 0,
                    "imbalance": imbalance, "fuel_pct": fuel_pct or 0, "fuel_burn": fuel_burn,
                    "comments": comments or None
                }
            )
            st.success(f"Saved scheduling row {sched_id}")

with tab2:
    st.write("Upload a CSV with columns: gas_day, cycle, pipeline, receipt_loc, delivery_loc, nom_dth, conf_dth, alloc_dth, fuel_pct, comments")
    file = st.file_uploader("Choose CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)
        # Light validation
        required = {"gas_day","cycle","pipeline","receipt_loc","delivery_loc","nom_dth","conf_dth","alloc_dth"}
        if not required.issubset(set([c.lower() for c in df.columns])):
            st.error(f"CSV missing required columns: {sorted(list(required))}")
        else:
            # normalize
            df.columns = [c.lower() for c in df.columns]
            rows = 0
            for _, r in df.iterrows():
                sched_id = str(uuid.uuid4())
                # parse date
                try:
                    gd = pd.to_datetime(r.get("gas_day")).date()
                except:
                    continue
                cycle = (r.get("cycle") or "Timely")
                pipeline = r.get("pipeline")
                receipt = r.get("receipt_loc")
                delivery = r.get("delivery_loc")
                nom = float(r.get("nom_dth") or 0)
                conf = float(r.get("conf_dth") or 0)
                alloc = float(r.get("alloc_dth") or 0)
                fuel_pct = float(r.get("fuel_pct") or 0)
                comments = r.get("comments")
                imbalance = alloc - conf
                fuel_burn = alloc * fuel_pct / 100.0
                execute(
                    """INSERT INTO scheduling (
                        sched_id, gas_day, cycle, pipeline, transport_id, receipt_loc, delivery_loc,
                        nom_dth, conf_dth, alloc_dth, imbalance_dth, fuel_pct, fuel_burn_dth, comments, status
                    ) VALUES (
                        :sched_id, :gas_day, :cycle, :pipeline, NULL, :receipt, :delivery,
                        :nom, :conf, :alloc, :imbalance, :fuel_pct, :fuel_burn, :comments, 'actualized'
                    )""", {
                        "sched_id": sched_id, "gas_day": gd, "cycle": cycle, "pipeline": pipeline or None,
                        "receipt": receipt or None, "delivery": delivery or None,
                        "nom": nom, "conf": conf, "alloc": alloc, "imbalance": imbalance,
                        "fuel_pct": fuel_pct, "fuel_burn": fuel_burn, "comments": comments or None
                    }
                )
                rows += 1
            st.success(f"Uploaded {rows} rows.")

st.divider()
st.subheader("Latest Scheduling (last 200 rows)")
df = query_df("SELECT * FROM scheduling ORDER BY gas_day DESC, sched_id DESC LIMIT 200")
st.dataframe(df, use_container_width=True)
