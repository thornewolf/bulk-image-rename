import requests
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import functools


_DOWNLOADS_DIR = Path("downloads")
_INPUT_IMAGES_FILE = Path("images.txt")


def download(*, url: str, target_dir: Path):
    print(f"Downloading {url}")
    try:
        # Define the headers with a Chrome user agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Make the request with the headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Generate a unique filename using UUID
            filename = f"{uuid.uuid4()}.jpg"

            # Save the file
            file_path = os.path.join(target_dir, filename)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded as {filename}")
        else:
            print(f"Failed to download {url}, {response}, {response.text}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


def download_all(*, urls: list[str], target_dir: Path):
    download_to_target_dir = lambda url: download(url=url, target_dir=target_dir)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_to_target_dir, urls)


def _load_urls(file_path):
    """Return a list of image URLs from the input file."""
    with open(file_path) as f:
        return [url.strip() for url in f.readlines()]


def main():
    if not os.path.exists(_DOWNLOADS_DIR):
        os.makedirs(_DOWNLOADS_DIR)

    urls = _load_urls(_INPUT_IMAGES_FILE)
    download_all(urls=urls, target_dir=_DOWNLOADS_DIR)


if __name__ == "__main__":
    main()
