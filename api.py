from fastapi import FastAPI
from service import run_download
import os

app = FastAPI()

@app.get("/download")
def download():
    run_download(
        os.getenv("EMAIL"),
        os.getenv("PASSWORD")
    )

    return {"status": "success"}