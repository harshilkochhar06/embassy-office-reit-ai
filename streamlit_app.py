import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Embassy Office Parks REIT AI", layout="centered")

st.title("📊 Embassy Office Parks REIT Investment AI")
st.caption("Long-term investment signal based on CAGR and dividend yield")

# Download data
ticker = "EMBASSY.NS"
df = yf.download(ticker, start="2019-01-01")

# Error handling
if df.empty or "Adj Close" not in df.columns:
    st.error("❌ Failed to fetch 'Adj Close' data for EMBASSY.NS. Please try again later or check ticker symbol.")
    st.stop()

df.dropna(inplace=True)

# Calculate CAGR
years = len(df) / 252
start_price = df["Adj Close"].iloc[0]
end_price = df["Adj Close"].iloc[-1]
cagr = (end_price / start_price) ** (1 / years) - 1

# Estimate dividend yield (approx)
dividends = df["Adj Close"].pct_change().rolling(252).mean() * 100
avg_yield = dividends.iloc[-1] if not dividends.isna().all() else 0

# Display price chart
st.subheader("📈 Price Chart (All-Time)")
st.line_chart(df["Adj Close"])

# Key metrics
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
