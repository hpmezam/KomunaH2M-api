from fastapi import FastAPI
from app.routers.state import state_router

app = FastAPI(title="KomunaH2M API", version="0.1.0")

app.include_router(state_router)