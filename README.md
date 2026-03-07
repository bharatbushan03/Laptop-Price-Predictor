# Laptop Price Predictor

A machine learning web app that predicts laptop prices based on hardware specs.

- **Backend**: FastAPI (`api.py`) — REST prediction endpoint
- **Frontend**: Streamlit (`frontend.py`) — interactive UI
- **Model**: scikit-learn pipeline in `model.pkl`

---

## Running Locally

```bash
pip install -r requirements.txt

# Terminal 1 — API
uvicorn api:app --reload

# Terminal 2 — Frontend
streamlit run frontend.py
```

API → `http://localhost:8000` | UI → `http://localhost:8501`

---

## Deploying to Railway

Railway deploys one service per project. You need **two Railway services** from the same GitHub repo.

### Step 1 — Push to GitHub
```bash
git add .
git commit -m "Add Railway deployment config"
git push
```

### Step 2 — Deploy the API service
1. Go to [railway.app](https://railway.app) → **New Project → Deploy from GitHub repo**
2. Select your repo
3. Railway auto-detects `railway.toml` → deploys the FastAPI backend
4. Go to **Settings → Networking → Generate Domain** to get a public URL
   - e.g. `https://laptop-api-production.up.railway.app`

### Step 3 — Deploy the Frontend service
1. In the same Railway project, click **+ New Service → GitHub Repo**
2. Select the **same repo** again
3. Go to **Settings → Deploy** and set the **Start Command** to:
   ```
   streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
   ```
4. Go to **Variables** and add:
   ```
   API_URL = https://your-api-domain.up.railway.app/predict
   ```
   *(replace with the actual URL from Step 2)*
5. Go to **Settings → Networking → Generate Domain** for the frontend

---

## API Reference

### `POST /predict`
```json
{
  "company": "Apple",
  "typename": "Ultrabook",
  "inches": 13.3,
  "screen_resolution": "IPS Panel Retina Display 2560x1600",
  "cpu": "Intel Core i5 2.3GHz",
  "ram": 8,
  "gpu": "Intel",
  "os": "macOS",
  "weight": 1.37,
  "ssd": 128,
  "hdd": 0,
  "flash_storage": 0,
  "hybrid_storage": 0
}
```
Response: `{"message": "Predicted price of the laptop is 131295.20"}`

Swagger UI available at `/docs`.
