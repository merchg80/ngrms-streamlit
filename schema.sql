
-- NGRMS Starter Schema (Postgres)
-- Run this whole script in your Postgres query console
-- Note: all IDs are TEXT for simplicity; you can switch to UUID later.

CREATE TABLE IF NOT EXISTS counterparties (
  counterparty_id TEXT PRIMARY KEY,
  legal_name TEXT NOT NULL,
  short_name TEXT,
  dba TEXT,
  lei TEXT,
  ein TEXT,
  is_vendor BOOLEAN DEFAULT FALSE,
  is_customer BOOLEAN DEFAULT FALSE,
  credit_limit_usd NUMERIC(14,2),
  parent_entity TEXT,
  netting_set TEXT,
  payment_terms_days INT,
  invoicing_email TEXT,
  ops_email TEXT,
  notes TEXT,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS locations (
  location_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT,
  pipeline TEXT,
  utility_ldc TEXT,
  iso TEXT,
  zone TEXT,
  hub_code TEXT,
  balancing_area TEXT,
  state TEXT,
  county TEXT,
  meter_id TEXT,
  op_point_id TEXT,
  capacity_dthd NUMERIC(14,2),
  loss_factor NUMERIC(8,6),
  pressure_psig NUMERIC(8,2),
  notes TEXT,
  active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS contracts (
  contract_id TEXT PRIMARY KEY,
  counterparty_id TEXT REFERENCES counterparties(counterparty_id),
  contract_type TEXT,
  start_date DATE,
  end_date DATE,
  evergreen BOOLEAN DEFAULT FALSE,
  termination_notice_days INT,
  swing_min_dthd NUMERIC(14,2),
  swing_max_dthd NUMERIC(14,2),
  index TEXT,
  basis_to TEXT,
  price_formula TEXT,
  point_of_delivery TEXT,
  title_transfer_point TEXT,
  incoterms TEXT,
  credit_support TEXT,
  lc_required BOOLEAN,
  auto_renew BOOLEAN,
  doc_repo_link TEXT,
  notes TEXT,
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS transport (
  transport_id TEXT PRIMARY KEY,
  pipeline TEXT,
  contract_number TEXT,
  rate_type TEXT,
  max_daily_quantity_dthd NUMERIC(14,2),
  primary_receipt TEXT,
  primary_delivery TEXT,
  fuel_pct NUMERIC(6,4),
  loss_pct NUMERIC(6,4),
  reservation_rate_usd_dthm NUMERIC(14,6),
  commodity_rate_usd_dth NUMERIC(14,6),
  path_rights TEXT,
  start_date DATE,
  end_date DATE,
  notes TEXT,
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS storage (
  storage_id TEXT PRIMARY KEY,
  facility TEXT,
  contract_number TEXT,
  max_inventory_dth NUMERIC(16,2),
  max_injection_dthd NUMERIC(14,2),
  max_withdrawal_dthd NUMERIC(14,2),
  fuel_pct NUMERIC(6,4),
  park_loan_rights TEXT,
  ratchet_table_link TEXT,
  reservation_rate_usd_mo NUMERIC(14,6),
  commodity_rates_desc TEXT,
  start_date DATE,
  end_date DATE,
  notes TEXT,
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS trades (
  trade_id TEXT PRIMARY KEY,
  trade_date DATE NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  counterparty_id TEXT REFERENCES counterparties(counterparty_id),
  buy_sell TEXT CHECK (buy_sell IN ('Buy','Sell')),
  product_type TEXT,
  hub TEXT,
  location_id TEXT REFERENCES locations(location_id),
  index TEXT,
  fixed_price_usd_dth NUMERIC(14,6),
  basis_usd_dth NUMERIC(14,6),
  qty_dthd NUMERIC(14,2) NOT NULL,
  curve_tenor TEXT,
  strategy_tag TEXT,
  trader TEXT,
  broker TEXT,
  fee_usd NUMERIC(14,2),
  deal_ticket_link TEXT,
  remarks TEXT,
  status TEXT DEFAULT 'open'
);

CREATE TABLE IF NOT EXISTS scheduling (
  sched_id TEXT PRIMARY KEY,
  gas_day DATE NOT NULL,
  cycle TEXT,
  pipeline TEXT,
  transport_id TEXT REFERENCES transport(transport_id),
  receipt_loc TEXT,
  delivery_loc TEXT,
  nom_dth NUMERIC(14,2),
  conf_dth NUMERIC(14,2),
  alloc_dth NUMERIC(14,2),
  imbalance_dth NUMERIC(14,2),
  fuel_pct NUMERIC(6,4),
  fuel_burn_dth NUMERIC(14,2),
  comments TEXT,
  status TEXT DEFAULT 'actualized'
);

CREATE INDEX IF NOT EXISTS idx_sched_gasday ON scheduling(gas_day);
CREATE INDEX IF NOT EXISTS idx_sched_delivery ON scheduling(delivery_loc);

CREATE TABLE IF NOT EXISTS prices (
  price_date DATE NOT NULL,
  hub TEXT NOT NULL,
  index_name TEXT,
  contract_month DATE,
  quote_source TEXT,
  price_type TEXT,
  price_usd_dth NUMERIC(14,6),
  asof_timestamp TIMESTAMPTZ DEFAULT now(),
  notes TEXT,
  PRIMARY KEY (price_date, hub, price_type, index_name)
);

CREATE TABLE IF NOT EXISTS invoices (
  invoice_id TEXT PRIMARY KEY,
  counterparty_id TEXT REFERENCES counterparties(counterparty_id),
  invoice_date DATE NOT NULL,
  period_start DATE,
  period_end DATE,
  category TEXT,
  subtype TEXT,
  currency TEXT DEFAULT 'USD',
  amount NUMERIC(14,2),
  tax_amount NUMERIC(14,2),
  total_amount NUMERIC(14,2),
  status TEXT DEFAULT 'draft',
  due_date DATE,
  external_reference TEXT,
  notes TEXT,
  file_link TEXT
);

CREATE TABLE IF NOT EXISTS settlements (
  settlement_id TEXT PRIMARY KEY,
  trade_id TEXT REFERENCES trades(trade_id),
  period DATE,
  qty_dth NUMERIC(14,2),
  price_usd_dth NUMERIC(14,6),
  cashflow_usd NUMERIC(14,2),
  fx_rate NUMERIC(12,6),
  pay_receive TEXT CHECK (pay_receive IN ('Pay','Receive')),
  value_date DATE,
  status TEXT DEFAULT 'open',
  notes TEXT
);
