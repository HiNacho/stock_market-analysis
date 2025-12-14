import pandas as pd
from backend.etl.data_cleaner import clean_dataframe

def test_data_cleaning():
    data = {
        'Symbol': ['MTNN', 'ZENITH'],
        'Open': ['200.0', '25,000'],
        'Close': ['210.5', '25,500'],
        'Volume': ['1,000', '2,000']
    }
    df = pd.DataFrame(data)
    cleaned = clean_dataframe(df)
    assert cleaned['Open'].iloc[1] == 25000.0
    assert cleaned['Close'].iloc[1] == 25500.0
    assert cleaned['Volume'].iloc[0] == 1000.0
    assert cleaned['Symbol'].iloc[0] == 'MTNN'
