from fastapi import FastAPI
from app.api.prediction_routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Lung Cancer Detection API Running"}