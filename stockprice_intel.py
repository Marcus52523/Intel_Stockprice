"""Plot the Intel (INTC) share price in euros.

Run:  python stockprice_intel.py
"""
import matplotlib.pyplot as plt
import yfinance as yf

PERIOD = "1y"  # e.g. "1mo", "6mo", "1y", "5y", "max"

# Intel closes in USD and the EUR/USD rate (USD per 1 EUR)
intc_usd = yf.download("INTC", period=PERIOD, progress=False, auto_adjust=True)["Close"].squeeze()
eurusd = yf.download("EURUSD=X", period=PERIOD, progress=False)["Close"].squeeze()

# Align the FX rate to the stock's trading days and convert USD -> EUR
eurusd = eurusd.reindex(intc_usd.index, method="ffill")
intc_eur = (intc_usd / eurusd).dropna()

latest = intc_eur.iloc[-1]
print(f"Latest Intel price: {latest:.2f} EUR ({intc_eur.index[-1]:%Y-%m-%d})")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(intc_eur.index, intc_eur.values, color="#0071C5", linewidth=1.8)
ax.set_title(f"Intel (INTC) share price in EUR, last {PERIOD} - latest {latest:.2f} EUR")
ax.set_ylabel("Price (EUR)")
ax.grid(alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
plt.show()
