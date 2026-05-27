# Image de base Python
FROM python:3.12-slim

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer les ports
EXPOSE 8501 8502 8503 8001

# Commande par défaut — interface principale
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]