"""
Development server runner with proper reload exclusions.
"""
import uvicorn
from app.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        reload_excludes=["logs/*", "*.log", "__pycache__/*", "*.pyc"],
        reload_dirs=["app"],  # Sadece app klasörünü izle
    )
