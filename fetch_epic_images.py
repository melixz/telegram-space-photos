import os
import requests
import argparse
from common import download_image
from dotenv import load_dotenv


load_dotenv()


def get_epic_image_urls(api_key, count=10):
    base_url = "https://api.nasa.gov/EPIC/api/natural"
    params = {'api_key': api_key}
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data:
        print("Нет данных от EPIC.")
        return []

    image_urls = []
    for item in data[:count]:
        image_date = item['date'].split()[0]
        image_name = item['image']
        image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{image_date.replace('-', '/')}/png/{image_name}.png"
        image_urls.append(image_url)

    return image_urls


def download_epic_images(api_key, count=10):
    image_urls = get_epic_image_urls(api_key, count)
    if not image_urls:
        print("Фотографии не найдены.")
        return

    os.makedirs('epic_images', exist_ok=True)

    for index, url in enumerate(image_urls):
        save_path = os.path.join('epic_images', f'epic_image_{index}.png')
        download_image(url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить фотографии NASA EPIC')
    parser.add_argument('--count', type=int, default=10, help='Количество изображений для загрузки')
    args = parser.parse_args()

    api_key = os.getenv('NASA_API_TOKEN')
    if not api_key:
        raise ValueError("NASA_API_TOKEN не найден")

    download_epic_images(api_key, args.count)


if __name__ == '__main__':
    main()
