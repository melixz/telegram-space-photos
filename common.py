import os
import requests
from urllib.parse import urlsplit, unquote


def download_image(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Изображение сохранено как {save_path}")


def get_file_extension_from_url(url):
    path = urlsplit(url).path
    filename = os.path.basename(unquote(path))
    _, extension = os.path.splitext(filename)
    return extension
