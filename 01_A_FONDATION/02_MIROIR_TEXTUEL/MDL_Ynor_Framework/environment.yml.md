# MIROIR TEXTUEL - environment.yml

Source : MDL_Ynor_Framework\environment.yml
Taille : 514 octets
SHA256 : d3fe6790642db33dd3959da6201c91a706aaf4ab468a5ead6f691fc9f447e80d

```text
name: mdl-ynor-env
channels:
  - conda-forge
  - pytorch
  - defaults
dependencies:
  - python=3.10
  - pip
  - numpy>=1.26.4
  - scipy>=1.12.0
  - pandas>=2.2.1
  - matplotlib>=3.8.3
  - plotly>=5.19.0
  - streamlit>=1.32.2
  - fastapi>=0.110.0
  - uvicorn>=0.27.1
  - python-dotenv>=1.0.1
  - requests>=2.31.0
  - pydantic>=2.6.1
  - openai>=1.13.3
  - cryptography>=42.0.5
  - pytest>=8.0.2
  - pytest-cov>=4.1.0
  - nbconvert>=7.11.0
  - ipykernel>=6.29.3
  - pip:
      - tiktoken==0.6.0
      - torch==2.2.1

```