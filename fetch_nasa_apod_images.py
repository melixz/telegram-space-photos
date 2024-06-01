import os
import requests
import argparse
from common import download_image, get_file_extension_from_url
from dotenv import load_dotenv


load_dotenv()


def download_nasa_apod_images(api_key, count=50):
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': api_key, 'count': count}
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    apod_data_list = response.json()

    os.makedirs('images', exist_ok=True)

    for index, apod_data in enumerate(apod_data_list):
        image_url = apod_data.get('url')
        if not image_url:
            print(f"URL изображения не найден для записи {index}.")
            continue

        file_extension = get_file_extension_from_url(image_url)
        save_path = os.path.join('images', f'nasa_apod_{index}{file_extension}')
        download_image(image_url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить фотографии NASA APOD')
    parser.add_argument('--count', type=int, default=50, help='Количество изображений для загрузки')
    args = parser.parse_args()

    api_key = os.getenv('NASA_API_TOKEN')
    if not api_key:
        raise ValueError("NASA_API_TOKEN не найден")

    download_nasa_apod_images(api_key, args.count)


if __name__ == '__main__':
    main()
