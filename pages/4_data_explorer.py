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

styled_header("Data Explorer", "Dive into raw data, filter, and export.", "📁")

with st.container():
	st.markdown("<div class='card'>", unsafe_allow_html=True)
	st.markdown("<div class='card-title'>Explore Data</div>", unsafe_allow_html=True)
	# ...existing code for data exploration...
	st.markdown("</div>", unsafe_allow_html=True)

st.toast("✨ Tip: Use filters and export options to customize your data view.", icon="📁")
import streamlit as st
import pandas as pd
from backend.db.db import get_engine, get_session
from backend.db.models import DailyPrice, Company

st.title("Data Explorer")

engine = get_engine()
session = get_session(engine)

# Query all daily prices with company info
results = session.query(DailyPrice, Company).join(Company, DailyPrice.company_id == Company.id).all()

# Build DataFrame
rows = []
for dp, company in results:
	rows.append({
		"Date": dp.date,
		"Symbol": company.symbol,
		"Company": company.name,
		"Sector": company.sector,
		"PClose": dp.pclose,
		"Open": dp.open,
		"High": dp.high,
		"Low": dp.low,
		"Close": dp.close,
		"Change": dp.change,
		"Deals": dp.deals,
		"Volume": dp.volume,
		"Value": dp.value,
		"VWAP": dp.vwap,
	})


df = pd.DataFrame(rows)
if not df.empty:
	df = df.sort_values('Date')

st.write("**All Daily Prices:**")
st.dataframe(df)

if not df.empty:
	st.write("Filter by Symbol:")
	symbols = sorted(df["Symbol"].unique())
	selected = st.multiselect("Select symbols", symbols, default=symbols)
	filtered = df[df["Symbol"].isin(selected)]
	st.dataframe(filtered)
else:
	st.info("No data found in database.")
