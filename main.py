import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote, urlencode


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


def get_file_extension_from_url(url):
    path = urlsplit(url).path
    filename = os.path.basename(unquote(path))
    _, extension = os.path.splitext(filename)
    return extension


def download_nasa_apod_images(api_key, count=50):
    apod_url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': api_key, 'count': count}

    # Кодируем параметры
    encoded_params = urlencode(params)
    full_url = f"{apod_url}?{encoded_params}"

    response = requests.get(full_url)
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
        response_img = requests.get(image_url)
        response_img.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response_img.content)
        print(f"Изображение сохранено как {save_path}")


load_dotenv()
api_key = os.environ.get('NASA_API_KEY')
download_nasa_apod_images(api_key, count=50)

test_url = "https://example.com/txt/hello%20world.txt?v=9#python"
print(get_file_extension_from_url(test_url))
