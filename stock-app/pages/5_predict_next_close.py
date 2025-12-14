import streamlit as st
import pandas as pd
import joblib
import os

def load_data():
    return pd.read_csv("data/stock_data.csv")

def load_model():
    return joblib.load("models/best_model.pkl")

def predict_next_day_close(company_name, model, df, feature_cols):
    company_df = df[df['Company'] == company_name].sort_values('S/N')
    latest = company_df.iloc[-1:]
    X_latest = latest[feature_cols]
    pred = model.predict(X_latest)[0]
    last_close = latest['Close'].values[0]
    pct_change = (pred - last_close) / last_close * 100
    return pred, last_close, pct_change

def main():
    st.title("Stock Market Closing Price Predictor")
    df = load_data()
    model = load_model()
    companies = df['Company'].unique()
    feature_cols = [c for c in df.columns if c not in ['Target_Close','Company','S/N']]
    company = st.selectbox("Select a company", companies)
    company_df = df[df['Company'] == company].sort_values('S/N')
    st.write("Recent historical prices (last 30 days):")
    st.dataframe(company_df[['S/N','Close']].tail(30).reset_index(drop=True))
    st.line_chart(company_df[['S/N','Close']].set_index('S/N').tail(30))
    if st.button("Predict Next Day Closing Price"):
        pred, last_close, pct_change = predict_next_day_close(company, model, df, feature_cols)
        st.success(f"Predicted next-day close: {pred:.2f}")
        st.info(f"Last close: {last_close:.2f}")
        st.info(f"Predicted % change: {pct_change:.2f}%")
        # Optional: plot marker for predicted next-day close
        import plotly.graph_objs as go
        chart_df = company_df[['S/N','Close']].tail(30).copy()
        chart_df = chart_df.append({'S/N': chart_df['S/N'].max()+1, 'Close': pred}, ignore_index=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_df['S/N'], y=chart_df['Close'], mode='lines+markers', name='Close'))
        fig.add_trace(go.Scatter(x=[chart_df['S/N'].max()], y=[pred], mode='markers', marker=dict(color='red', size=12), name='Predicted Next Close'))
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
