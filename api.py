from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import requests
import os
from datetime import datetime

from auth.login import login
from downloader.rinex import download_rinex
from config import (
    LOGIN_URL,
    DOWNLOAD_URL,
    HEADERS,
    ZIP_DOWNLOAD_URL,
)

app = FastAPI()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


@app.get("/download/{station}")
def download_station(station: str):

    session = requests.Session()

    success = login(
        session,
        LOGIN_URL,
        EMAIL,
        PASSWORD
    )

    if not success:
        raise HTTPException(
            status_code=401,
            detail="Login failed"
        )

    doy = datetime.utcnow().timetuple().tm_yday
    year = datetime.utcnow().year

    zip_name, zip_content = download_rinex(
        session,
        HEADERS,
        DOWNLOAD_URL,
        station,
        doy,
        year,
        ZIP_DOWNLOAD_URL,
        None
    )

    return Response(
        content=zip_content,
        media_type="application/zip",
        headers={
            "Content-Disposition":
            f'attachment; filename="{zip_name}"'
        }
    )