import os
import requests


url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'


os.makedirs('images', exist_ok=True)


file_path = os.path.join('images', 'hubble.jpeg')


response = requests.get(url)


with open(file_path, 'wb') as file:
    file.write(response.content)

print(f"Изображение сохранено как {file_path}")
