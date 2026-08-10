# LLM-Powered Financial News Sentiment Analysis

## Overview

This project develops an end-to-end Natural Language Processing (NLP) pipeline that analyses US financial news using Large Language Models (LLMs) to generate recession sentiment indicators.

The pipeline automates:

- Financial news collection
- Text preprocessing and cleaning
- AI-powered sentiment classification
- Time-series generation
- Comparison of sentiment trends against S&P 500 market returns
- Sector-level sentiment analysis

This project was developed to explore how AI can automate financial sentiment extraction and support data-driven economic analysis.

---

## Project Workflow

1. Collect financial news articles using NewsAPI.
2. Clean and preprocess article text.
3. Classify recession-related sentiment using the Hugging Face Inference API.
4. Convert sentiment into quantitative scores.
5. Generate daily sentiment time series.
6. Compare sentiment against S&P 500 returns.
7. Produce sector-level sentiment indicators.

---

## Technologies

- Python
- Pandas
- NewsAPI
- Hugging Face API
- REST APIs
- Natural Language Processing (NLP)
- Matplotlib
- yfinance

---

## Repository Structure

```text
data_collection.py
sentiment_analysis.py
timeseries_analysis.py
sector_analysis.py

financial_news_cleaned.csv
financial_news_scored.csv
daily_sentiment_timeseries.csv
sector_sentiment_timeseries.csv
sentiment_vs_market.csv
```

---

## Future Improvements

- Fine-tuned transformer models
- Explainable AI
- Interactive dashboard
- Cloud deployment
- Additional macroeconomic indicators
