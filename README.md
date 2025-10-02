
# NGRMS (Natural Gas Risk Management System) — Streamlit Starter

This is a tiny, working web app you can deploy on Streamlit Cloud that connects to a Postgres database and lets you:
- Add **Trades**
- Add/Upload **Scheduling** rows
- Add **Invoices**
- View a **Daily Position** report (Traded vs Allocated by hub)

## 0) What you need
- A **Postgres** database URL (Neon/Supabase/Railway/RDS — anything with a connection string)
- A **Streamlit Cloud** account (free tier is fine)

## 1) Create a Postgres database
- Make a new Postgres instance on your preferred provider.
- Copy the connection string (it usually looks like: `postgresql://USER:PASSWORD@HOST:PORT/DBNAME`).
- Run the `schema.sql` file in the provider's SQL console to create tables.

## 2) Deploy the app on Streamlit Cloud
- Put these files in a GitHub repo (or upload directly to Streamlit Cloud).
- In Streamlit Cloud, create a new app and point it at `streamlit_app.py` in this folder.
- In **App Settings → Secrets**, add:
  ```
  DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DBNAME"
  ```

## 3) Use the app
- Go to **Trades** page → add a sample trade.
- Go to **Scheduling** page → add a row or upload a CSV (see the columns printed on the page).
- Go to **Invoices** page → add an invoice header.
- Go to **Reports** → choose a date range and see Daily Position.

## Notes
- Tables use TEXT IDs by default so you can type anything or paste UUIDs. You can switch to UUID later.
- The schema roughly matches the Excel workbook provided earlier so you can import data over time.
- This is a starter; you can add pages for Counterparties, Prices, Settlements, Transport, Storage, etc.
