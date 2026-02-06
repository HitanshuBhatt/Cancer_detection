from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.health import router as health_router
from app.api.inference import router as inference_router
from app.config import Settings
from app.logging_config import logger

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    description="AI-powered lung cancer detection system with heatmap visualization for medical professionals"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(inference_router)

@app.on_event("startup")
def startup():
    logger.info("Starting up the AI Lung Cancer Detection application")
    logger.info("Model loaded and ready for inference")

@app.on_event("shutdown")
def shutdown():
    logger.info("Shutting down the AI Lung Cancer Detection application")
