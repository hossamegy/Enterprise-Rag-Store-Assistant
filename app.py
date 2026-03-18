"""from fastapi import FastAPI
from src.api.routers.vectoreDb_router import router
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


    import torch
"""
import torch

print(torch.cuda.is_available())


