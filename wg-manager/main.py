from fastapi import FastAPI
from api.router import router
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(title="WireGuard Manager", version="1.0.0")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting WireGuard Manager...")
    uvicorn.run(app, host="0.0.0.0", port=settings.wg_manager_port)