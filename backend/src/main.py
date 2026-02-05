from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import router
from .models import SQLModel
from .database.session import engine
from .models.user import User
from .models.task import Task

app = FastAPI(title="Todo Web Application API", version="1.0.0")

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