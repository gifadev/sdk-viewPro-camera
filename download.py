import requests
from bs4 import BeautifulSoup
import argparse

BASE_URL = "http://192.168.2.119:8554/download/"
TARGETS = {
    "photo": [".jpeg"],
    "video": [".mp4",]
}

def download_files(subdir, extensions):
    url = BASE_URL + subdir + "/"
    print(f"\nChecking: {url}")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    links = [
        a['href'] for a in soup.find_all('a', href=True)
        if any(a['href'].lower().endswith(ext) for ext in extensions)
    ]

    for link in links:
        file_url = url + link
        print(f"Downloading: {file_url}")
        r = requests.get(file_url)
        with open(link, 'wb') as f:
            f.write(r.content)

    if not links:
        print(f"No files found in {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download media files (photos and videos) from server.",
        epilog="Example: python download_media.py -f -v"
    )

    parser.add_argument('-f', '--photo', action='store_true', help='Download photo files')
    parser.add_argument('-v', '--video', action='store_true', help='Download video files')

    args = parser.parse_args()

    if not args.photo and not args.video:
        download_files("photo", TARGETS["photo"])
        download_files("video", TARGETS["video"])
    else:
        if args.photo:
            download_files("photo", TARGETS["photo"])
        if args.video:
            download_files("video", TARGETS["video"])
