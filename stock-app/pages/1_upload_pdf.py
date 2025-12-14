import streamlit as st

# Custom CSS for unified dashboard look
st.markdown("""
<style>
body, .main, .block-container { font-family: 'Inter', sans-serif; }
.hero-header {
    background: linear-gradient(90deg, #4C8BF5 0%, #1A1D23 100%);
    color: #FAFAFA;
    padding: 2rem 1.5rem 1.5rem 1.5rem;
    border-radius: 1.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 24px rgba(76,139,245,0.10);
    display: flex;
    align-items: center;
}
.hero-icon {
    font-size: 2.5rem;
    margin-right: 1.2rem;
}
.card {
    background: #23272F;
    border-radius: 1.2rem;
    box-shadow: 0 2px 12px rgba(76,139,245,0.10);
    padding: 1.5rem 1.2rem;
    margin-bottom: 1.2rem;
    transition: box-shadow 0.2s;
}
.card:hover {
    box-shadow: 0 6px 24px rgba(76,139,245,0.18);
}
.card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #4C8BF5;
    margin-bottom: 0.5rem;
}
.card-desc {
    font-size: 1rem;
    color: #FAFAFA;
    margin-bottom: 0.7rem;
}
</style>
""", unsafe_allow_html=True)

def styled_header(title, subtitle, icon):
    st.markdown(f"""
    <div class='hero-header'>
        <span class='hero-icon'>{icon}</span>
        <div>
            <div style='font-size:1.7rem;font-weight:700;'>{title}</div>
            <div style='font-size:1.05rem;color:#A0AEC0;margin-top:0.3rem;'>{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

styled_header("Upload PDF", "Import daily price lists in PDF format.", "📤")

with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Step 1: Select PDF File</div>", unsafe_allow_html=True)
    st.markdown("<div class='card-desc'>Choose a daily price list PDF to upload and process.</div>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDF(s)", type=["pdf"], key="card_pdf_uploader", accept_multiple_files=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='card-title'>Step 2: Preview & Process - {uploaded_file.name}</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Preview the extracted data and save to database.</div>", unsafe_allow_html=True)
            import tempfile
            import pandas as pd
            import backend.etl.pdf_extractor as pdf_extractor
            import backend.etl.data_cleaner as data_cleaner
            import backend.etl.loader as loader
            import backend.db.db as db
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            st.info(f"Extracting tables from {uploaded_file.name}...")
            dfs, preview, date_str, warnings = pdf_extractor.extract_tables(tmp_path, output_csv="cleaned_daily_price_list.csv")
            st.write("**Preview of cleaned extracted data:**")
            st.dataframe(preview.head(20))
            if warnings:
                st.warning("\n".join(warnings))
            force_reprocess = st.checkbox(f"Reprocess if already uploaded ({uploaded_file.name})", key=f"reprocess_{uploaded_file.name}")
            if st.button(f"Save {uploaded_file.name} to Database", key=f"save_{uploaded_file.name}"):
                engine = db.get_engine()
                session = db.get_session(engine)
                for i, df in enumerate(dfs):
                    st.write(f"Original DataFrame {i+1} columns: {list(df.columns)}")
                    st.dataframe(df.head(5))
                    from backend.etl.data_cleaner import clean_dataframe
                    cleaned = clean_dataframe(df)
                    st.write(f"DataFrame {i+1} shape after cleaning: {cleaned.shape}")
                    required_cols = {'Symbol', 'Close'}
                    missing = [col for col in required_cols if col not in df.columns]
                    if missing:
                        st.warning(f"DataFrame {i+1} is missing required columns: {missing}")
                    if cleaned.empty:
                        st.warning(f"DataFrame {i+1} is empty after cleaning. Check required columns and data format.")
                summary = loader.load_data(dfs, date_str, tmp_path, session, force_reprocess=force_reprocess)
                st.success(f"Inserted {summary['rows_inserted']} rows for {summary['companies']} companies.")
                if summary.get('errors'):
                    st.error("Errors:\n" + "\n".join(summary['errors']))
            st.markdown("</div>", unsafe_allow_html=True)

st.toast("✨ Tip: You can upload multiple PDFs for batch processing.", icon="📤")
