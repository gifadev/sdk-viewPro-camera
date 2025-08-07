import requests
from bs4 import BeautifulSoup
import argparse
import os

BASE_URL = "http://192.168.2.119:8554/download/"
TARGETS = {
    "photo": [".jpeg"],
    "video": [".mp4"]
}

def download_files(subdir, extensions, output_dir):
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
        response = requests.get(file_url)

        # Simpan ke folder output
        save_path = os.path.join(output_dir, link)
        with open(save_path, 'wb') as f:
            f.write(response.content)

    if not links:
        print(f"No files found in {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download media files (photos and videos) from server.",
        epilog="Example: python download_media.py -f -v -s 20250807_1100"
    )

    parser.add_argument('-f', '--photo', action='store_true', help='Download photo files')
    parser.add_argument('-v', '--video', action='store_true', help='Download video files')
    parser.add_argument('-s', '--start-time', required=True, help='Timestamp for output folder name (e.g., 20250807_1100)')

    args = parser.parse_args()

    # Buat output folder
    output_folder = os.path.join("Drone_Tethered", f"DT_{args.start_time}")
    os.makedirs(output_folder, exist_ok=True)

    if not args.photo and not args.video:
        download_files("photo", TARGETS["photo"], output_folder)
        download_files("video", TARGETS["video"], output_folder)
    else:
        if args.photo:
            download_files("photo", TARGETS["photo"], output_folder)
        if args.video:
            download_files("video", TARGETS["video"], output_folder)
