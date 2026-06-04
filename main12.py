import requests
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from config import (
    LOGIN_URL,
    DOWNLOAD_URL,
    HEADERS,
    ZIP_DOWNLOAD_URL,
    directory
)

from auth.login import login
from downloader.rinex import download_rinex

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def main():

    session = requests.Session()

    success = login(
        session,
        LOGIN_URL,
        EMAIL,
        PASSWORD
    )

    if not success:
        print("LOGIN FAILED")
        return

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

    # Temp
    # start_date = datetime(2026, 4, 1)
    # end_date = datetime(2026, 6, 2)

    # current_date = start_date

    # while current_date <= end_date:

    #     doy = current_date.timetuple().tm_yday
    #     year = current_date.year

    #     print(f"DATE: {current_date.strftime('%Y-%m-%d')}")
    #     print(f"DOY: {doy}")

    #     for station in stations:

    #         print(f"\nDownloading station: {station}")

    #         try:

    #             download_rinex(
    #                 session,
    #                 HEADERS,
    #                 DOWNLOAD_URL,
    #                 station,
    #                 doy,
    #                 year,
    #                 ZIP_DOWNLOAD_URL,
    #                 directory
    #             )

    #         except Exception as e:

    #             print(f"FAILED {station} : {e}")

    #         # Delay supaya tidak spam request
    #         time.sleep(1)

    #     current_date += timedelta(days=1)

    # print("\nDONE")

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


if __name__ == "__main__":
    main()