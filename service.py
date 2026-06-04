import requests
from datetime import datetime

from config import (
    LOGIN_URL,
    DOWNLOAD_URL,
    HEADERS,
    ZIP_DOWNLOAD_URL,
    directory
)

from auth.login import login
from downloader.rinex import download_rinex


def run_download(email, password):

    session = requests.Session()

    success = login(
        session,
        LOGIN_URL,
        email,
        password
    )

    if not success:
        raise Exception("Login failed")

    doy = datetime.utcnow().timetuple().tm_yday
    year = datetime.utcnow().year

    stations = [
        "bako",
        "cang",
        "cbik",
        "cdnp",
        "samp",
        "cbda",
        "cmak"
    ]

    for station in stations:
        download_rinex(
            session,
            HEADERS,
            DOWNLOAD_URL,
            station,
            doy,
            year,
            ZIP_DOWNLOAD_URL,
            directory
        )