import os
import requests
import argparse
from common import download_image


def spacex_api_by_id(api_url, flight_id):
    response = requests.get(f"{api_url}/{flight_id}")
    response.raise_for_status()
    rocket_launch_data = response.json()
    image_urls = rocket_launch_data['links']['flickr']['original'] if rocket_launch_data['links']['flickr']['original'] else []
    return image_urls


def save_spacex_photos_to_folder(image_urls):
    if not image_urls:
        print("Фотографии не найдены.")
        return

    os.makedirs('images', exist_ok=True)

    for index, url in enumerate(image_urls):
        save_path = f'images/spacex_{index}.jpg'
        download_image(url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить фотографии SpaceX по ID запуска')
    parser.add_argument('--flight_id', type=str, help='ID запуска SpaceX')
    args = parser.parse_args()

    if args.flight_id:
        image_urls = spacex_api_by_id('https://api.spacexdata.com/v5/launches', args.flight_id)
        save_spacex_photos_to_folder(image_urls)
    else:
        print("ID запуска не указан")


if __name__ == '__main__':
    main()
