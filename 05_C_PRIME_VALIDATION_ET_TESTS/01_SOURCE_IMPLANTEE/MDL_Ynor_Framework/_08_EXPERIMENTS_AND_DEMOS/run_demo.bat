@echo off
TITLE MDL YNOR - DEMO RUNBOOK (v2.2.0-PROD)
SETLOCAL

echo ============================================================
echo   ⚡ MDL YNOR - AUTOMATED DEMO & VALIDATION ⚡
echo ============================================================

:: 1. CHECK VIRTUAL ENV
IF NOT EXIST venv (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

echo [INFO] Activating environment...
CALL venv\Scripts\activate

:: 2. INSTALL DEPS
echo [INFO] Installing required dependencies...
pip install -r requirements.txt
pip install -e .

:: 3. ENVIRONMENT CHECK
IF NOT EXIST .env (
    echo [WARNING] No .env file found. Copying template...
    copy .env.template .env
    echo [ACTION] Please edit your .env file and add your API keys!
)

:: 4. RUN VALIDATION
echo.
echo [1/3] RUNNING HARDCORE VALIDATION (MU MARGIN)...
python hardcore_validation.py

:: 5. RUN EXPERIMENT
echo.
echo [2/3] RUNNING AGI MUTATION EXPERIMENT...
python run_experiment.py

:: 6. NOTEBOOK LAUNCH (INFO)
echo.
echo [3/3] DEMO COMPLETE. 
echo [INFO] To view the Jupyter Notebook, run:
echo jupyter notebook ynor_core_demonstration.ipynb
echo.

echo ============================================================
echo   ✅ DEMO & AUDIT SUCCESSFUL
echo ============================================================
pause
