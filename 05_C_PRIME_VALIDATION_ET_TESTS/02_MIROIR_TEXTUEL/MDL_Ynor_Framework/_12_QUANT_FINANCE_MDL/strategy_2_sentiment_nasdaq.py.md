# MIROIR TEXTUEL - strategy_2_sentiment_nasdaq.py

Source : MDL_Ynor_Framework\_12_QUANT_FINANCE_MDL\strategy_2_sentiment_nasdaq.py
Taille : 5804 octets
SHA256 : d79a704ba83a2c2362c03f9bda606a264d77cd99cf675bbf1d515f8800f5dfc8

```text
"""
MDL YNOR QUANTUM - STRATEGY 2: TWITTER SENTIMENT (ENGAGEMENT RATIO)
==================================================================
Principal Investigatorure : Sentiment-Driven Alpha Extraction
Core logic:
1. Load social media metrics (Likes, Comments, Sentiment)
2. Filter for significant engagement (Noise Reduction)
3. Calculate Engagement Ratio (Comments / Likes)
4. Rank Top-5 Tickers Monthly
5. Monthly Rebalanced Equal-Weighted Portfolio
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import logging

# --- CONFIGURATION MDL YNOR ---
logging.basicConfig(level=logging.INFO, format='YNOR_SENTIMENT [%(levelname)s] - %(message)s')

class SentimentQuantEngine:
    def __init__(self, tickers=None):
        # Default to NASDAQ-100 sample
        self.tickers = tickers or ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'PYPL', 'NFLX', 'INTC']
        self.sentiment_df = None
        self.prices_df = None
        self.results = None

    def generate_synthetic_data(self, start_date="2022-01-01", end_date="2023-12-31"):
        """Create a mock CSV that follows the structure described in the video transcription."""
        logging.info("Generating Synthetic Sentiment Data for demonstration...")
        dates = pd.date_range(start_date, end_date, freq='D')
        data = []
        for d in dates:
            for s in self.tickers:
                # Random metrics representing Twitter activity
                posts = np.random.randint(5, 50)
                comments = np.random.randint(5, 100)
                likes = np.random.randint(10, 500)
                impressions = np.random.randint(100, 10000)
                sentiment = np.random.uniform(-0.5, 0.8)
                
                # Introduce structural bias (e.g. NVDA has high engagement and high returns)
                if s == 'NVDA':
                    likes += 200
                    comments += 50
                
                data.append([d, s, posts, comments, likes, impressions, sentiment])
        
        self.sentiment_df = pd.DataFrame(data, columns=['date', 'symbol', 'twitter_posts', 'twitter_comments', 'twitter_likes', 'twitter_impressions', 'twitter_sentiment'])
        self.sentiment_df.set_index(['date', 'symbol'], inplace=True)
        return self.sentiment_df

    def download_prices(self):
        logging.info(f"Downloading daily prices for {len(self.tickers)} symbols...")
        # Using auto_adjust=True for consistent 'Close' column regardless of yfinance version
        df = yf.download(self.tickers, start=self.sentiment_df.index.get_level_values(0).min(), 
                         end=self.sentiment_df.index.get_level_values(0).max(), auto_adjust=True)
        
        if isinstance(df.columns, pd.MultiIndex):
            self.prices_df = df['Close']
        else:
            self.prices_df = df[['Close']]
        return self.prices_df

    def build_signals(self):
        logging.info("Calculating Engagement Ratio and Ranking...")
        df = self.sentiment_df.copy()
        
        # Engagement Ratio logic from Video
        df['engagement_ratio'] = df['twitter_comments'] / df['twitter_likes']
        
        # Filter noise
        df = df[(df['twitter_likes'] > 20) & (df['twitter_comments'] > 10)]
        
        # Monthly Aggregation (Mean Engagement)
        df_monthly = df.groupby([pd.Grouper(level=0, freq='M'), 'symbol'])['engagement_ratio'].mean().to_frame()
        
        # Rank Cross-Sectionally
        df_monthly['rank'] = df_monthly.groupby(level=0)['engagement_ratio'].transform(lambda x: x.rank(ascending=False))
        
        # Select Top 5
        self.signals = df_monthly[df_monthly['rank'] <= 5]
        return self.signals

    def run_backtest(self):
        logging.info("Starting monthly rebalanced backtest (Equal Weighted)...")
        returns = self.prices_df.pct_change()
        
        all_months = self.signals.index.get_level_values(0).unique()
        monthly_returns = []
        
        for month in all_months:
            top_tickers = self.signals.loc[month].index.tolist()
            if not top_tickers: continue
            
            # Start of next month
            start_date = month + pd.DateOffset(days=1)
            end_date = month + pd.DateOffset(months=1)
            
            # Equal weight (1 / 5)
            monthly_perf = returns.loc[start_date:end_date, top_tickers].mean(axis=1)
            monthly_returns.append(monthly_perf)
            
        self.results = pd.concat(monthly_returns).dropna()
        return self.results

    def plot(self):
        if self.results is None: return
        
        # Cumulative Strategy
        strat_cum = (1 + self.results).cumprod() - 1
        
        # Benchmark (NASDAQ-100 Proxy)
        qqq_df = yf.download("QQQ", start=self.results.index.min(), end=self.results.index.max(), auto_adjust=True)
        if isinstance(qqq_df.columns, pd.MultiIndex):
            qqq = qqq_df['Close'].pct_change()
        else:
            qqq = qqq_df['Close'].pct_change()
        qqq_cum = (1 + qqq).cumprod() - 1
        
        plt.figure(figsize=(12, 6))
        plt.plot(strat_cum, label='MDL Sentiment Strategy (Top 5 Engagement)', color='#3b82f6', linewidth=2)
        plt.plot(qqq_cum, label='NASDAQ-100 (QQQ) Benchmark', color='#a1a1aa', linestyle='--')
        plt.title("Quantum Sentiment Backtest - Engagement Ratio Ranking", fontsize=14)
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    engine = SentimentQuantEngine()
    engine.generate_synthetic_data()
    engine.download_prices()
    engine.build_signals()
    engine.run_backtest()
    engine.plot()

```