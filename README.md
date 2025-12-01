# Portfolio-Calculations
A Python project for Indian stock portfolio analysis using Jugaad Data. It downloads NSE prices, computes daily returns, annualized return &amp; volatility, and builds an annualized covariance matrix. Uses these to calculate portfolio return and risk for any weight allocation.
This project demonstrates a complete workflow for portfolio return, risk, and optimization analysis using historical stock data from the National Stock Exchange (NSE). The focus is on building a clean, modular, and transparent process for calculating returns, volatility, covariance matrices, and portfolio metrics, specifically tailored for Indian financial markets.

1. Data Collection (Jugaad Data – NSE)

We start by fetching historical daily closing prices for selected Indian stocks using the Jugaad Data NSE API, a reliable and developer-friendly source for real market data. The downloaded prices are aligned by date and stored in a consolidated DataFrame, setting the foundation for further analysis.

2. Daily Returns Calculation

Using the adjusted close prices, the project computes daily percentage returns, which represent the day-to-day changes in stock prices. These returns are essential inputs for measuring risk, performance, and portfolio behavior.

3. Annualized Return and Volatility (Standalone Computation)

To ensure clarity and reusability, we compute the following as separate explicit lines of code:

Annualized Return
Calculated using geometric compounding of average daily returns, assuming 252 trading days.

Annualized Volatility
Obtained by scaling the daily standard deviation with the square root of 252.

These independent calculations make the code intuitive and easy to extend when analyzing additional assets.

4. Covariance Matrix Construction

We compute the annualized covariance matrix from the daily returns. This matrix represents how stocks move relative to each other and is a key component in portfolio risk estimation. It is later used to calculate the variance and volatility of any portfolio allocation.

5. Portfolio Return & Volatility

Using the annualized returns and covariance matrix, the project computes:

Portfolio Expected Return

Portfolio Annualized Volatility

Both metrics are derived from weighted combinations of individual asset statistics, allowing users to test different portfolio allocations and risk–return profiles.
