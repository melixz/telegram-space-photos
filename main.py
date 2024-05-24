import os
import requests


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


image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
save_path = 'images/hubble.jpeg'
download_image(image_url, save_path)


api_url_latest = 'https://api.spacexdata.com/v5/launches/latest'
spacex_save_path_latest = 'images/spacex_latest.jpeg'
spacex_api_latest(api_url_latest, spacex_save_path_latest)


api_url_by_id = 'https://api.spacexdata.com/v5/launches'
flight_id = '5eb87d47ffd86e000604b38a'
save_spacex_photos_to_folder(api_url_by_id, flight_id)
