from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict

class InferenceResponse(BaseModel):
    # Must be lowercase to match the API output
    prediction: Literal["normal", "benign", "malignant"]
    
    # Confidence between 0.0 and 1.0
    confidence: float = Field(..., ge=0.0, le=1.0)
    
    # Probability score as percentage (0-100)
    probability_score: float = Field(..., ge=0.0, le=100.0, description="AI model confidence as percentage")
    
    # All class probabilities
    probabilities: Dict[str, float] = Field(..., description="Probability percentages for all classes")
    
    # Heatmap image as base64 string
    heatmap_image: Optional[str] = Field(None, description="Base64 encoded heatmap visualization")
    
    # Optional message about the model/version
    message: str
