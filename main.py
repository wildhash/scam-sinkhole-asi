import uvicorn
from app.api.main import app
from app.core.config import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "app.api.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
