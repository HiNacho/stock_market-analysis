import pandas as pd
import pdfplumber
import re


def is_sn_symbol_row(row):
    # S/N is usually a digit, Symbol is a string (not a price)
    return len(row) >= 2 and re.match(r'^\d+$', str(row[0]).strip()) and str(row[1]).strip().isalpha()

def extract_tables(pdf_path, output_csv=None):
    warnings = []
    all_rows = []
    date_str = None
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        # Remove empty rows
                        if not any(row): continue
                        # Remove header row containing 'NIGERIAN EXCHANGE'
                        if any('NIGERIAN EXCHANGE' in str(cell).upper() for cell in row):
                            continue
                        all_rows.append(row)
            text = pdf.pages[0].extract_text()
            m = re.search(r'(\w+ \d{1,2}, \d{4})', text)
            if m:
                date_str = m.group(1)
    except Exception as e:
        warnings.append(f"pdfplumber failed: {e}")
        return [], pd.DataFrame(), None, warnings

    # Merge broken rows: if a row starts with S/N and Symbol, but is too short, merge with next
    cleaned_rows = []
    i = 0
    while i < len(all_rows):
        row = all_rows[i]
        if is_sn_symbol_row(row) and len(row) < 13 and i + 1 < len(all_rows):
            merged = row + all_rows[i + 1][2:]
            cleaned_rows.append(merged)
            i += 2
        else:
            cleaned_rows.append(row)
            i += 1

    # Define column names
    columns = ['S/N', 'Symbol', 'PClose', 'Open', 'High', 'Low', 'Close', 'Change', '%', 'Deals', 'Volume', 'Value', 'VWAP']
    # Filter out rows that don't start with a valid S/N and Symbol
    final_rows = [row for row in cleaned_rows if is_sn_symbol_row(row)]
    df = pd.DataFrame(final_rows, columns=columns)

    # Save to CSV if requested
    if output_csv:
        df.to_csv(output_csv, index=False)

    # For compatibility with rest of pipeline
    dfs = [df]
    preview = df.copy()
    return dfs, preview, date_str, warnings
