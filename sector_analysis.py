import pandas as pd
import matplotlib.pyplot as plt

SECTORS = {

"Technology":["ai","software","chip","semiconductor","nvidia","apple"],
"Energy":["oil","gas","opec","crude"],
"Financials":["bank","lending","credit","interest rate"],
"Healthcare":["drug","pharma","biotech","hospital"],
"Consumer":["retail","consumer","shopping"],
"Industrials":["manufacturing","construction","factory"]

}

def detect_sector(text):

    text = str(text).lower()

    for sector,words in SECTORS.items():

        for w in words:

            if w in text:
                return sector

    return "Other"


df = pd.read_csv("financial_news_scored.csv")

df["date"] = pd.to_datetime(df["publishedAt"]).dt.date

df["sector"] = df["text"].apply(detect_sector)

sector_ts = (
    df.groupby(["date","sector"])
    .agg(sentiment=("sentiment_score","mean"))
    .reset_index()
)

sector_ts["date"] = pd.to_datetime(sector_ts["date"])

for s in sector_ts["sector"].unique():

    subset = sector_ts[sector_ts["sector"]==s]

    plt.plot(subset["date"], subset["sentiment"], label=s)

plt.legend()

plt.title("Sector Sentiment Trends")

plt.show()

sector_ts.to_csv("sector_sentiment_timeseries.csv",index=False)

print("Bonus complete")