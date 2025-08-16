import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit UI
st.set_page_config(page_title="📈 Stock Price Tracker", layout="wide")
st.title("📈 Stock Price Tracker")
st.markdown("Get stock info, history, and charts with live data from Yahoo Finance.")

# User Input
ticker_symbol = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA, MSFT)", "AAPL").upper()

if ticker_symbol:
    try:
        # Fetch Stock Data
        stock = yf.Ticker(ticker_symbol)
        info = stock.get_info()

        # Stock Info
        current_price = info.get('currentPrice', 'N/A')
        name = info.get('longName', ticker_symbol)
        market_cap = info.get('marketCap', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')

        st.subheader(f"📊 {name}")
        col1, col2, col3 = st.columns(3)
        col1.metric("💵 Current Price", f"${current_price}")
        col2.metric("🏢 Market Cap", f"{market_cap}")
        col3.metric("📈 P/E Ratio", f"{pe_ratio}")

        # Historical Data
        hist = stock.history(period="1mo")
        if hist.empty:
            st.warning("⚠️ No historical data found.")
        else:
            hist['MA10'] = hist['Close'].rolling(10).mean()

            # Show Data Table
            st.subheader("📅 Historical Data (Last 1 Month)")
            st.dataframe(hist.tail(10))

            # Plot with Matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            hist[['Close', 'MA10']].plot(ax=ax, title=f"{ticker_symbol} - Last 1 Month Prices")
            plt.xlabel("Date")
            plt.ylabel("Price (USD)")
            plt.grid(True)
            st.pyplot(fig)

            # Download CSV
            safe_ticker = ticker_symbol.replace("^", "").replace("/", "_")
            csv = hist.to_csv().encode('utf-8')
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{safe_ticker}_1mo_history.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Error fetching data: {e}")
