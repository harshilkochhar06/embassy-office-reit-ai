import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Embassy Office REIT AI", layout="centered")

st.title("📊 Embassy Office Parks REIT Investment AI")
st.caption("Long-term investment signal based on CAGR and dividend yield")

# Download data
ticker = "EMBASSY.NS"
df = yf.download(ticker, start="2019-01-01")
df.dropna(inplace=True)

# CAGR
years = len(df) / 252
cagr = (df["Adj Close"][-1] / df["Adj Close"][0]) ** (1 / years) - 1

# Dividend yield (approx)
dividends = df['Adj Close'].pct_change().rolling(252).mean() * 100
avg_yield = dividends[-1] if not dividends.isna().all() else 0

# Charts
st.subheader("📈 Price Chart (All-Time)")
st.line_chart(df["Adj Close"])

st.subheader("📊 Investment Metrics")
st.metric("CAGR (since 2019)", f"{cagr:.2%}")
st.metric("Estimated Dividend Yield", f"{avg_yield:.2f}%")

# Recommendation
st.subheader("📌 AI Investment Recommendation")
if cagr > 0.07 and avg_yield > 5:
    st.success("✅ Good long-term opportunity. Consider investing.")
elif cagr > 0.05:
    st.info("🟡 Fair performance. Monitor fundamentals before investing.")
else:
    st.warning("❌ Low CAGR. Might not be ideal for long-term holding.")
