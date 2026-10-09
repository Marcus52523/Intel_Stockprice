"""Build site/index.html: an interactive Intel (INTC) price chart in EUR.

Run:  python build_intel_page.py
Fetches 5 years of daily data and fills it into intel_template.html.
GitHub Actions runs this on a schedule and deploys site/ to GitHub Pages.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

HERE = Path(__file__).parent

intc_usd = yf.download("INTC", period="5y", progress=False, auto_adjust=True)["Close"].squeeze()
eurusd = yf.download("EURUSD=X", period="5y", progress=False)["Close"].squeeze()
eurusd = eurusd.reindex(intc_usd.index, method="ffill")
intc_eur = (intc_usd / eurusd).dropna()

data = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    "points": [[d.strftime("%Y-%m-%d"), round(float(v), 2)] for d, v in intc_eur.items()],
}

template = (HERE / "intel_template.html").read_text(encoding="utf-8")
out = HERE / "site" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(template.replace("__DATA__", json.dumps(data)), encoding="utf-8")
print(f"Wrote {out} ({len(data['points'])} days, latest {data['points'][-1]})")
