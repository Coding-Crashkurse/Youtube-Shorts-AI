import os
import requests

class PexelsImageSearch:
    def __init__(self, api_key: str, folder_name: str = "data"):
        self.api_key = api_key
        self.folder_name = folder_name
        self.base_url = "https://api.pexels.com/v1/search"
        self._create_folder_if_not_exists()

    def process_images(self, query: str, per_page: int = 4) -> None:
        images = self._search_images(query, per_page)
        self._save_images(images)

    def _search_images(self, query: str, per_page: int) -> dict:
        headers = {"Authorization": self.api_key}
        params = {"query": query, "per_page": per_page}
        response = requests.get(self.base_url, headers=headers, params=params)
        return response.json()

    def _save_images(self, images: dict) -> None:
        for index, photo in enumerate(images['photos']):
            image_url = photo['src']['original']
            file_extension = image_url.split('.')[-1]
            filename = f"{self.folder_name}_{index}.{file_extension}"
            self._save_image(image_url, filename)

    def _save_image(self, url: str, filename: str) -> None:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(self.folder_name, filename), 'wb') as file:
                file.write(response.content)

    def _create_folder_if_not_exists(self) -> None:
        if not os.path.exists(self.folder_name):
            os.makedirs(self.folder_name)
