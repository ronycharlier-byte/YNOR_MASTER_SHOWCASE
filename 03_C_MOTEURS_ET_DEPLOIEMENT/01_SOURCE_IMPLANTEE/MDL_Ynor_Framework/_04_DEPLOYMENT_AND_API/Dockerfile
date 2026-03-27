# Utilise une image miniature Linux (Debian) optimisée pour la grande vitesse
FROM python:3.11-slim

# Crée le dossier d'application "dans le nuage"
WORKDIR /app

# Optimisations DevOps : Bloque la création de cache lourd
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copie le fichier d'exigences des bibliothèques
COPY requirements.txt .

# Installe toutes tes dépendances (FastAPI, Cryptography, etc)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copie l'intégralité du code de ton API (depuis ton PC) vers le serveur
COPY . .

# IMPORTANT : Le port dynamique pour les hébergeurs Cloud (Render/Heroku/AWS)
ENV PORT=8492
EXPOSE $PORT

# Allume ton Moteur Mathématique avec le Serveur de Haute Performance (Uvicorn)
CMD ["sh", "-c", "uvicorn ynor_api_server:app --host 0.0.0.0 --port ${PORT}"]
