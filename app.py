from fastapi import FastAPI
from routes.app import app

app = FastAPI()
app.include_router(app)