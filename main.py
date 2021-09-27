import yfinance as yf
import streamlit as st
import datetime as dt

# Hello! Welcome to my first project!

st.header("The Stock Analyzer App!")

st.markdown("""
Have a stock you want to analyze? Input the ticker symbol below!

---

""")

symbol = st.text_input("What ticker symbol would you like to analyze?: ", value="MSFT").upper()

# This block of code will return the information about a stock. If the ticker symbol doesn't exist or can't
# be found, it will handle that error.
try:
    if symbol != "":
        st.write(f"You have chosen {symbol}. Here's some relevant information: ")

        ticker = yf.Ticker(symbol)

        image_url = ticker.get_info()["logo_url"]
        st.image(image=image_url)

        st.write(ticker.get_info()["shortName"])

        website = ticker.get_info()["website"]
        with st.expander("Associated Website"):
            st.write(website)

        price = (ticker.get_info()["currentPrice"])
        recc = (ticker.get_info()["recommendationKey"])

        st.subheader(f"The current price of {symbol} is ${price}.")
        st.subheader(f"It's current recommendation is {recc}!")

        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input("What is the start date?: ",
                                  value=(dt.datetime.now().date() - dt.timedelta(days=90)))

        with col2:
            end = st.date_input("What is the end date?: ")

        ticker_history = ticker.history(period="1d", start=start, end=end)

        col3, col4 = st.columns(2)

        with col3:
            selector = st.selectbox(label="Choose a parameter:", options=["Open", "Close", "Volume"])

        with col4:
            selector2 = st.selectbox(label="Additional viewing options:", options=["Coming Soon"])

        if selector == "Open":
            st.line_chart(ticker_history.Open)
        elif selector == "Close":
            st.line_chart(ticker_history.Close)
        elif selector == "Volume":
            st.line_chart(ticker_history.Volume)
        else:
            st.write("Awaiting input...")
    else:
        "Eagerly awaiting Input..."
except FileNotFoundError:
    st.subheader("Hmm...We can't find that ticker symbol...")
