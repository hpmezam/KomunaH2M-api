from fastapi import FastAPI
from app.routers.state import state_router
from app.routers.gender import gender_router

app = FastAPI(title="KomunaH2M API", version="0.1.0")

app.include_router(state_router)
app.include_router(gender_router)