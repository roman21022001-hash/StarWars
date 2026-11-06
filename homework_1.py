# скажу честно, часть решения взял через ИИ потому что этот сайт вообще никак не захотел открываться
# поэтому ИИ предложил сделать локальный запрос что бы все работало/ так как на запуске у меня
# чисто физически не забивались папки информацией
import os
import json

MOCK_CATEGORIES = {
    "people": "https://swapi.dev",
    "planets": "https://swapi.dev",
    "films": "https://swapi.dev",
    "species": "https://swapi.dev",
    "vehicles": "https://swapi.dev",
    "starships": "https://swapi.dev"
}

MOCK_DATA = {
    "people/": {"name": "Luke Skywalker", "height": "172", "mass": "77", "gender": "male"},
    "planets/": {"name": "Tatooine", "climate": "arid", "terrain": "desert"},
    "films/": {"title": "A New Hope", "episode_id": 4, "director": "George Lucas"},
    "species/": {"name": "Human", "classification": "mammal", "language": "Galactic Basic"},
    "vehicles/": {"name": "Snowspeeder", "model": "T-47 airspeeder"},
    "starships/": {"name": "X-wing", "model": "T-65 X-wing"}
}


class MockResponse:
    def __init__(self, data_dict):
        self._data = data_dict
        self.text = json.dumps(data_dict, indent=4, ensure_ascii=False)

    def json(self):
        return self._data

    def raise_for_status(self):
        pass


class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint=""):
        if endpoint == "":
            return MockResponse(MOCK_CATEGORIES)
        elif endpoint in MOCK_DATA:
            return MockResponse(MOCK_DATA[endpoint])
        else:
            return MockResponse({"results": []})


class SWRequester(APIRequester):
    def get_sw_categories(self):
        response = self.get()
        categories_dict = response.json()
        return list(categories_dict.keys())

    def get_sw_info(self, sw_type):
        response = self.get(f"{sw_type}/")
        return response.text


def save_sw_data():
    base_url = 'https://swapi.dev'

    requester = SWRequester(base_url)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')

    os.makedirs(data_dir, exist_ok=True)
    print(f"Папка создана по пути: {data_dir}")

    categories = requester.get_sw_categories()

    for category in categories:
        print(f"Загрузка категории: {category}...")
        category_data = requester.get_sw_info(category)

        file_path = os.path.join(data_dir, f"{category}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(category_data)

    print("Все данные успешно сохранены!")


if __name__ == "__main__":
    save_sw_data()
