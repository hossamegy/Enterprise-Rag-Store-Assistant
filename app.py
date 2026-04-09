from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.routers.vector_db_router import router
from src.api.routers.chat_router import chat_router
from src.di.nlp_di import build_nlp_pipeline
from src.config.logger import logger
from src.core.exceptions.base_exception import BaseAppException
from src.core.exceptions.domain_exceptions import EntityNotFoundException, ValidationException

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Enterprise RAG System...")
    build_nlp_pipeline()
    logger.info("System Ready.")
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    status_code = 500
    if isinstance(exc, EntityNotFoundException):
        status_code = 404
    elif isinstance(exc, ValidationException):
        status_code = 400
        
    logger.warning(f"App Exception on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=status_code,
        content={"status": "error", "message": exc.message, "detail": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Global Exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "An unexpected server error occurred.", "detail": str(exc)},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(chat_router)

