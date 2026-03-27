# MIROIR TEXTUEL - mdl_full_check.yml

Source : MDL_Ynor_Framework\.github\workflows\mdl_full_check.yml
Taille : 1543 octets
SHA256 : c8d002412d627afb253d30c4749633ee6196be3f0f753b330da43e8dcc300d0e

```text
name: MDL YNOR - FULL AUDIT CI (v2.2.0-PROD)

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  scientific-audit:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install Dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
        pip install nbconvert ipykernel
    
    - name: 🧪 Unit & Robustness Tests (pytest)
      run: |
        pytest tests/test_mdl_robustness.py --cov=_04_DEPLOYMENT_AND_API.ynor_core
    
    - name: 🔬 Reproducible Research Audit (seeds check)
      run: |
        python _03_CORE_AGI_ENGINES/hardcore_validation.py
        python _08_EXPERIMENTS_AND_DEMOS/run_experiment.py
    
    - name: 📓 Notebook Execution Check (nbconvert)
      run: |
        jupyter nbconvert --to notebook --execute _08_EXPERIMENTS_AND_DEMOS/ynor_core_demonstration.ipynb --output executed_ynor_demo.ipynb
    
    - name: 🚀 Auto-Push Audit Reports (Notebooks)
      env:
        GITHUB_TOKEN: ${{ secrets.GH_PAT }}
      run: |
        git config --global user.name "MDL YNOR Engine [Bot]"
        git config --global user.email "bot@mdlstrategy.ai"
        git add executed_ynor_demo.ipynb
        git commit -m "📊 [AUTO-AUDIT] Updated Scientific Reproducibility Notebook (v${{ github.run_number }})" || echo "No changes to commit"
        git push origin ${{ github.ref_name }}

```