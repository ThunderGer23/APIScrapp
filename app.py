from fastapi import FastAPI
from routes.app import red

app = FastAPI()
app.include_router(red)