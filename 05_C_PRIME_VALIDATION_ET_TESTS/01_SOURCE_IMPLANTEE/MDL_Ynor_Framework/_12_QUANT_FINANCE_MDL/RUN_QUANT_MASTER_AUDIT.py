"""
MDL YNOR QUANTUM - MASTER ORCHESTRATOR & AUDIT (V1)
===================================================
Architecture : Global Portfolio Governance
Runs all active strategies and performs a Mu-Margin viability audit.
"""

import pandas as pd
import numpy as np
import logging
import sys
import os

# Import local strategies and the wrapper
try:
    from strategy_2_sentiment_nasdaq import SentimentQuantEngine
except ImportError:
    SentimentQuantEngine = None

try:
    from strategy_3_intraday_garch import GarchIntradayEngine
except ImportError:
    GarchIntradayEngine = None

from ynor_quant_wrapper import YnorQuantViability

# --- CONFIGURATION MDL YNOR ---
logging.basicConfig(level=logging.INFO, format='YNOR_QUANT_MASTER [%(levelname)s] - %(message)s')

def run_master_audit():
    print("=========================================================")
    print(" 🛡️ MDL YNOR - QUANTUM FINANCE MASTER AUDIT CENTER (V2) 🛡️")
    print("=========================================================\n")
    
    all_returns = []

    # 1. Start Strategy 2 (Twitter Sentiment)
    if SentimentQuantEngine:
        print("[STEP 1/4] Launching 'Twitter Sentiment NASDAQ 100'...")
        try:
            strat_2 = SentimentQuantEngine()
            strat_2.generate_synthetic_data()
            strat_2.download_prices()
            strat_2.build_signals()
            returns_2 = strat_2.run_backtest()
            print(f" -> Strategy 2 completed. {len(returns_2)} data points.\n")
            all_returns.append(returns_2)
        except Exception as e:
            print(f" -> Strategy 2 FAILED: {e}\n")
    else:
        print("[STEP 1/4] Strategy 2 SKIPPED (Dependencies missing)\n")

    # 2. Start Strategy 3 (GARCH Intraday)
    if GarchIntradayEngine:
        print("[STEP 2/4] Launching 'Intraday GARCH SPY'...")
        try:
            strat_3 = GarchIntradayEngine()
            strat_3.get_data(start="2023-01-01")
            strat_3.apply_garch_daily()
            returns_3 = strat_3.process_intraday_signals()
            print(f" -> Strategy 3 completed. {len(returns_3)} data points.\n")
            all_returns.append(returns_3)
        except Exception as e:
            print(f" -> Strategy 3 FAILED: {e}\n")
    else:
        print("[STEP 2/4] Strategy 3 SKIPPED (Dependencies missing: 'arch')\n")
    
    # 3. Perform Mu Audit
    if not all_returns:
        print("❌ NO DATA ACQUIRED. AUDIT CANNOT PROCEED.")
        return

    print("[STEP 3/4] Calculating Systemic Viability (Mu-Margin)...")
    ensemble_returns = pd.concat(all_returns, axis=1).mean(axis=1)
    auditor = YnorQuantViability(ensemble_returns)
    mu_score = auditor.compute_mu()
    
    # 4. Final Report
    print("[STEP 4/4] Generating Sovereign Audit Report...")
    print("-" * 50)
    status = auditor.generate_audit_report()
    print("-" * 50)
    
    print(f"\n✅ GLOBAL AUDIT COMPLETED.")
    print(f"Portfolio Viability Score: μ = {mu_score:.4f}")
    print(f"Verdict: {status}")

if __name__ == "__main__":
    run_master_audit()
