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

styled_header("Forecast Prices", "Generate price forecasts and visualize trends.", "📈")

with st.container():
	st.markdown("<div class='card'>", unsafe_allow_html=True)
	st.markdown("<div class='card-title'>Select Company & Forecast</div>", unsafe_allow_html=True)
	# ...existing code for prediction and visualization...
	st.markdown("</div>", unsafe_allow_html=True)

st.toast("✨ Tip: Forecasts are based on historical price trends.", icon="📈")
import streamlit as st
st.title("Predictions")
st.write("Coming soon: Train and view forecasts.")
