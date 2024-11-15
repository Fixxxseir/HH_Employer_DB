from typing import Any

import requests

from src.base_hh_api import Parser


class HeadHunterAPI(Parser):
    """Получение данных  с API HeadHunter"""

    def __init__(self):
        """Инициализация класса"""
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"employer_id": "", "page": 0, "per_page": 100}
        self.__vacancies = []

    def __connect_to_api(self) -> None:
        """Проверка подключения к api hh.ru"""
        response = requests.get(self.__url)
        if response.status_code != 200:
            raise Exception(f"Не удается подключится, код: {response.status_code}")

    def load_vacancies(self, employer_id: str) -> list[dict[str, Any]]:
        """Получение вакансий по id работодателя"""
        self.__connect_to_api()
        self.__params["employer_id"] = employer_id
        while self.__params.get("page") != 10:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

        return self.__vacancies

    @property
    def get_vacancies(self) -> list[dict[str, Any]]:
        """Отдает список вакансий"""
        return self.__vacancies


# if __name__ == "__main__":
#     sub = HeadHunterAPI()
#     sub.load_vacancies(1740)
#     vacancies_sub = sub.get_vacancies
#
#     print(vacancies_sub)

# employers = (["1740", "Yandex"],
#              ["3529", "Сбер"],
#              ["109542064", "Aston"],
#              ["738", "Аурига"],
#              ["1062788", "OOO Napoleon IT"],
#              ["109240500", "Алабуга"],
#              ["15478", "Вконтакте"],
#              ["633069", "Selectel"],
#              ["4649269", "+ I ti"],
#              ["80", "Альфа банк"]
#              )
