from fastapi import FastAPI

app = FastAPI()

from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Offer Engine API is running"}
