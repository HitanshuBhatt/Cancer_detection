from fastapi import APIRouter, UploadFile, File
from app.services.lung_prediction_service import predict_lung_cancer

router = APIRouter()

@router.post("/predict-lung-cancer")
async def predict_route(file: UploadFile = File(...)):
    result = await predict_lung_cancer(file)
    return result