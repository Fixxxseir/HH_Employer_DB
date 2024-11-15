from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс для парсинга данных"""

    @abstractmethod
    def load_vacancies(self, employer_id):
        """Получает данные в JSON формате с апи HeadHunter"""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Обычный геттр полученных данных который я не использовал))"""
        pass
