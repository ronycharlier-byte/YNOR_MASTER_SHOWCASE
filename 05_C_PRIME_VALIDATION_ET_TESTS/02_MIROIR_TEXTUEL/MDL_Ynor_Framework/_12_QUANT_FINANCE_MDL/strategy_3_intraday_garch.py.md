# MIROIR TEXTUEL - strategy_3_intraday_garch.py

Source : MDL_Ynor_Framework\_12_QUANT_FINANCE_MDL\strategy_3_intraday_garch.py
Taille : 6740 octets
SHA256 : 56a95be7b11c751ff16ef3ae6f5cac1a355ccd18acebd63e6e1162742d367f9f

```text
"""
MDL YNOR QUANTUM - STRATEGY 3: INTRADAY GARCH + TECHNICAL SIGNALS
================================================================
Architecture : Volatility-Momentum Convergence
Core logic:
1. Daily Variance Forecast via GARCH(1,3)
2. Daily Signal: Detect volatility "Prediction Premium" (Anomalous variance)
3. Intraday Filter (5-min): RSI + Bollinger Bands Pattern Match
4. Entry Rule: Match Daily Volatility Bias + Intraday Overbought/Oversold
5. Execution: Enter at first intraday signal, exit at EOD close.
"""

import pandas as pd
import numpy as np
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
from arch import arch_model
from datetime import datetime
import logging

# --- CONFIGURATION MDL YNOR ---
logging.basicConfig(level=logging.INFO, format='YNOR_GARCH [%(levelname)s] - %(message)s')

class GarchIntradayEngine:
    def __init__(self, ticker="SPY"):
        self.ticker = ticker
        self.daily_df = None
        self.intraday_df = None
        self.results = None

    def get_data(self, start="2020-01-01"):
        logging.info(f"Downloading daily data for {self.ticker}...")
        # yfinance 0.2+ returns MultiIndex by default sometimes, adjust extraction
        raw_data = yf.download(self.ticker, start=start, auto_adjust=True)
        
        if isinstance(raw_data.columns, pd.MultiIndex):
            self.daily_df = raw_data['Close'].to_frame() # 'Close' is 'Adj Close' if auto_adjust=True
        else:
            self.daily_df = raw_data[['Close']]
            
        self.daily_df['log_return'] = np.log(self.daily_df['Close']).diff()
        
        # In a real-world scenario, you would use real intraday data. 
        # Here we mock 5-minute data for the demonstration as yfinance has short history for 5m.
        logging.info("Generating Mock 5-minute Intraday Data...")
        # (Assuming 78 bars of 5-min per trading day of 6.5 hours)
        dates = self.daily_df.index
        # Mocking OHLC for 5m
        intraday_list = []
        for d in dates:
            p_start = self.daily_df.loc[d, 'Close']
            # Simple walk for 78 bars
            for t in range(78):
                dt = d + pd.Timedelta(hours=9.5) + pd.Timedelta(minutes=5*t)
                # Random walk around daily price
                p_current = p_start * (1 + (np.random.normal(0, 0.001))) 
                intraday_list.append([dt, p_current, p_current*1.001, p_current*0.999, p_current, d])
        
        self.intraday_df = pd.DataFrame(intraday_list, columns=['datetime', 'open', 'high', 'low', 'close', 'date'])
        self.intraday_df.set_index('datetime', inplace=True)
        return self.daily_df, self.intraday_df

    def apply_garch_daily(self):
        logging.info("Running Rolling GARCH(1,3) Prediction...")
        # Variance calculation (rolling 6 months)
        self.daily_df['rolling_var'] = self.daily_df['log_return'].rolling(180).var()
        
        # Forecast Loop (Very slow, we sample every 5 days for speed)
        def predict_volatility(x):
            if x.isna().any(): return np.nan
            model = arch_model(x, p=1, q=3, vol='GARCH', dist='normal')
            res = model.fit(update_freq=0, disp="off")
            forecast = res.forecast(horizon=1).variance.iloc[-1, 0]
            return forecast
            
        # Optimization: We'll do it on a slice for the demo
        self.daily_df['garch_predict'] = self.daily_df['log_return'].rolling(180).apply(predict_volatility)
        
        # Signal Generation
        self.daily_df['prediction_premium'] = (self.daily_df['garch_predict'] - self.daily_df['rolling_var']) / self.daily_df['rolling_var']
        self.daily_df['premium_std'] = self.daily_df['prediction_premium'].rolling(180).std()
        
        # Rule: 1 if premium > 1.5 sigma, -1 if < -1.5 sigma
        def daily_signal_rule(row):
            if row['prediction_premium'] > 1.5 * row['premium_std']: return 1
            if row['prediction_premium'] < -1.5 * row['premium_std']: return -1
            return 0
        
        self.daily_df['signal_daily'] = self.daily_df.apply(daily_signal_rule, axis=1).shift(1)
        return self.daily_df

    def process_intraday_signals(self):
        logging.info("Processing Intraday (5-min) Filters (RSI/Bollinger)...")
        df = self.intraday_df.copy()
        
        # RSI 20
        df['rsi'] = ta.rsi(df['close'], length=20)
        
        # Bollinger Bands
        bb = ta.bbands(df['close'], length=20)
        df['bbu'] = bb['BBU_20_2.0']
        df['bbl'] = bb['BBL_20_2.0']
        
        # Signal Matching: 
        # Daily == 1 (High Forecast Vol) -> Short if Overbought (RSI > 70 & close > BBU)
        # Daily == -1 (Low Forecast Vol) -> Long if Oversold (RSI < 30 & close < BBL)
        
        # Merge daily signals into intraday
        df = df.merge(self.daily_df[['signal_daily']], left_on='date', right_index=True)
        
        df['signal_pos'] = 0
        df.loc[(df['signal_daily'] == 1) & (df['rsi'] > 70) & (df['close'] > df['bbu']), 'signal_pos'] = -1
        df.loc[(df['signal_daily'] == -1) & (df['rsi'] < 30) & (df['close'] < df['bbl']), 'signal_pos'] = 1
        
        # EOD Rule: First signal of day defines position sign, hold until EOD.
        # Group by date, find first non-zero, ffill.
        def daily_carry(x):
            first_sig = x[x != 0].head(1)
            if not first_sig.empty:
                val = first_sig.values[0]
                return pd.Series(val, index=x.index)
            return pd.Series(0, index=x.index)
            
        df['final_position'] = df.groupby('date')['signal_pos'].apply(daily_carry).reset_index(level=0, drop=True)
        
        # Returns
        df['ret'] = df['close'].pct_change()
        df['strat_ret'] = df['ret'] * df['final_position'].shift(1)
        
        self.results = df.groupby('date')['strat_ret'].sum()
        return self.results

    def plot_performance(self):
        if self.results is None: return
        
        cum_ret = (1 + self.results).cumprod() - 1
        
        plt.figure(figsize=(12, 6))
        plt.plot(cum_ret, label=f'MDL Ynor GARCH Strategy ({self.ticker})', color='#f43f5e', linewidth=2)
        plt.title("Quantum Volatility Forecasting - GARCH + Intraday Filters", fontsize=14)
        plt.ylabel("Cumulative Returns")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    # Note: Running actual GARCH OLS on 1000 days is compute-heavy.
    engine = GarchIntradayEngine()
    # Limit data for faster demo execution
    engine.get_data(start="2023-01-01")
    engine.apply_garch_daily()
    engine.process_intraday_signals()
    engine.plot_performance()

```