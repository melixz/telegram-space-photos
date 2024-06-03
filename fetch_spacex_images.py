import os
import requests
import argparse
from common import download_image


def fetch_spacex_image_urls_by_flight_id(api_url, flight_id):
    response = requests.get(f"{api_url}/{flight_id}")
    response.raise_for_status()
    launch_data = response.json()
    image_urls = launch_data['links']['flickr']['original'] if launch_data['links']['flickr']['original'] else []
    return image_urls


def fetch_latest_spacex_image_urls(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    launch_data = response.json()
    image_urls = launch_data['links']['flickr']['original'] if launch_data['links']['flickr']['original'] else []
    return image_urls


def save_spacex_photos_to_folder(image_urls, folder_name='images'):
    if not image_urls:
        print("Фотографии не найдены.")
        return

    os.makedirs(folder_name, exist_ok=True)

    for index, url in enumerate(image_urls):
        save_path = os.path.join(folder_name, f'spacex_{index}.jpg')
        download_image(url, save_path)


def main():
    parser = argparse.ArgumentParser(description='Загрузить фотографии SpaceX по ID запуска или последнего запуска')
    parser.add_argument('--flight_id', type=str, help='ID запуска SpaceX')
    args = parser.parse_args()

    if args.flight_id:
        image_urls = fetch_spacex_image_urls_by_flight_id('https://api.spacexdata.com/v5/launches', args.flight_id)
        save_spacex_photos_to_folder(image_urls, folder_name=f'images/{args.flight_id}')
    else:
        image_urls = fetch_latest_spacex_image_urls('https://api.spacexdata.com/v5/launches/latest')
        save_spacex_photos_to_folder(image_urls, folder_name='images/latest')


if __name__ == '__main__':
    main()
