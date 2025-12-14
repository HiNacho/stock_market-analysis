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

styled_header("Company Analysis", "Explore company analytics, sector breakdowns, and more.", "📊")

with st.container():
	st.markdown("<div class='card'>", unsafe_allow_html=True)
	st.markdown("<div class='card-title'>Select Company</div>", unsafe_allow_html=True)
	# Get all companies
	from backend.db.db import get_engine, get_session
	from backend.db.models import Company
	engine = get_engine()
	session = get_session(engine)
	companies = session.query(Company).all()
	company_symbols = [c.symbol for c in companies]
	# Use session state to sync selection
	if "selected_company" not in st.session_state:
		st.session_state["selected_company"] = company_symbols[0] if company_symbols else None
	def update_company_selection():
		st.session_state["selected_company"] = st.session_state["main_company_select"]
	selected_symbol_main = st.selectbox(
		"Select a company to analyze",
		company_symbols,
		key="main_company_select",
		index=company_symbols.index(st.session_state["selected_company"]) if st.session_state["selected_company"] in company_symbols else 0,
		on_change=update_company_selection
	)
	st.markdown("</div>", unsafe_allow_html=True)

st.toast("✨ Tip: Use the sidebar to switch between companies and analysis features.", icon="📊")

import streamlit as st
import pandas as pd
from backend.db.db import get_engine, get_session
from backend.db.models import DailyPrice, Company
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

# NGX sector mapping
SECTOR_MAP = {
	"Financial Services": [
		"ACCESSCORP", "FCMB", "FIDELITYBK", "GTCO", "JAIZBANK", "STANBIC", "STERLINGNG", "UBA", "WEMABANK", "ETI", "NPFMCRFBK",
		"CORNERST", "GUINEAINS", "LINKASSURE", "MBENEFIT", "MANSARD", "NEM", "PRESTIGE", "REGALINS", "ROYALEX", "SOVRENINS", "SUNUASSUR", "UNIVINSURE",
		"ABBEYBDS", "LIVINGTRUST",
		"ETRANZACT", "VFDGROUP",
		"AFRIPRUD", "UCAP"
	],
	"Oil & Gas": ["ARADEL", "CONOIL", "ETERNA", "MRS", "SEPLAT", "TOTAL", "OANDO"],
	"Industrial Goods": ["BERGER", "BETAGLAS", "BUACEMENT", "CAP", "CUTIX", "DANGCEM", "FIDSON", "MEYER", "WAPCO"],
	"Consumer Goods": ["CADBURY", "CHAMPION", "DANGSUGAR", "FLOURMILL", "HONYFLOUR", "INTBREW", "MAYBAKER", "NB", "NASCON", "NNFM", "PZ", "UNILEVER", "VITAFOAM"],
	"Consumer Services": ["IKEJAHOTEL", "TANTALIZER", "TRANSCOHOT"],
	"Conglomerates": ["UACN", "TRANSCOHOT", "TRANSCORP", "RTBRISCOE", "SCOA"],
	"Agriculture": ["ELLAHLAKES", "FTNCOCOA", "OKOMUOIL", "PRESCO", "LIVESTOCK"],
	"Services": ["ABCTRANS", "CAVERTON", "DAARCOMM", "GREENWETF", "REDSTAREX", "SKYAVN", "TRANSEXPR", "GEREGU"],
	"ICT / Technology": ["ACADEMY", "CHAMS", "CWG", "ETRANZACT", "NSLTECH", "OMATEK"],
	"Healthcare": ["MECURE", "MORISON", "NEIMETH", "FIDSON"],
	"Real Estate": ["UPDC", "UNIONDICON"],
	"Utilities": ["GEREGU", "TRANSPOWER"],
	"ETFs": ["LOTUSHAL15", "SIAMLETF40", "STANBICETF30", "VETBANK", "VETGOODS", "VETGRIF30", "VETINDETF", "VSPBONDETF"],
	"Fixed Income Securities & Government Bonds": ["FGSUK2031S4", "FGSUK2032S5", "NIDF", "TAJSUKS2"],
	"Mining & Natural Resources": ["JAPAULGOLD", "MULTIVERSE"],
	"Industrial/Construction Engineering": ["JBERGER", "TRANSPOWER"],
	"Telecommunications": ["AIRTELAFRI", "MTNN"]
}

def classify_sector(symbol):
	for sector, symbols in SECTOR_MAP.items():
		if symbol in symbols:
			return sector
	return "Uncategorized"


