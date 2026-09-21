from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.logging_config import configure_logging
from app.routers import ai, billing, health, resumes

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title="DollarResume API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["resumes"])
app.include_router(ai.router, prefix="/api", tags=["ai"])
app.include_router(billing.router, prefix="/api", tags=["billing"])
