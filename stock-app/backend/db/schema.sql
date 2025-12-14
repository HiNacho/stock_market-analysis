CREATE TABLE companies (
  id SERIAL PRIMARY KEY,
  symbol VARCHAR(32) UNIQUE NOT NULL,
  name TEXT,
  sector TEXT
);

CREATE TABLE uploaded_files (
  id SERIAL PRIMARY KEY,
  filename TEXT,
  upload_date TIMESTAMP,
  md5 VARCHAR(64) UNIQUE,
  rows_extracted INTEGER,
  success BOOLEAN
);

CREATE TABLE daily_prices (
  id SERIAL PRIMARY KEY,
  company_id INTEGER REFERENCES companies(id),
  date DATE NOT NULL,
  pclose NUMERIC,
  open NUMERIC,
  high NUMERIC,
  low NUMERIC,
  close NUMERIC,
  change NUMERIC,
  deals INTEGER,
  volume BIGINT,
  value NUMERIC,
  vwap NUMERIC,
  source_file_id INTEGER REFERENCES uploaded_files(id),
  UNIQUE(company_id, date)
);
