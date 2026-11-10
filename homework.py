import os
import requests
from requests.exceptions import RequestException

# 1. Базовый класс APIRequester


class APIRequester:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str = "") -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except RequestException as e:
            print(f"Ошибка при выполнении запроса к {url}: {e}")
            raise


class SWRequester(APIRequester):
    def get_sw_categories(self) -> list:
        response = self.get()
        categories_dict = response.json()
        return list(categories_dict.keys())

    def get_sw_info(self, sw_type: str) -> str:
        endpoint = f"{sw_type}/"
        response = self.get(endpoint)
        return response.text


def save_sw_data():

    sw_client = SWRequester(base_url="https://swapi.dev/api/")

    os.makedirs("data", exist_ok=True)

    categories = sw_client.get_sw_categories()

    for category in categories:
        print(f"Загрузка данных для категории: {category}...")
        data_str = sw_client.get_sw_info(category)

        file_path = os.path.join("data", f"{category}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(data_str)

    print("Все данные успешно сохранены в папку 'data'!")


# Пример запуска кода:
if __name__ == "__main__":
    save_sw_data()
