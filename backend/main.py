"""
Main FastAPI application entry point.
Configures the FastAPI app, CORS, and includes all routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection
from routes.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    Handles startup and shutdown events.
    - On startup: Connect to MongoDB
    - On shutdown: Close MongoDB connection
    """
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks using FastAPI and MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include task routes
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Task Management API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
