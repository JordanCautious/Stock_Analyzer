import yfinance as yf
import streamlit as st
import datetime as dt

# Hello! Welcome to my first project! Ideally, this code will change over time as I learn more about Python!

st.set_page_config(
     page_title="Jordan's Stock Analyzer",
     # page_icon="🧊",
     layout="wide",
     # initial_sidebar_state="expanded",
)

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
        st.markdown(f"You have chosen **{symbol}**. Here's some relevant information: ")

        ticker = yf.Ticker(symbol)

        image_url = ticker.get_info()["logo_url"]
        st.image(image=image_url)

        # Introduces a bunch of variables that will be used in the following lines of code.
        sector = ticker.get_info()["sector"]
        industry = ticker.get_info()["industry"]
        ticker_name = ticker.get_info()["shortName"]
        beta = ticker.info["beta"]
        market_cap = ticker.get_info()["marketCap"]

        # This chunk of code uses the variables we previously created above.
        st.write(ticker_name)
        st.markdown(f"**{symbol}** is in the '{sector}' sector and '{industry}' industry.")
        st.markdown(f"It has a **beta** of {beta} and a **market cap** of ${market_cap:,}!")
        website = ticker.get_info()["website"]
        with st.expander("Associated Website"):
            st.write(website)

        # A few variables needed for the following lines.
        price = (ticker.get_info()["currentPrice"])
        recc = (ticker.get_info()["recommendationKey"])

        st.markdown(f"##### {symbol} has a current price of: ${round(price,2)}")
        st.markdown(f"##### Recommendation: {recc.upper()}!")

        st.markdown("""
        ---
        """)

        # Returns the closing stock price from the last seven days, or 5 trading days.
        seven_days = ticker.history(period="1h", start=(dt.datetime.now().date() - dt.timedelta(days=7)))

        # This code helps generate the 5 previous closing prices.
        st.markdown(f"##### Previous 5 closing prices for {ticker_name} (DESC):")
        for i in seven_days.Close:
            st.markdown(f"###### ${round(i,2)}")

        st.markdown("""
        ---
        """)

        # Created 2 columns for start and end date.
        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input("What is the start date for Volume?: ",
                                  value=(dt.datetime.now().date() - dt.timedelta(days=30)))

        with col2:
            end = st.date_input("What is the end date for Volume?: ")

        # This block of code is ideally for a variety of parameters.
        col3, col4 = st.columns(2)

        selector = st.selectbox(label="Choose a parameter:", options=["Stock Price", "Volume"])

        ticker_history = ticker.history(period="1d", start=start, end=end)

        # This code block is dependent upon the number of parameters created.
        if selector == "Volume":
            st.line_chart(ticker_history.Volume)
        elif selector == "Stock Price":
            # Returns the value of a stock on a certain day
            start1 = st.date_input("Find out the price of the stock on a certain day:")
            st.write(f"You chose {start1}!")
            # This code basically returns the stock price from a specified day.
            try:
                single_price = (ticker.history(period="1d", start=start1, end=(start1 + dt.timedelta(days=1))).Close[0])
                st.subheader(f"The price was: ${round(single_price, 2)}")
            except IndexError:
                st.write("There seemed to be an error in calculating this. Please choose a different date")
        else:
            st.write("Awaiting input...")

    else:
        "Eagerly awaiting Input..."
except FileNotFoundError:
    st.subheader("Hmm...We can't find that ticker symbol...")
