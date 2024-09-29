
import os
from dotenv import load_dotenv
from Ton import TonClient, TonContract
from PIL import Image
import requests
import json

load_dotenv()

# Настройки
TON_API_URL = os.getenv('TON_API_URL')
NFT_CONTRACT_ADDRESS = os.getenv('NFT_CONTRACT_ADDRESS')
W3_BASE_URL = "https://api.what3words.com/v3/"
W3_API_KEY = os.getenv('W3_API_KEY')

# Функция для создания NFT
def create_nft(tree_image_path, w3_words, location_image_path):
    # Загрузка изображения дерева
    with open(tree_image_path, 'rb') as tree_image:
        tree_image_data = tree_image.read()

    # Загрузка изображения с местоположением
    with open(location_image_path, 'rb') as location_image:
        location_image_data = location_image.read()

    # Создание метаданных NFT
    metadata = {
        "name": f"Tree NFT - {w3_words}",
        "description": "NFT, который показывает посаженное дерево и его местоположение.",
        "image": f"data:image/jpeg;base64,{base64.b64encode(tree_image_data).decode()}",
        "location_image": f"data:image/jpeg;base64,{base64.b64encode(location_image_data).decode()}",
        "w3_words": w3_words
    }

    # Отправка метаданных на сервер NFT
    response = requests.post(f"{TON_API_URL}/nft", json=metadata)
    return response.json()

# Функция для получения изображения по координатам
def get_location_image(w3_words):
    response = requests.get(f"{W3_BASE_URL}convert-to-coordinates?words={w3_words}&key={W3_API_KEY}")
    coordinates = response.json()
    
    latitude = coordinates['coordinates']['lat']
    longitude = coordinates['coordinates']['lng']
    
    location_response = requests.get(f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/{longitude},{latitude},14.25,0,0/600x400?access_token={os.getenv('MAPBOX_ACCESS_TOKEN')}")
    
    with open("location_image.png", "wb") as f:
        f.write(location_response.content)

    return "location_image.png"

# Пример использования
tree_image_path = "path_to_your_tree_image.jpg"  # Путь к изображению дерева
w3_words = "filled.count.soap"  # Пример what3words
location_image_path = get_location_image(w3_words)

nft_data = create_nft(tree_image_path, w3_words, location_image_path)
print("NFT создан:", nft_data)
