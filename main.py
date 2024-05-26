import os
import requests
from dotenv import load_dotenv


def download_image(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f"Изображение сохранено как {save_path}")


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


def fetch_spacex_last_launch():
    api_url_latest = 'https://api.spacexdata.com/v5/launches/latest'
    spacex_save_path_latest = 'images/spacex_latest.jpeg'
    spacex_api_latest(api_url_latest, spacex_save_path_latest)


def download_nasa_apod_image(api_key):
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': api_key, 'hd': True}
    response = requests.get(apod_url, params=params)
    response.raise_for_status()
    apod_data = response.json()
    image_url = apod_data.get('url')
    if not image_url:
        print("URL изображения не найден.")
        return
    save_path = os.path.join('images', 'nasa_apod_today.jpg')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response_img = requests.get(image_url)
    response_img.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response_img.content)
    print(f"Изображение сохранено как {save_path}")


load_dotenv()
api_key = os.environ.get('NASA_API_KEY')
download_nasa_apod_image(api_key)

fetch_spacex_last_launch()