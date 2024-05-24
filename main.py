import os
import requests


def download_image(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()

    with open(save_path, 'wb') as file:
        file.write(response.content)

    print(f"Изображение сохранено как {save_path}")


image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
save_path = 'images/hubble.jpeg'

download_image(image_url, save_path)
