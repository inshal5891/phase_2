from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api.router import router
from .models import SQLModel
from .database.session import engine
from .models.user import User
from .models.task import Task
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Todo Web Application API", version="1.0.0")

# Add exception handler for debugging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {type(exc).__name__}: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Add CORS middleware to allow communication between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the task router
app.include_router(router)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    """Root endpoint for basic health check."""
    return {"message": "Todo Web Application API is running!"}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)