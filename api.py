from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated
import pickle
import pandas as pd
import logging

app = FastAPI(
    title="Laptop Price Predictor API",
    description="An API to predict laptop prices based on their features.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    logger.info("Model loaded successfully.")
except FileNotFoundError:
    logger.error("Model file 'model.pkl' not found. The API will not be able to make predictions.")
    model = None
except Exception as e:
    logger.error(f"An error occurred while loading the model: {e}")
    model = None

class LaptopFeatures(BaseModel):
    company: Annotated[str, Field(..., description = 'The company of the Laptop')]
    typename: Annotated[str, Field(..., description = 'The type of the Laptop')]
    inches: Annotated[float, Field(..., description = 'The size of the Laptop in inches', gt = 0)]
    screen_resolution: Annotated[str, Field(..., description = 'The screen resolution')]
    cpu: Annotated[str, Field(..., description = 'The CPU of the Laptop')]
    ram: Annotated[int, Field(..., description = 'The RAM of the Laptop in GB', gt = 0)]
    gpu: Annotated[str, Field(..., description = 'The GPU of the Laptop')]
    os: Annotated[str, Field(..., description = 'The operating system of the Laptop')]
    weight: Annotated[float, Field(..., description = 'The weight of the Laptop in kg', gt=0)]
    ssd: Annotated[int, Field(..., description = 'The SSD of the Laptop in GB', ge=0)]
    hdd: Annotated[int, Field(..., description = 'The HDD of the Laptop in GB', ge=0)]
    flash_storage: Annotated[int, Field(..., description = 'The flash storage of the Laptop in GB', ge=0)]
    hybrid_storage: Annotated[int, Field(..., description = 'The hybrid storage of the Laptop in GB', ge=0)]

@app.get('/')
def home():
    return {"message": "Welcome to Laptop Price Predictor API"}

@app.post('/predict')
def predict_price(data: LaptopFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not available. Please check server logs.")

    try:
        input_df = pd.DataFrame([data.model_dump()])
        input_df = input_df.rename(columns={
            'company': 'Company',
            'typename': 'TypeName',
            'inches': 'Inches',
            'screen_resolution': 'ScreenResolution',
            'cpu': 'Cpu',
            'ram': 'Ram',
            'gpu': 'Gpu',
            'os': 'OpSys',
            'weight': 'Weight',
            'ssd': 'SSD',
            'hdd': 'HDD',
            'flash_storage': 'Flash',
            'hybrid_storage': 'Hybrid',
        })
        prediction = model.predict(input_df)
        predicted_price = prediction[0]

        logger.info(f"Prediction successful. Price: {predicted_price:.2f}")
        return {'message': f'Predicted price of the laptop is {predicted_price:.2f}'}
    except Exception as e:
        logger.error(f"An error occurred during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Could not make a prediction. Error: {e}")