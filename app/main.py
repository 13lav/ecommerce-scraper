from fastapi import FastAPI, Depends
from app.api.v1 import api as v1_api
from app.security.auth import match_api_key
app = FastAPI()

app.include_router(v1_api.router, prefix="/api/v1", dependencies=[Depends(match_api_key)])
