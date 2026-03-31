# MIROIR TEXTUEL - Dockerfile

Source : MDL_Ynor_Framework\Dockerfile
Taille : 754 octets
SHA256 : f02c9edfa988d5389223c453679bb9203548654fc4af8c5ab6461f6e205bb9fa

```text
# Batir le conteneur MDL Ynor - Architecture Supreme
# Copyright (c) 2026 Charlier Rony

FROM python:3.10-slim

# Configuration environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

WORKDIR /app

# Installation dependances systeme minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installation requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Exposition port API par defaut
EXPOSE 8492

# Commande par defaut : lancement du serveur d'audit
CMD ["uvicorn", "_04_DEPLOYMENT_AND_API.ynor_api_server:app", "--host", "0.0.0.0", "--port", "8492"]

```