from fastapi import FastAPI
from app.routers.state import state_router
from app.routers.gender import gender_router
from app.routers.marital_status import marital_router
from app.routers.education_level import education_router


app = FastAPI(title="KomunaH2M API", version="0.1.0")

app.include_router(state_router)
app.include_router(gender_router)
app.include_router(marital_router)
app.include_router(education_router)