import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

df = pd.read_csv("financial_news_scored.csv")

df["date"] = pd.to_datetime(df["publishedAt"]).dt.date

daily = (
    df.groupby("date")
    .agg(sentiment=("sentiment_score","mean"))
    .reset_index()
)

daily["date"] = pd.to_datetime(daily["date"])

full_dates = pd.date_range(
    start=daily["date"].min(),
    end=daily["date"].max()
)

full = pd.DataFrame({"date": full_dates})

full = full.merge(daily,on="date",how="left")

full["sentiment"] = full["sentiment"].ffill()

full["rolling_sentiment"] = full["sentiment"].rolling(5).mean()

sp500 = yf.download("^GSPC", start=full["date"].min(), end=full["date"].max())

if isinstance(sp500.columns, pd.MultiIndex):
    sp500.columns = sp500.columns.get_level_values(0)

sp500 = sp500.reset_index()

sp500["date"] = pd.to_datetime(sp500["Date"])

sp500["return"] = sp500["Close"].pct_change()

merged = full.merge(sp500,on="date",how="left")

plt.figure(figsize=(10,5))

plt.plot(merged["date"], merged["rolling_sentiment"], label="Sentiment")

plt.plot(merged["date"], merged["return"], label="S&P500 Return")

plt.legend()

plt.title("Recession Sentiment vs Market")

plt.show()

merged.to_csv("sentiment_vs_market.csv",index=False)

print("Task 3 complete")