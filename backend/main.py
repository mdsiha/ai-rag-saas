from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import router
from app.logger import logger

app = FastAPI(
    title="AI RAG SaaS",
    description="Production-ready RAG API",
    version="1.0.0",
)

app.include_router(router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"ERREUR CRITIQUE: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "Une erreur inattendue est survenue."
        }
    )