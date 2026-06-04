from service import run_download
import os

run_download(
    os.getenv("EMAIL"),
    os.getenv("PASSWORD")
)