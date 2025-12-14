import backend.etl.pdf_extractor as pdf_extractor
import os

def test_pdf_extraction():
    sample_pdf = "DAILY_PRICE_LIST_DEC_5_2025.pdf"
    if not os.path.exists(sample_pdf):
        print("Sample PDF not found.")
        return
    dfs, preview, date_str, warnings = pdf_extractor.extract_tables(sample_pdf)
    assert len(dfs) > 0, "No tables extracted"
    assert not preview.empty, "Preview DataFrame is empty"
    assert date_str is not None, "Date not extracted"
