import os
import requests
import argparse
from common import download_image


def spacex_api_latest(api_url, save_path, params=None):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    launch_data = response.json()
    image_url = launch_data['links']['flickr']['original'][0] if launch_data['links']['flickr']['original'] else None
    if image_url:
        download_image(image_url, save_path)
    else:
        print("Изображение не найдено в данных последнего запуска")


def spacex_api_by_id(api_url, flight_id):
    response = requests.get(f"{api_url}/{flight_id}")
    response.raise_for_status()
    launch_data = response.json()
    image_urls = launch_data['links']['flickr']['original'] if launch_data['links']['flickr']['original'] else []
    return image_urls


def save_spacex_photos_to_folder(api_url, flight_id):
    photos = spacex_api_by_id(api_url, flight_id)
    if not photos:
        print("Фотографии не найдены.")
        return

    os.makedirs('images', exist_ok=True)

    for index, url in enumerate(photos):
        save_path = f'images/spacex_{index}.jpg'
        download_image(url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить фотографии SpaceX по ID запуска')
    parser.add_argument('--flight_id', type=str, help='ID запуска SpaceX')
    args = parser.parse_args()

    if args.flight_id:
        save_spacex_photos_to_folder('https://api.spacexdata.com/v5/launches', args.flight_id)
    else:
        spacex_api_latest('https://api.spacexdata.com/v5/launches/latest', 'images/spacex_latest.jpeg')


if __name__ == '__main__':
    main()
