from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.routers.vector_db_router import router
from src.api.routers.chat_router import chat_router
from src.di.nlp_di import build_nlp_pipeline

@asynccontextmanager
async def lifespan(app: FastAPI):
    build_nlp_pipeline()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(chat_router)

