# MIROIR TEXTUEL - strategy_1_sp500_cluster_ml.py

Source : MDL_Ynor_Framework\_12_QUANT_FINANCE_MDL\strategy_1_sp500_cluster_ml.py
Taille : 10496 octets
SHA256 : 9dac72410bbdb3add0e7fd8c00b866fde49c27fd5df098f736e69a1956376cd1

```text
"""
MDL YNOR QUANTUM - STRATEGY 1: S&P 500 + K-MEANS + PORTFOLIO OPTIMIZED
====================================================================
Principal Investigatorure : AGI-Managed Quantitative Strategy
Core logic: 
1. Daily data ingestion (yfinance)
2. Hybrid Feature Engineering (Technical + Fama-French + Momentum)
3. Monthly K-Means Clustering (Fixed Centroids for RSI control)
4. Portfolio Optimization (Max Sharpe via PyPortfolioOpt)
5. Backtest Loop with Transaction Logic
"""

import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from pypfopt import expected_returns, risk_models, EfficientFrontier
import pandas_datareader.data as web
import logging
import warnings

# --- CONFIGURATION MDL YNOR ---
logging.basicConfig(level=logging.INFO, format='YNOR_QUANT [%(levelname)s] - %(message)s')
warnings.filterwarnings('ignore')

def get_sp500_tickers():
    """Scrape S&P 500 tickers from Wikipedia and fix formatting for yfinance."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    table = pd.read_html(url)[0]
    tickers = table['Symbol'].tolist()
    # Replace dots with dashes for yfinance (e.g. BRK.B -> BRK-B)
    tickers = [t.replace('.', '-') for t in tickers]
    return tickers

def calculate_garman_klass_vol(df):
    """Calculate Garman-Klass volatility proxy."""
    return ((np.log(df['High']) - np.log(df['Low']))**2) / 2 - (2*np.log(2)-1) * ((np.log(df['Adj Close']) - np.log(df['Open']))**2)

class Sp500QuantEngine:
    def __init__(self, start_date="2018-01-01", end_date=None):
        self.start_date = start_date
        self.end_date = end_date or datetime.now().strftime("%Y-%m-%d")
        self.tickers = get_sp500_tickers()
        self.data = None
        self.features = None
        self.portfolio_results = None

    def download_data(self):
        logging.info(f"Downloading data for {len(self.tickers)} S&P 500 tickers...")
        # Note: auto_adjust=True for consistent column naming
        raw_data = yf.download(self.tickers, start=self.start_date, end=self.end_date, interval="1d", auto_adjust=True)
        
        # If returns a MultiIndex, stack it to get [date, ticker] rows
        if isinstance(raw_data.columns, pd.MultiIndex):
            self.data = raw_data.stack(future_stack=True) # Supporting pandas 2.0+
        else:
            self.data = raw_data
            
        self.data.index.names = ['date', 'ticker']
        # Normalize column names
        self.data.columns = [c.lower().replace(' ', '_') for c in self.data.columns]
        return self.data

    def feature_engineering(self):
        logging.info("Engineering technical indicators and features...")
        df = self.data.copy()
        
        # Garman-Klass Volatility
        df['volatility_gk'] = calculate_garman_klass_vol(df)
        
        # RSI 20
        df['rsi'] = df.groupby(level=1)['adj_close'].transform(lambda x: ta.rsi(x, length=20))
        
        # Bollinger Bands
        def calc_bb(x):
            bb = ta.bbands(np.log1p(x), length=20)
            if bb is not None:
                # Normalization (close - low) / (high - low)
                return (np.log1p(x) - bb['BBL_20_2.0']) / (bb['BBU_20_2.0'] - bb['BBL_20_2.0'])
            return np.nan
        df['bb_normalized'] = df.groupby(level=1)['adj_close'].transform(calc_bb)
        
        # ATR 14 (Normalized by price)
        def calc_atr(x):
            # x is a sub-dataframe per ticker
            atr = ta.atr(x['high'], x['low'], x['close'], length=14)
            return atr / x['close'] if atr is not None else np.nan
        
        # Note: atr requires high/low/close. Groupby.apply is safer here
        df['atr_norm'] = df.groupby(level=1).apply(lambda x: ta.atr(x['high'], x['low'], x['close'], length=14) / x['close']).reset_index(level=0, drop=True)
        
        # MACD (Signal line normalization)
        def calc_macd(x):
            m = ta.macd(x, fast=12, slow=26, signal=9)
            if m is not None:
                return m['MACD_12_26_9'] / m['MACDs_12_26_9']
            return np.nan
        df['macd_norm'] = df.groupby(level=1)['adj_close'].transform(calc_macd)
        
        # Dollar Volume
        df['dollar_volume'] = (df['adj_close'] * df['volume']) / 1e6
        
        # Monthly Resampling
        last_cols = ['adj_close', 'rsi', 'bb_normalized', 'atr_norm', 'macd_norm', 'volatility_gk']
        monthly_df = df.groupby([pd.Grouper(level=0, freq='M'), 'ticker'])[last_cols].last()
        monthly_df['dollar_volume'] = df.groupby([pd.Grouper(level=0, freq='M'), 'ticker'])['dollar_volume'].mean()
        
        # Filtering Liquidity (Top 150)
        monthly_df['dv_rank'] = monthly_df.groupby(level=0)['dollar_volume'].transform(lambda x: x.rank(ascending=False))
        monthly_df = monthly_df[monthly_df['dv_rank'] <= 150].drop(columns=['dv_rank', 'dollar_volume'])
        
        # Momentum Features (Return horizons)
        outlier_cutoff = 0.005
        for h in [1, 2, 3, 6, 9, 12]:
            monthly_df[f'return_{h}m'] = monthly_df.groupby(level=1)['adj_close'].pct_change(h)
            # Clip outliers
            q_low = monthly_df[f'return_{h}m'].quantile(outlier_cutoff)
            q_high = monthly_df[f'return_{h}m'].quantile(1-outlier_cutoff)
            monthly_df[f'return_{h}m'] = monthly_df[f'return_{h}m'].clip(q_low, q_high)
            
        self.features = monthly_df.dropna()
        return self.features

    def get_fama_french_betas(self):
        logging.info("Downloading Fama-French factors and calculating rolling betas...")
        try:
            # Get monthly FF factors
            factors = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench', start=self.start_date)[0]
            factors.index = factors.index.to_timestamp()
            factors = factors / 100
            return factors
        except Exception as e:
            logging.warning(f"Fama-French data fetching failed: {e}. Using proxy factors.")
            # Mock factors for demonstration
            dates = pd.date_range(self.start_date, periods=24, freq='M')
            factors = pd.DataFrame(np.random.normal(0, 0.02, (len(dates), 5)), 
                                   index=dates, columns=['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA'])
            return factors

    def apply_clustering(self):
        logging.info("Applying Anchored K-Means Clustering...")
        # We want to force cluster 3 to be "High RSI" (Overbought/Momentum)
        def get_clusters(df_month):
            if len(df_month) < 4: return df_month
            
            # Target centroids for RSI: [30, 45, 55, 70]
            # Since we have ~18 features, we initialize a (4, n_features) matrix with zeros
            n_features = df_month.shape[1]
            init_centroids = np.zeros((4, n_features))
            rsi_idx = df_month.columns.get_loc('rsi')
            init_centroids[:, rsi_idx] = [30, 45, 55, 70]
            
            km = KMeans(n_clusters=4, init=init_centroids, n_init=1, random_state=0)
            df_month['cluster'] = km.fit_predict(df_month)
            return df_month
        
        self.features = self.features.groupby(level=0, group_keys=False).apply(get_clusters)
        return self.features

    def run_backtest(self):
        logging.info("Starting Portoflio Optimization Backtest...")
        # Filter for Cluster 3 (High Momentum)
        universe = self.features[self.features['cluster'] == 3]
        
        all_dates = universe.index.get_level_values(0).unique()
        portfolio_returns = []
        
        for date in all_dates:
            tickers_month = universe.loc[date].index.tolist()
            if not tickers_month: continue
            
            # Get historical daily prices for these tickers (last 12 months for covariance)
            start_opt = date - pd.DateOffset(months=12)
            end_opt = date - pd.DateOffset(days=1)
            
            try:
                # We need prices from self.data (unstacked)
                prices_df = self.data['adj_close'].unstack()[tickers_month].loc[start_opt:end_opt].dropna(axis=1)
                if prices_df.empty or prices_df.shape[1] < 2: 
                    # Fallback to equal weight
                    weights = {t: 1.0/len(tickers_month) for t in tickers_month}
                else:
                    mu = expected_returns.mean_historical_return(prices_df)
                    S = risk_models.sample_cov(prices_df)
                    ef = EfficientFrontier(mu, S)
                    weights = ef.max_sharpe()
                    weights = ef.clean_weights()
                
                # Calculate next month performance
                next_start = date + pd.DateOffset(days=1)
                next_end = date + pd.DateOffset(months=1)
                next_returns = self.data['adj_close'].unstack()[list(weights.keys())].loc[next_start:next_end].pct_change().dropna()
                
                # Weighted daily returns
                daily_perf = (next_returns * pd.Series(weights)).sum(axis=1)
                portfolio_returns.append(daily_perf)
                
            except Exception as e:
                logging.warning(f"Optimization failed for {date}: {e}")
                
        self.portfolio_results = pd.concat(portfolio_returns)
        return self.portfolio_results

    def plot_performance(self):
        if self.portfolio_results is None: return
        # Cumulative performance
        cum_ret = (1 + self.portfolio_results).cumprod() - 1
        
        # Benchmark (SPY)
        spy = yf.download("SPY", start=self.start_date, end=self.end_date)['Adj Close'].pct_change()
        cum_spy = (1 + spy).cumprod() - 1
        
        plt.figure(figsize=(12, 6))
        plt.plot(cum_ret, label='MDL Ynor Cluster Strategy', color='#22c55e', linewidth=2)
        plt.plot(cum_spy, label='S&P 500 (SPY) Buy & Hold', color='#a1a1aa', linestyle='--')
        plt.title("Quantum Performance - Cluster-Based Portfolio Optimization", fontsize=14)
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    engine = Sp500QuantEngine(start_date="2020-01-01")
    engine.download_data()
    engine.feature_engineering()
    engine.apply_clustering()
    engine.run_backtest()
    engine.plot_performance()

```