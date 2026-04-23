# ── Étape 1 : on part d'une image Python légère ──────────────────────────────
FROM python:3.12-slim

# ── Étape 2 : on crée le dossier de travail dans le conteneur ────────────────
WORKDIR /app

# ── Étape 3 : on copie et installe les dépendances ───────────────────────────
# (on copie requirements.txt AVANT le reste pour profiter du cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Étape 4 : on copie le code de l'application ──────────────────────────────
COPY . .

# ── Étape 5 : on expose le port 8000 ─────────────────────────────────────────
EXPOSE 8000

# ── Étape 6 : commande de démarrage ──────────────────────────────────────────
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
