import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Embassy Office Parks REIT AI", layout="centered")

st.title("📊 Embassy Office Parks REIT Investment AI")
st.caption("Long-term investment signal based on CAGR and dividend yield")

# Download data
ticker = "EMBASSY.NS"
df = yf.download(ticker, start="2019-01-01")

# Choose 'Adj Close' if available, else fallback to 'Close'
price_col = None
if "Adj Close" in df.columns:
    price_col = "Adj Close"
elif "Close" in df.columns:
    price_col = "Close"

# Stop if no usable price column
if df.empty or price_col is None:
    st.error("❌ Failed to fetch usable price data for EMBASSY.NS. Try again later or check ticker.")
    st.stop()

df.dropna(inplace=True)

# Calculate CAGR
years = len(df) / 252
start_price = df[price_col].iloc[0]
end_price = df[price_col].iloc[-1]
cagr = (end_price / start_price) ** (1 / years) - 1

# Estimate dividend yield (approx)
dividends = df[price_col].pct_change().rolling(252).mean() * 100
if dividends.isna().all():
    avg_yield = 0
else:
    avg_yield = dividends.dropna().iloc[-1]

# Display price chart
st.subheader("📈 Price Chart (All-Time)")
st.line_chart(df[price_col])

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
