from urllib.request import urlretrieve
from pathlib import Path
from setuptools import setup

PROJECT_NAME= "static"

def download_cdn_files()  -> None:
    static_path = Path(__file__).parent / PROJECT_NAME
    static_path.mkdir(parents=True, exist_ok=True)
    for cdn_url in (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
    ):
        urlretrieve(cdn_url, static_path / cdn_url.split("/")[-1])

download_cdn_files()
