# MIROIR TEXTUEL - ynor_ci.yml

Source : MDL_Ynor_Framework\.github\workflows\ynor_ci.yml
Taille : 1063 octets
SHA256 : 4fadc6ad4957f05b06caf415b3798f05f871cf88d39e621f9899c3d24cd83057

```text
name: Ynor AGI CI (10/10 Readiness)

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -e .
    - name: Run Unit Tests
      env:
        PYTHONPATH: .
      run: |
        python -m pytest tests/
    - name: Run Core Logic Validation (Monte Carlo)
      env:
        PYTHONPATH: .
      run: |
        python _03_CORE_AGI_ENGINES/hardcore_validation.py
    - name: Infrastructure Security Scan
      run: |
        # Mocking a security scan for secrets
        if grep -r "SK-" .; then
          echo "Hardcoded secrets found!"
          exit 1
        fi
        echo "Security Scan Passed."
    - name: Build Secure SDK
      run: |
        python _04_DEPLOYMENT_AND_API/build_secure_sdk.py

```