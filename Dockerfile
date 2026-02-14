FROM python:3.12-slim

# Éviter la génération de fichiers .pyc et forcer l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installation des dépendances système + Chromium
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Variables d'environnement pour Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Copier les fichiers de configuration des dépendances
COPY pyproject.toml .
# Si vous avez un fichier lock (ex: pdm.lock ou poetry.lock), copiez-le aussi ici

# Installer les dépendances via pip (en utilisant pyproject.toml)
RUN pip install --no-cache-dir .

# Copier le reste du code
COPY . .

EXPOSE 8000

# Utilisation de l'utilisateur non-root (recommandé pour la sécurité)
# Note : Selenium peut parfois nécessiter des ajustements de permissions
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]