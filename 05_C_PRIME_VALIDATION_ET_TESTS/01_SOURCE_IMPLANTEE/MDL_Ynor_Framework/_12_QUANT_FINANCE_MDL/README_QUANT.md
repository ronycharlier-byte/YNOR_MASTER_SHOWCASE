# 🌌 MDL YNOR - QUANTUM LIQUIDITY DESK (V1.0)
> "Intelligence is the ultimate arbitrage. Risk is just unmanaged entropy."

Welcome to the **Quantum Finance AGI** module of the **MDL Ynor Architecture**. This suite implements, refines, and modernizes the quantitative strategies presented in the "Algorithmic Trading – Machine Learning & Quant Strategies" course, integrating them into the **Mu-Margin Viability Engine**.

## 🧠 Core Philosophy: The Financial Mu
Traditional finance measures Risk vs. Return. MDL Ynor measures **Viability (μ)**.
- **ALPHA (Value)**: Not just benchmark outperformance, but **Information Gain** per unit of compute. Derived from Sharpe Ratios and Prediction Premiums.
- **BETA (Dissipation)**: The energy lost to the market. Mapped to **Drawdowns** and **Volatility Spikes** (Systemic Entropy).
- **KAPPA (Memory/Entropy)**: The friction of the past. Mapped to **Fama-French Betas**, **Transaction Costs**, and **Liquidity Squeeze**.

$\mu = \text{Alpha} - \text{Beta} - \text{Kappa}$

---

## 🛠️ Module Architecture

### 📊 Strategy 1: S&P 500 Cluster Dynamics (`strategy_1_sp500_cluster_ml.py`)
- **Method**: Monthly K-Means clustering on 150 top liquid stocks.
- **Signal**: Anchored RSI centroids (Momentum vs. Mean Reversion).
- **Control**: Portfolio optimization (PyPortfolioOpt) for Max Sharpe.
- **Update**: Integrated with Fama-French 5-factor filtering for residual alpha.

### 🐦 Strategy 2: Social Sentiment Arbitrage (`strategy_2_sentiment_nasdaq.py`)
- **Method**: Twitter/X Engagement Ratio (Comments / Likes) on NASDAQ 100.
- **Signal**: Identifying "Organic Attention" vs. "Bot-Noise".
- **Execution**: Top-5 monthly rebalanced equal-weighted portfolio.
- **Update**: Includes synthetic data generator for "Zero-Latency" research demos.

### 📉 Strategy 3: Volatility Forecasting & Intraday Execution (`strategy_3_intraday_garch.py`)
- **Method**: GARCH(1,3) on 180-day daily log-returns.
- **Signal**: "Prediction Premium" detection (Standard deviation of GARCH-Var vs. Realized-Var).
- **Refinement**: 5-minute Intraday filters (RSI 20 + Bollinger Bands).
- **Update**: Automated EOD Exit logic to prevent overnight gap entropy.

---

## 🚀 How to Run (Quantum Protocol)

1.  **Prepare Environment**:
    Install specific quant dependencies:
    ```powershell
    pip install -r _12_QUANT_FINANCE_MDL/requirements_quant.txt
    ```

2.  **Execute Strategies**:
    Each script can be run independently for localized alpha research:
    - `python _12_QUANT_FINANCE_MDL/strategy_1_sp500_cluster_ml.py`
    - `python _12_QUANT_FINANCE_MDL/strategy_2_sentiment_nasdaq.py`
    - `python _12_QUANT_FINANCE_MDL/strategy_3_intraday_garch.py`

3.  **Audit Viability**:
    Run the `ynor_quant_wrapper.py` to see the **Mu-Margin** of your strategy.

---

## 📝 Compliance & Performance Monitoring
The **MDL Ynor Governance** layer monitors these scripts to ensure they don't enter an "Entropy Trap" (excessive drawdowns or transaction costs). If $\mu < 0$, the system recommends halting the execution.

*(c) 2026 Charlier Rony & The MDL Ynor Research Group*
