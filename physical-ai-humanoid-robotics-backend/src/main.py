from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, content, chatbot, progress, personalization, translation, hardware
from src.routes import ingestion, retrieval

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="Backend API for the Physical AI textbook with authentication, content management, and RAG chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(content.router, prefix="/api", tags=["content"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(ingestion.router, prefix="/api", tags=["ingestion"])
app.include_router(retrieval.router, prefix="/api", tags=["retrieval"])
app.include_router(progress.router, prefix="/api", tags=["progress"])
app.include_router(personalization.router, prefix="/api/personalization", tags=["personalization"])
app.include_router(translation.router, prefix="/api/translation", tags=["translation"])
app.include_router(hardware.router, prefix="/api/hardware", tags=["hardware"])

@app.get("/")
def read_root():
    return {"message": "Physical AI & Humanoid Robotics Textbook API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}