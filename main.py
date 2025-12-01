# ------------------------------------------------------
# IMPORTS 
# ------------------------------------------------------
import pandas as pd
import numpy as np
from datetime import date, timedelta
from jugaad_data.nse import stock_df, NSELive


# ======================================================
# ==============  CAPITAL & WEIGHT SECTION  ============
# ======================================================

# Total capital
M = 100000  # example: 1 lakh

# Investment amounts
N1 = 60000   # investment in asset 1
N2 = M - N1  # investment in asset 2

# Calculate weights
w1 = N1 / M
w2 = N2 / M  # or 1 - w1

print("Total Capital (M):", M)
print("Investment in Asset 1 (N1):", N1)
print("Investment in Asset 2 (N2):", N2)

print("\nPortfolio Weights:")
print("Weight of Asset 1 (w1):", round(w1, 4))
print("Weight of Asset 2 (w2):", round(w2, 4))


# ======================================================
# ===============  HISTORICAL DATA SECTION  =============
# ======================================================

# Function to get historical stock data
def get_stock(symbol, start, end):
    df = stock_df(symbol=symbol, from_date=start, to_date=end, series="EQ")
    df = df[["DATE", "CLOSE"]]
    df["DATE"] = pd.to_datetime(df["DATE"])
    df.set_index("DATE", inplace=True)
    return df

# Download data for INFY, TCS, HDFCBANK
start = date(2023, 1, 1)
end   = date(2023, 12, 31)

symbols = ["INFY", "TCS", "HDFCBANK"]

df_list = []
for sym in symbols:
    d = get_stock(sym, start, end)
    d["symbol"] = sym
    df_list.append(d)

df = pd.concat(df_list).reset_index()

# ======================================================
# ================= DAILY RETURN SECTION ================
# ======================================================

df["return"] = df.groupby("symbol")["CLOSE"].pct_change()
df = df.dropna()

# Mean daily returns
mean_returns = df.groupby("symbol")["return"].mean()
print("------COMPUTING PORTFOLIO RETURNS------")
print("Mean daily returns:\n", mean_returns, "\n")


# Portfolio Weights (INFY, TCS, HDFCBANK)
weights = np.array([0.3, 0.4, 0.3])
returns = mean_returns.values


# A) Two-asset return formula
w1, w2 = 0.6, 0.4
r1 = mean_returns["INFY"]
r2 = mean_returns["TCS"]

Rp_two = w1*r1 + w2*r2
print("Two-asset portfolio return:", Rp_two)


# B) Summation form
Rp_sum = sum(w * r for w, r in zip(weights, returns))
print("Summation form return:", Rp_sum)


# C) Vector/matrix form
Rp_matrix = np.dot(weights, returns)
print("Matrix/vector form return:", Rp_matrix)


# ======================================================
# ===============  PORTFOLIO VOLATILITY  ===============
# ======================================================

print("\n------COMPUTING PORTFOLIO VOLATILITY------")

# Standard deviations for each stock
std_devs = df.groupby("symbol")["return"].std()
sigmas = std_devs.values

# Correlation matrix
corr_matrix = df.pivot(index="DATE", columns="symbol", values="return").corr().values

# Covariance matrix
cov_matrix = df.pivot(index="DATE", columns="symbol", values="return").cov().values


# A) Two-asset volatility
sigma1 = std_devs["INFY"]
sigma2 = std_devs["TCS"]
rho12  = corr_matrix[symbols.index("INFY")][symbols.index("TCS")]

var_two = w1**2 * sigma1**2 + w2**2 * sigma2**2 + 2*w1*w2*rho12*sigma1*sigma2
print("Two-asset portfolio variance:", var_two)
print("Two-asset portfolio volatility:", np.sqrt(var_two))


# B) Multi-asset volatility
N = len(symbols)
first_sum = sum(weights[i]**2 * sigmas[i]**2 for i in range(N))

second_sum = 0
for i in range(N):
    for j in range(i+1, N):
        second_sum += weights[i]*weights[j]*corr_matrix[i][j]*sigmas[i]*sigmas[j]

multi_var = first_sum + 2*second_sum
print("\nMulti-asset portfolio variance:", multi_var)
print("Multi-asset portfolio volatility:", np.sqrt(multi_var))


# C) Matrix form volatility
matrix_var = float(weights.T @ cov_matrix @ weights)
print("\nMatrix form variance:", matrix_var)
print("Matrix form volatility:", np.sqrt(matrix_var))


# ======================================================
# =========  ANNUALIZED RETURN & VOLATILITY  ===========
# ======================================================

print("\n------ ANNUALIZED METRICS (Using Daily Returns) ------")

# 252 trading days in India
trading_days = 252

# Annualized returns
annualized_returns = mean_returns * trading_days
print("\nAnnualized Returns (each stock):")
print(annualized_returns)

# Annualized volatility
daily_volatility = std_devs
annualized_volatility = daily_volatility * np.sqrt(trading_days)
print("\nAnnualized Volatility (each stock):")
print(annualized_volatility)

# Annualized portfolio return
annualized_port_return = Rp_matrix * trading_days
print("\nAnnualized Portfolio Return:", annualized_port_return)

# Annualized portfolio volatility
daily_port_vol = np.sqrt(matrix_var)
annualized_port_vol = daily_port_vol * np.sqrt(trading_days)
print("Annualized Portfolio Volatility:", annualized_port_vol)
