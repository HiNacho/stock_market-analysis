


import streamlit as st
import os
st.set_page_config(page_title="Stock Analysis & Forecasting App", layout="wide")
# Load Font Awesome from CDN
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"/>
<div style='display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;'>
    <i class='fa-solid fa-chart-line' style='font-size:2.8rem;color:#4C8BF5;'></i>
    <span style='font-size:2.2rem;font-weight:700;color:#4C8BF5;'>StockApp</span>
</div>
""", unsafe_allow_html=True)

# Custom CSS for modern dashboard UI
st.markdown("""
<style>
body, .main, .block-container { font-family: 'Inter', 'Font Awesome 6 Free', 'Font Awesome 6 Brands', sans-serif; }
.hero-header {
    background: linear-gradient(90deg, #4C8BF5 0%, #1A1D23 100%);
    color: #FAFAFA;
    padding: 2.5rem 2rem 2rem 2rem;
    border-radius: 1.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 24px rgba(76,139,245,0.10);
    display: flex;
    align-items: center;
}
.hero-icon {
    font-size: 3.2rem;
    margin-right: 1.2rem;
    color: #4C8BF5;
    font-family: 'Font Awesome 6 Free';
}
.sidebar-logo {
    width: 56px;
    margin-bottom: 1.2rem;
}
.sidebar-section {
    background: #1A1D23;
    border-radius: 1.2rem;
    padding: 1.5rem 1rem 1.5rem 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px rgba(76,139,245,0.07);
}
.nav-link {
    font-size: 1.15rem;
    font-weight: 500;
    color: #FAFAFA;
    padding: 0.7rem 1rem;
    border-radius: 0.7rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    transition: background 0.2s;
}
.nav-link:hover, .nav-link.active {
    background: #4C8BF5;
    color: #fff;
}
.nav-icon {
    font-size: 1.3rem;
    margin-right: 0.7rem;
    font-family: 'Font Awesome 6 Free';
}
.card {
    background: #1A1D23;
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
    font-size: 1.25rem;
    font-weight: 600;
    color: #4C8BF5;
    margin-bottom: 0.5rem;
}
.card-desc {
    font-size: 1rem;
    color: #FAFAFA;
    margin-bottom: 0.7rem;
}
.card-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-family: 'Font Awesome 6 Free';
}
.quick-metrics {
    display: flex;
    gap: 1.2rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: #23272F;
    border-radius: 1rem;
    padding: 1.2rem 1rem;
    box-shadow: 0 2px 8px rgba(76,139,245,0.07);
    flex: 1;
    text-align: left;
}
.metric-title {
    font-size: 1rem;
    color: #FAFAFA;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #4C8BF5;
}
.muted {
    color: #A0AEC0;
    font-size: 0.98rem;
}
.feature-cards {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.feature-card {
    background: #23272F;
    border-radius: 1.2rem;
    box-shadow: 0 2px 12px rgba(76,139,245,0.10);
    padding: 1.5rem 1.2rem;
    flex: 1;
    text-align: left;
    transition: box-shadow 0.2s;
    cursor: pointer;
}
.feature-card:hover {
    box-shadow: 0 6px 24px rgba(76,139,245,0.18);
    background: #1A1D23;
}
.feature-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #4C8BF5;
    margin-bottom: 0.5rem;
}
.feature-desc {
    font-size: 0.98rem;
    color: #FAFAFA;
    margin-bottom: 0.7rem;
}
.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-family: 'Font Awesome 6 Free';
}
</style>
""", unsafe_allow_html=True)

# Helper functions
def styled_header(title, subtitle, icon="📈"):
        st.markdown(f"""
        <div class='hero-header'>
                <span class='hero-icon'>{icon}</span>
                <div>
                        <div style='font-size:2.1rem;font-weight:700;'>{title}</div>
                        <div style='font-size:1.1rem;color:#A0AEC0;margin-top:0.3rem;'>{subtitle}</div>
                </div>
        </div>
        """, unsafe_allow_html=True)

def build_card(title, desc, icon, button_label=None, button_action=None):
        st.markdown(f"""
        <div class='feature-card'>
                <div class='feature-icon'>{icon}</div>
                <div class='feature-title'>{title}</div>
                <div class='feature-desc'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if button_label and button_action:
                st.button(button_label, on_click=button_action, use_container_width=True)

