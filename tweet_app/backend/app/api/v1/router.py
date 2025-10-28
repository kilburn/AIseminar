from fastapi import APIRouter

# Import route modules (these will be created later)
# from app.api.v1.endpoints import auth, datasets, tweets, analysis, search, export

api_router = APIRouter()

# Health endpoint for API
@api_router.get("/health", tags=["health"])
async def api_health():
    """API health check"""
    return {"status": "healthy", "message": "API is running"}

# Placeholder routes - these will be implemented in subsequent phases
# api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
# api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
# api_router.include_router(tweets.router, prefix="/tweets", tags=["tweets"])
# api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
# api_router.include_router(search.router, prefix="/search", tags=["search"])
# api_router.include_router(export.router, prefix="/export", tags=["export"])

@api_router.get("/info", tags=["info"])
async def api_info():
    """API information"""
    return {
        "name": "TweetEval NLP Platform API",
        "version": "1.0.0",
        "description": "API for tweet dataset analysis using TweetEval models",
        "endpoints": {
            "authentication": "/auth",
            "datasets": "/datasets",
            "tweets": "/tweets",
            "analysis": "/analysis",
            "search": "/search",
            "export": "/export"
        }
    }