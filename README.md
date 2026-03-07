# Laptop Price Predictor

A machine learning web app that predicts laptop prices based on hardware specifications.

- **Backend**: FastAPI (`api.py`) — serves predictions via a REST endpoint
- **Frontend**: Streamlit (`frontend.py`) — interactive UI for submitting laptop specs
- **Model**: scikit-learn pipeline stored in `model.pkl`

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API (terminal 1)
uvicorn api:app --reload

# Start the frontend (terminal 2)
streamlit run frontend.py
```

The API will be at `http://localhost:8000` and the UI at `http://localhost:8501`.

---

## Deploying to Render

### One-click Blueprint Deploy

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New → Blueprint**.
3. Connect your GitHub repo. Render will detect `render.yaml` and create **two services** automatically:
   - `laptop-api` — FastAPI backend
   - `laptop-frontend` — Streamlit frontend

### Post-deploy: Set the API URL

Once both services are deployed:

1. Copy the live URL of the **`laptop-api`** service (e.g. `https://laptop-api.onrender.com`).
2. Go to the **`laptop-frontend`** service → **Environment** tab.
3. Set the environment variable:
   ```
   API_URL = https://laptop-api.onrender.com/predict
   ```
4. Click **Save Changes** — Render will redeploy the frontend automatically.

> **Note**: On the free tier, services spin down after 15 minutes of inactivity. The first request after a sleep period may take ~30 seconds.

---

## API Reference

### `GET /`
Returns a welcome message.

### `POST /predict`
Predict the price of a laptop.

**Request body:**
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

**Response:**
```json
{
  "message": "Predicted price of the laptop is 131295.20"
}
```

Interactive API docs available at `/docs` (Swagger UI).
