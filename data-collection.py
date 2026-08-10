from newsapi import NewsApiClient
import pandas as pd
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(".env.py")

api_key = os.getenv("NEWSAPI_KEY")

if not api_key:
    raise ValueError("NEWSAPI_KEY not found in .env.py")

newsapi = NewsApiClient(api_key=api_key)


def clean_text(text):
    if text is None:
        return ""
    text = str(text)
    text = text.replace("\n"," ").replace("\r"," ")
    text = re.sub(r"\[\+\d+\schars\]","",text)
    text = re.sub(r"\s+"," ",text)
    return text.strip()


def fetch_articles_for_day(day):

    next_day = day + timedelta(days=1)

    query = (
        '("US economy" OR recession OR "Federal Reserve" OR inflation OR jobs)'
        ' AND (stocks OR equities OR "S&P 500" OR Nasdaq)'
    )

    all_articles = []

    for page in range(1,3):

        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            from_param=day.strftime("%Y-%m-%d"),
            to=next_day.strftime("%Y-%m-%d"),
            page_size=50,
            page=page
        )

        articles = response["articles"]

        if not articles:
            break

        all_articles.extend(articles)

    return all_articles


def collect_articles(days_back=21):

    today = datetime.utcnow().date()

    rows = []

    for i in range(days_back):

        day = today - timedelta(days=i)

        print("Fetching", day)

        articles = fetch_articles_for_day(day)

        for article in articles:

            title = clean_text(article.get("title"))
            desc = clean_text(article.get("description"))
            content = clean_text(article.get("content"))

            text = clean_text(title + " " + desc + " " + content)

            if len(text) < 80:
                continue

            rows.append({
                "source": article["source"]["name"],
                "title": title,
                "text": text,
                "url": article["url"],
                "publishedAt": article["publishedAt"]
            })

    df = pd.DataFrame(rows)

    df["publishedAt"] = pd.to_datetime(df["publishedAt"])

    df = df.drop_duplicates(subset=["text"])

    df = df.sort_values("publishedAt")

    df.to_csv("financial_news_cleaned.csv", index=False)

    print("Task 1 complete")
    print("Articles collected:", len(df))


if __name__ == "__main__":
    collect_articles()