
# Utilise Python 3.11 slim pour optimiser la taille
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Variables d'environnement pour optimiser Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Installe les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copie et installe les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source
COPY *.py ./

# Crée un utilisateur non-root pour la sécurité
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# Change le propriétaire des fichiers
RUN chown -R appuser:appgroup /app
USER appuser

# Expose le port
EXPOSE 3000

# Variables d'environnement par défaut
ENV NODE_ENV=production
ENV PORT=3000

# Commande de santé pour Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Commande de démarrage
CMD ["python", "main.py"]

# Labels pour la documentation
LABEL maintainer="MCP Server Python"
LABEL version="1.0.0"
LABEL description="Chaster Locks MCP Server - Python FastAPI"
