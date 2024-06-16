import os
import sys
import py7zr
import shutil
import requests
import subprocess

GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "D4N1L0200"
REPO_NAME = "DelNet"


def get_releases():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/releases"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_asset(download_url, output_path):
    headers = {"Accept": "application/octet-stream"}
    response = requests.get(download_url, headers=headers, stream=True)
    response.raise_for_status()

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Downloaded to {output_path}")


def extract_7z(file_path, extract_to):
    with py7zr.SevenZipFile(file_path, mode="r") as archive:
        archive.extractall(path=extract_to)
    print(f"Extracted {file_path} to {extract_to}")


def move_files(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        shutil.move(source_file, target_file)

    print(f"Moved files from {source_dir} to {target_dir}.")

def delete_files_in_directory(directory):
    if not os.path.exists(directory):
        return
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
    
    print(f"Deleted all files in {directory}.")

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python download_release.py <version>")
        return

    version = sys.argv[1]

    if not os.path.exists("server"):
        os.makedirs("server")

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    releases = get_releases()
    release = None

    for _release in releases:
        if _release["tag_name"] != version:
            continue
        else:
            release = _release
            break

    if release is None:
        print(f"Version {version} not found.")
        return

    assets = release["assets"]
    if not assets:
        print(f"No assets found for version {version}")
        return

    for asset in assets:
        asset_name = asset["name"]
        if asset_name != "server.7z":
            continue

        delete_files_in_directory("backup")
        delete_files_in_directory("downloads")
        move_files("server", "backup")

        download_url = asset["browser_download_url"]
        output_path = os.path.join("downloads", asset_name)

        print(f"Downloading {asset_name} from {download_url}...")
        download_asset(download_url, output_path)
        extract_7z(output_path, "")
    
    subprocess.Popen(["python", "server/server.py"])


if __name__ == "__main__":
    main()
    sys.exit(1)
