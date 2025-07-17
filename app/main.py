from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Offer Engine API is running"}
