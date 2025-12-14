# Data cleaning utilities for stock price tables
import pandas as pd
import numpy as np

def clean_dataframe(df):
    # Standardize column names
    col_map = {
        'SYMBOL': 'Symbol', 'symbol': 'Symbol', 'SYMB': 'Symbol', 'TICKER': 'Symbol', 'CODE': 'Symbol',
        'PCLOSE': 'PClose', 'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low',
        'CLOSE': 'Close', 'CHANGE': 'Change', 'DEALS': 'Deals', 'VOLUME': 'Volume',
        'VALUE': 'Value', 'VWAP': 'VWAP', 'DATE': 'Date'
    }
    df.columns = [col_map.get(str(c).strip().upper(), str(c).strip().title()) for c in df.columns]
    # Remove whitespace, upper symbols
    if 'Symbol' in df.columns:
        df['Symbol'] = df['Symbol'].astype(str).str.strip().str.upper()
    # Coerce numerics
    num_cols = ['PClose', 'Open', 'High', 'Low', 'Close', 'Change', 'Deals', 'Volume', 'Value', 'VWAP']
    for col in num_cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace(',', '', regex=False)
                .str.replace('$', '', regex=False)
                .str.replace('%', '', regex=False)
                .str.replace('−', '-', regex=False)
                .replace(['', 'nan', 'None'], np.nan)
                .apply(lambda x: x if str(x).replace('.', '', 1).replace('-', '', 1).isdigit() else np.nan)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')
    # If required columns missing, skip this DataFrame
    required_cols = {'Symbol', 'Close'}
    if not required_cols.issubset(df.columns):
        return pd.DataFrame()  # skip this DataFrame if required columns missing
    # Fill missing numeric columns with 0
    num_cols = ['PClose', 'Open', 'High', 'Low', 'Close', 'Change', 'Deals', 'Volume', 'Value', 'VWAP']
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    # Fill missing Symbol with empty string
    if 'Symbol' in df.columns:
        df['Symbol'] = df['Symbol'].fillna("")
    # Remove any row where any column contains 'NIGERIAN EXCHANGE' (case-insensitive)
    df = df[~df.apply(lambda row: row.astype(str).str.upper().str.contains('NIGERIAN EXCHANGE').any(), axis=1)]
    # Validate
    df = df[df['Close'] >= 0]
    if 'Volume' in df.columns:
        df = df[df['Volume'] >= 0]
    return df.reset_index(drop=True)
