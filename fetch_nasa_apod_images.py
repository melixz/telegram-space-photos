import argparse
import os
import requests
from common import download_image, get_file_extension_from_url
from dotenv import load_dotenv


def download_nasa_apod_images(api_key, count=1):
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': api_key, 'count': count}
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    apod_data_list = response.json()

    os.makedirs('images', exist_ok=True)
    image_paths = []

    for index, apod_data in enumerate(apod_data_list):
        image_url = apod_data.get('url')
        if not image_url:
            print(f"URL изображения не найден для записи {index}.")
            continue

        file_extension = get_file_extension_from_url(image_url)
        save_path = os.path.join('images', f'nasa_apod_{index}{file_extension}')
        download_image(image_url, save_path)
        image_paths.append(save_path)

    return image_paths


def main():
    parser = argparse.ArgumentParser(description='Загрузить фотографии NASA APOD')
    parser.add_argument('--count', type=int, default=50, help='Количество изображений для загрузки')
    args = parser.parse_args()

    api_key = os.getenv('NASA_API_TOKEN')
    if not api_key:
        raise ValueError("NASA_API_TOKEN не найден")

    image_paths = download_nasa_apod_images(api_key, args.count)
    for image_path in image_paths:
        print(f"Image downloaded: {image_path}")


if __name__ == '__main__':
    load_dotenv()
    main()