# Sidebar
with st.sidebar:
    st.markdown('<img src="https://img.icons8.com/color/96/stock-market.png" class="sidebar-logo"/>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown("<span style='font-size:1.3rem;font-weight:600;color:#4C8BF5;'>StockApp Navigation</span>", unsafe_allow_html=True)
    nav_items = [
        ("📤", "Upload PDF", "1_upload_pdf.py", "Upload daily price list PDFs"),
        ("📊", "Company Analysis", "2_company_analysis.py", "Analyze company performance"),
        ("📈", "Predictions", "3_predictions.py", "Forecast future prices"),
        ("📁", "Data Explorer", "4_data_explorer.py", "Explore raw data")
    ]
    for icon, name, file, tip in nav_items:
        st.page_link(f"pages/{file}", label=f"{icon} {name}", help=tip)
    st.markdown("---")
    st.markdown("<span class='muted'>Theme: Modern, Wide Layout, Dark/Light Mode Toggle</span>", unsafe_allow_html=True)
    st.toggle("Dark Mode", value=True, key="dark_mode_toggle")
    st.markdown("<span class='muted'>Contact: <a href='mailto:support@stockapp.com'>support@stockapp.com</a></span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-top:2rem;font-size:0.95rem;color:#A0AEC0;text-align:center;">© 2025 StockApp &mdash; v1.0 &mdash; <a href="https://stockapp.com">Website</a></div>', unsafe_allow_html=True)

# Main header
styled_header(
    "Stock Analysis & Forecasting Web App",
    "A modern dashboard for uploading price PDFs, analyzing companies, forecasting prices, and exploring your data.",
    icon="📊"
)
st.markdown("<div style='margin-bottom:1.2rem;'><span style='color:#A0AEC0;font-size:1.05rem;'>Welcome to StockApp! Use the sidebar to navigate. Hover over icons for tips.</span></div>", unsafe_allow_html=True)

# Quick metrics row (example values, replace with real data)
import backend.db.db as db
import backend.db.models as models
engine = db.get_engine()
session = db.get_session(engine)
num_companies = session.query(models.Company).count()
num_pdfs = session.query(models.DailyPrice.date).distinct().count()
try:
    num_forecasts = session.query(models.Forecast).count()
except AttributeError:
    num_forecasts = 0

# Homepage summary chart (top 5 companies by uploads)
import pandas as pd
company_counts = pd.DataFrame(session.query(models.Company.symbol, models.DailyPrice.date).join(models.DailyPrice).all(), columns=["symbol", "date"])
top_companies = company_counts["symbol"].value_counts().head(5)
st.markdown("<div class='quick-metrics'>", unsafe_allow_html=True)
st.markdown(f"""
    <div class='metric-card' title='Total companies in database'>
        <div class='metric-title'>Companies</div>
        <div class='metric-value'>{num_companies}</div>
    </div>
    <div class='metric-card' title='Unique PDFs uploaded'>
        <div class='metric-title'>PDFs Uploaded</div>
        <div class='metric-value'>{num_pdfs}</div>
    </div>
    <div class='metric-card' title='Forecasts generated'>
        <div class='metric-title'>Forecasts</div>
        <div class='metric-value'>{num_forecasts}</div>
    </div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:1.2rem;'><b>Top 5 Companies by Uploads:</b> " + ", ".join(top_companies.index) + "</div>", unsafe_allow_html=True)



# Feature cards row with st.page_link navigation
st.markdown("<div class='feature-cards'>", unsafe_allow_html=True)
st.page_link("pages/1_upload_pdf.py", label="📤 Upload PDF", use_container_width=True, help="Upload daily price list PDFs")
st.page_link("pages/2_company_analysis.py", label="📊 Analyze Companies", use_container_width=True, help="Analyze company performance")
st.page_link("pages/3_predictions.py", label="📈 Forecast Prices", use_container_width=True, help="Forecast future prices")
st.page_link("pages/4_data_explorer.py", label="📁 Data Explorer", use_container_width=True, help="Explore raw data")
st.markdown("</div>", unsafe_allow_html=True)

# Welcome message
st.markdown("<div class='muted' style='margin-top:1.5rem;'>Welcome! Use the sidebar to navigate between features. Your data is secure and private.</div>", unsafe_allow_html=True)

# Modern feedback toast
st.toast("✨ Tip: Use the sidebar to switch between features!", icon="💡")

# Footer
st.markdown('<div style="margin-top:2rem;font-size:0.95rem;color:#A0AEC0;text-align:center;">© 2025 StockApp &mdash; v1.0 &mdash; <a href="https://stockapp.com">Website</a></div>', unsafe_allow_html=True)
