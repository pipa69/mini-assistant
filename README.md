# Mini Assistant (scikit-learn)

Repo zawiera kompletny projekt "Mini Assistant" — NLU oparty na TF-IDF + LogisticRegression,
REST API (FastAPI), trening modelu, Dockerfile, CI (GitHub Actions) oraz prosty logger SQLite.

## Co jest w repo
- `/app` - aplikacja (FastAPI)
- `/training` - skrypty treningowe i przykładowy dataset
- `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml`
- Testy w `/tests`

## Szybkie uruchomienie lokalne
1. Stwórz venv i zainstaluj dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Wytrenuj model:
   ```bash
   cd training
   python train.py --data dataset.csv
   ```
   Model zapisze się do `app/model/nlu_pipeline.joblib`.
3. Uruchom API:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

## Wypchnięcie na GitHub
1. Stwórz repo na GitHub (np. `mini-assistant`)
2. Wykonaj:
   ```bash
   git remote add origin git@github.com:pipa69/mini-assistant.git
   git branch -M main
   git push -u origin main
   ```
(możesz użyć HTTPS jeśli preferujesz)

## Uwaga bezpieczeństwa
- Nie commituj kluczy API; używaj secrets w CI i env vars w runtime.
- Logi mogą zawierać dane użytkownika — anonimizuj je jeśli zamierzasz produkcyjnie przechowywać.
