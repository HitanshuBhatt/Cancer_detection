from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
def health():
    return{
        "status": "ok",
        "service": "Hybrid AI lung detection backend"        
    }