import logging
from fastapi import FastAPI
from app.views import auth, users, admin, assets  # Adjust imports if necessary
from fastapi.middleware.cors import CORSMiddleware

# Configure logging for the entire application
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SOSO Backend",
    description="Backend for the SOSO satellite operations system",
    version="1.0.0"
)

# Enable CORS for the Next.js frontend (assumed to be running on http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different functionalities
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(assets.router)

logger.info("SOSO Backend is running!")