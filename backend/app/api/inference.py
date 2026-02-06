from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.schemas.inference import InferenceResponse
from app.services.inference_service import run_inference

router = APIRouter(prefix="/inference", tags=["Lung Cancer Detection"])

@router.post(
    "/predict",
    response_model=InferenceResponse,
    summary="Detect lung cancer from CT scan image",
    description="""
    Upload a lung CT scan image (PNG or JPEG) to get:
    - Cancer detection prediction (normal/benign/malignant)
    - Probability score showing AI confidence percentage
    - Heatmap visualization showing where the AI detected abnormalities
    - Detailed probability breakdown for all classes
    """
)
async def predict_lung_cancer(
    file: UploadFile = File(..., description="Lung CT scan image (PNG or JPEG)"),
    generate_heatmap: bool = Query(True, description="Generate heatmap visualization")
):
    """
    AI-powered lung cancer detection endpoint.
    
    Returns comprehensive analysis including:
    - Prediction (normal/benign/malignant)
    - Confidence score (0-1)
    - Probability percentage (0-100)
    - Heatmap showing cancer location
    - All class probabilities
    """
    # 1️⃣ Validate image type
    if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(
            status_code=415,
            detail="Only PNG and JPEG lung CT scan images are supported"
        )

    # 2️⃣ Run model inference with heatmap generation
    try:
        result = await run_inference(file, generate_heatmap=generate_heatmap)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during inference: {str(e)}"
        )

    # 3️⃣ Return validated response
    return InferenceResponse(
        prediction=result["prediction"],
        confidence=result["confidence"],
        probability_score=result["probability_score"],
        probabilities=result["probabilities"],
        heatmap_image=result.get("heatmap_image"),
        message=result["message"]
    )
