"""
MDL YNOR QUANTUM - STRATEGY VIABILITY WRAPPER (MU ENGINE)
=========================================================
Architecture : Unified Risk/Return Governance
Definition of Quantum Mu for Finance:
Mu = Alpha (Sharpe) - Beta (Drawdown/Risk) - Kappa (Slippage/Friction)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging

class YnorQuantViability:
    def __init__(self, strategy_returns):
        self.returns = strategy_returns
        self.alpha = 0.0
        self.beta = 0.0
        self.kappa = 0.0
        self.mu = 0.0
        self.audit_log = []

    def compute_mu(self, risk_free_rate=0.0):
        """Map Finance Metrics to Ynor State Space (Alpha, Beta, Kappa)."""
        
        # 1. ALPHA (Gain / Reward) -> Using Sharpe Ratio as proxy for 'Pure Value'
        excess_returns = self.returns - risk_free_rate/252
        sharpe = (excess_returns.mean() / excess_returns.std()) * (252**0.5) if excess_returns.std() != 0 else 0
        self.alpha = max(0, sharpe)
        
        # 2. BETA (Cost / Entropy / Realized Loss) -> Max Drawdown as 'Dissipative Pressure'
        cum_ret = (1 + self.returns).cumprod()
        running_max = cum_ret.cummax()
        drawdown = (cum_ret - running_max) / running_max
        self.beta = abs(drawdown.min()) * 10 # Scaled for visibility
        
        # 3. KAPPA (Memory / Inertia / Friction) -> Portfolio Kurtosis/Skew or Transaction penalty
        # High Kurtosis = Heavy tails = Higher risk of memory trauma
        kurt = self.returns.kurtosis()
        self.kappa = (kurt / 10.0) if not np.isnan(kurt) else 0.1
        
        # FINAL VIABILITY
        self.mu = self.alpha - self.beta - self.kappa
        return self.mu

    def generate_audit_report(self):
        logging.info("--- MDL YNOR QUANTUM AUDIT ---")
        logging.info(f"ALPHA (Sharpe-Value): {self.alpha:.4f}")
        logging.info(f"BETA (Drawdown-Entropy): {self.beta:.4f}")
        logging.info(f"KAPPA (Fat-Tail Trauma): {self.kappa:.4f}")
        logging.info(f"MU (Systemic Viability): {self.mu:.4f}")
        
        if self.mu > 0.5:
            status = "SUPREME VIABILITY (INVESTABLE)"
        elif self.mu > 0:
            status = "CRITICAL STABILITY (WATCH)"
        else:
            status = "SYSTEMIC COLLAPSE (STOP TRADING)"
            
        logging.info(f"STATUS : {status}")
        return status

    def plot_mu_trajectory(self):
        """Simulate the Mu evolution through time."""
        # Rolling 60-day Mu
        window = 60
        mu_hist = []
        for i in range(window, len(self.returns)):
            slice_ret = self.returns.iloc[i-window:i]
            # Quick calc for rolling
            sr = (slice_ret.mean() / slice_ret.std()) * (252**0.5) if slice_ret.std() != 0 else 0
            dd = abs(((1+slice_ret).cumprod() / (1+slice_ret).cumprod().cummax() - 1).min())
            m = sr - (dd * 5) # simplified rolling mu
            mu_hist.append(m)
            
        plt.figure(figsize=(10, 5))
        plt.plot(mu_hist, color='#f43f5e', linewidth=2)
        plt.axhline(0, color='white', linestyle='--', alpha=0.5)
        plt.title("Ynor Quant Mu (Rolling 60d Systemic Viability)", color='white')
        plt.ylabel("Mu Score")
        plt.style.use('dark_background')
        plt.grid(True, alpha=0.1)
        plt.show()

if __name__ == "__main__":
    # Test with random returns
    test_rets = pd.Series(np.random.normal(0.0005, 0.01, 500))
    auditor = YnorQuantViability(test_rets)
    auditor.compute_mu()
    auditor.generate_audit_report()
    auditor.plot_mu_trajectory()
