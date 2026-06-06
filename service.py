import os
import requests
from datetime import datetime

from config import (
    LOGIN_URL,
    DOWNLOAD_URL,
    HEADERS,
    ZIP_DOWNLOAD_URL,
    API_STATIONS
)

from auth.login import login
from downloader.rinex import download_rinex

def load_valid_stations():
    url = API_STATIONS
    try:
        data = requests.get(url, timeout=20).json()
    except Exception as e:
        print("Error fetching stations:", e)
    
    stations = data['results']['pasutStasiuns']

    return {
        s['sitecode'].strip().lower()
        for s in stations
    }


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

    stations = load_valid_stations()

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