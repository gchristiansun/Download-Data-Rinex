import configparser
import os
import re
import requests

BASE_URL = "https://download-data-rinex.onrender.com/download"

STATIONS = [
    "bako",
    "cang",
    "cbik",
    "cdnp",
    "samp",
    "cbda",
    "cmak"
]

def load_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    return config["DOWNLOAD"]["path"]

def download_rinex(download_dir):
    os.makedirs(download_dir, exist_ok=True)

    for station in STATIONS:
        try:
            print(f"Downloading {station}...")

            response = requests.get(
                f"{BASE_URL}/{station}",
                timeout=300
            )

            if response.status_code != 200:
                print(
                    f"Failed {station}: "
                    f"HTTP {response.status_code}"
                )
                continue

            filename = f"{station}.zip"

            cd = response.headers.get(
                "Content-Disposition",
                ""
            )

            match = re.search(
                r'filename="?([^"]+)"?',
                cd
            )

            if match:
                filename = match.group(1)

            filepath = os.path.join(
                download_dir,
                filename
            )

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"Saved: {filepath}")

        except Exception as e:
            print(f"Error {station}: {e}")

if __name__ == "__main__":
    download_path = load_config()
    download_rinex(download_path)