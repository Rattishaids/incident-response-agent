from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import AlertRequest, IncidentResponse
from .agent import IncidentAgent
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Incident Response Agent with Hindsight Memory"
)

# Enable CORS for UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent (singleton)
try:
    agent = IncidentAgent()
except ValueError as e:
    print(f"❌ {e}")
    agent = None

# ============================================
# API Endpoints
# ============================================

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy" if agent and agent.memory else "unhealthy"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    if not agent:
        return {
            "status": "error",
            "message": "Agent not configured. Check API keys."
        }
    return {
        "status": "healthy",
        "hindsight_cloud": "connected",
        "cascadeflow": "ready"
    }

@app.post("/incident", response_model=IncidentResponse)
async def handle_incident(request: AlertRequest):
    """
    Analyze an incident alert
    
    - **alert**: Description of the incident (e.g., "Payment service is returning 500 errors")
    """
    if not agent:
        raise HTTPException(
            status_code=503,
            detail="Agent not configured. Check API keys in .env file."
        )
    try:
        return await agent.analyze(request.alert)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))