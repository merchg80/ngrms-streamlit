
import streamlit as st
from db import query_df, execute
from datetime import date
import uuid

st.title("🧾 Invoices")

with st.form("inv_form", clear_on_submit=True):
    st.subheader("Add an Invoice (header)")
    counterparty_id = st.text_input("Counterparty ID")
    invoice_date = st.date_input("Invoice Date", value=date.today())
    period = st.date_input("Billing Period (start and end)", value=(date.today().replace(day=1), date.today()))
    category = st.selectbox("Category", ["commodity","transport","storage","park-loan","imbalance","fee","tax"])
    amount = st.number_input("Amount (pre-tax)", step=0.01, format="%.2f")
    tax_amount = st.number_input("Tax Amount", step=0.01, format="%.2f")
    total_amount = st.number_input("Total Amount", step=0.01, format="%.2f")
    notes = st.text_area("Notes / File link")
    submitted = st.form_submit_button("Save Invoice")
    if submitted:
        invoice_id = str(uuid.uuid4())
        execute(
            """INSERT INTO invoices (
                invoice_id, counterparty_id, invoice_date, period_start, period_end,
                category, currency, amount, tax_amount, total_amount, status, notes, file_link
            ) VALUES (
                :invoice_id, :counterparty_id, :invoice_date, :pstart, :pend,
                :category, 'USD', :amount, :tax_amount, :total_amount, 'draft', :notes, :file_link
            )""",
            {
                "invoice_id": invoice_id,
                "counterparty_id": counterparty_id or None,
                "invoice_date": invoice_date,
                "pstart": period[0],
                "pend": period[1],
                "category": category,
                "amount": amount or 0,
                "tax_amount": tax_amount or 0,
                "total_amount": total_amount or 0,
                "notes": notes or None,
                "file_link": notes or None
            }
        )
        st.success(f"Saved invoice {invoice_id}")

st.divider()
st.subheader("Recent Invoices")
df = query_df("SELECT invoice_id, counterparty_id, invoice_date, period_start, period_end, category, total_amount, status FROM invoices ORDER BY invoice_date DESC LIMIT 100")
st.dataframe(df, use_container_width=True)