engine = get_engine()
session = get_session(engine)

# Sidebar navigation
st.sidebar.title("Company Analysis")
st.sidebar.info("Select a company and choose a visualization or insight.")

# Get all companies
companies = session.query(Company).all()
company_symbols = [c.symbol for c in companies]

def update_sidebar_selection():
	st.session_state["selected_company"] = st.session_state["sidebar_company_select"]
selected_symbol = st.sidebar.selectbox(
	"Select a company",
	company_symbols,
	key="sidebar_company_select",
	index=company_symbols.index(st.session_state["selected_company"]) if st.session_state["selected_company"] in company_symbols else 0,
	on_change=update_sidebar_selection,
	help="Choose a company to analyze"
)

visual_options = [
	"Price Trend (MA)",
	"MACD",
	"Volatility",
	"Best/Worst Day",
	"Candlestick Chart",
	"Daily Returns Histogram",
	"Drawdown Analysis",
	"Monthly Aggregates",
	"Weekly Aggregates",
	"Price/Volume Heatmap",
	"Forecasting"
]
selected_vis = st.sidebar.radio("Visualization/Insight", visual_options, help="Pick a chart or analysis to view")

if selected_symbol:
	company = session.query(Company).filter_by(symbol=selected_symbol).first()
	prices = session.query(DailyPrice).filter_by(company_id=company.id).order_by(DailyPrice.date).all()
	if prices:
		with st.spinner("Loading company data and analysis..."):
			df = pd.DataFrame([{ 'Date': p.date, 'Close': p.close, 'Open': p.open, 'High': p.high, 'Low': p.low, 'Volume': p.volume, 'Value': p.value, 'VWAP': p.vwap } for p in prices])
			df = df.sort_values('Date')
			df['MA5'] = df['Close'].rolling(window=5).mean()
			df['MA20'] = df['Close'].rolling(window=20).mean()
			df['Return'] = df['Close'].pct_change()
			df['Volatility'] = df['Return'].rolling(window=5).std()
			# MACD
			exp12 = df['Close'].ewm(span=12, adjust=False).mean()
			exp26 = df['Close'].ewm(span=26, adjust=False).mean()
			df['MACD'] = exp12 - exp26
			df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
			# Drawdown
			df['Cumulative'] = df['Close'].cummax()
			df['Drawdown'] = (df['Close'] - df['Cumulative']) / df['Cumulative']
			# Monthly/Weekly
			df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
			df['Week'] = pd.to_datetime(df['Date']).dt.to_period('W')

			# Profile card with sector classification
			sector = classify_sector(company.symbol)
			st.markdown(f"### {company.symbol} - {company.name if company.name else ''}")
			cols = st.columns([2,1])
			with cols[0]:
				st.markdown(f"**Sector:** {sector}")
				st.markdown(f"**Records:** {len(df)}")
				st.markdown(f"**Date Range:** {df['Date'].min()} to {df['Date'].max()}")
			with cols[1]:
				st.download_button("Download Data (CSV)", df.to_csv(index=False), file_name=f"{selected_symbol}_data.csv", mime="text/csv")

			# Tabs for analysis and latest data
			tab1, tab2 = st.tabs(["Analysis", "Latest Data"])
			with tab1:
				if selected_vis == "Price Trend (MA)":
					st.subheader(f"Price Trend for {selected_symbol} (with MA)")
					fig = go.Figure()
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close', line=dict(color='blue')))
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], mode='lines', name='Open', line=dict(color='orange', dash='dot')))
					fig.add_trace(go.Scatter(x=df['Date'], y=df['High'], mode='lines', name='High', line=dict(color='green', dash='dash')))
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Low'], mode='lines', name='Low', line=dict(color='red', dash='dash')))
					fig.add_trace(go.Scatter(x=df['Date'], y=df['MA5'], mode='lines', name='MA5', line=dict(color='purple', dash='dot')))
					fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], mode='lines', name='MA20', line=dict(color='black', dash='dot')))
					fig.update_layout(xaxis_title='Date', yaxis_title='Price', legend_title='Legend', hovermode='x unified')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "MACD":
					st.subheader(f"MACD for {selected_symbol}")
					fig = go.Figure()
					fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], mode='lines', name='MACD', line=dict(color='blue')))
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Signal'], mode='lines', name='Signal', line=dict(color='red')))
					fig.update_layout(xaxis_title='Date', yaxis_title='MACD', legend_title='Legend', hovermode='x unified')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Volatility":
					st.subheader(f"Volatility (5-day rolling std) for {selected_symbol}")
					fig = go.Figure()
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Volatility'], mode='lines', name='Volatility', line=dict(color='orange')))
					fig.update_layout(xaxis_title='Date', yaxis_title='Volatility', hovermode='x unified')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Best/Worst Day":
					st.subheader(f"Best/Worst Day for {selected_symbol}")
					best_idx = df['Return'].idxmax()
					worst_idx = df['Return'].idxmin()
					st.write(f"Best Day: {df.loc[best_idx, 'Date']} ({df.loc[best_idx, 'Return']*100:.2f}%)")
					st.write(f"Worst Day: {df.loc[worst_idx, 'Date']} ({df.loc[worst_idx, 'Return']*100:.2f}%)")
				elif selected_vis == "Candlestick Chart":
					st.subheader(f"Candlestick Chart for {selected_symbol}")
					fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
					fig.update_layout(xaxis_title='Date', yaxis_title='Price', hovermode='x unified')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Daily Returns Histogram":
					st.subheader(f"Daily Returns Histogram for {selected_symbol}")
					fig = px.histogram(df, x='Return', nbins=30, title='Distribution of Daily Returns')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Drawdown Analysis":
					st.subheader(f"Drawdown Analysis for {selected_symbol}")
					fig = go.Figure()
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Drawdown'], mode='lines', name='Drawdown', line=dict(color='red')))
					fig.update_layout(xaxis_title='Date', yaxis_title='Drawdown', hovermode='x unified')
					st.plotly_chart(fig, use_container_width=True)
					st.write(f"Max Drawdown: {df['Drawdown'].min()*100:.2f}%")
				elif selected_vis == "Monthly Aggregates":
					st.subheader(f"Monthly Aggregates for {selected_symbol}")
					monthly = df.groupby('Month').agg({'Close':'mean', 'Volume':'sum'}).reset_index()
					monthly['Month'] = monthly['Month'].astype(str)
					st.dataframe(monthly)
					fig = px.line(monthly, x='Month', y='Close', title='Monthly Average Close')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Weekly Aggregates":
					st.subheader(f"Weekly Aggregates for {selected_symbol}")
					weekly = df.groupby('Week').agg({'Close':'mean', 'Volume':'sum'}).reset_index()
					weekly['Week'] = weekly['Week'].astype(str)
					st.dataframe(weekly)
					fig = px.line(weekly, x='Week', y='Close', title='Weekly Average Close')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Price/Volume Heatmap":
					st.subheader(f"Price/Volume Heatmap for {selected_symbol}")
					fig = px.density_heatmap(df, x='Close', y='Volume', nbinsx=30, nbinsy=30, color_continuous_scale='Viridis')
					st.plotly_chart(fig, use_container_width=True)
				elif selected_vis == "Forecasting":
					st.subheader(f"Simple Price Forecast for {selected_symbol}")
					# Simple linear regression forecast
					df['DateInt'] = pd.to_datetime(df['Date']).map(pd.Timestamp.toordinal)
					X = df[['DateInt']]
					y = df['Close']
					model = LinearRegression()
					model.fit(X, y)
					future_days = 7
					last_date = df['DateInt'].iloc[-1]
					future_dates = [last_date + i for i in range(1, future_days+1)]
					future_preds = model.predict(np.array(future_dates).reshape(-1,1))
					future_df = pd.DataFrame({'DateInt': future_dates, 'Forecast': future_preds})
					# Convert DateInt back to datetime using fromordinal
					future_df['Date'] = future_df['DateInt'].apply(pd.Timestamp.fromordinal)
					fig = go.Figure()
					fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
					fig.add_trace(go.Scatter(x=future_df['Date'], y=future_df['Forecast'], mode='lines', name='Forecast', line=dict(dash='dot', color='red')))
					fig.update_layout(xaxis_title='Date', yaxis_title='Price', hovermode='x unified')
					st.plotly_chart(fig, use_container_width=True)
			with tab2:
				st.write("**Latest Data:**")
				st.dataframe(df.tail(10))
				st.write("**Insights:**")
				st.write(f"Max Close: {df['Close'].max()}")
				st.write(f"Min Close: {df['Close'].min()}")
				st.write(f"Average Close: {df['Close'].mean():.2f}")
				st.write(f"Total Volume: {df['Volume'].sum():,.0f}")
	else:
		st.warning("No price data found for this company.")
