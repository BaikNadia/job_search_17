from abc import ABC, abstractmethod
from typing import List, Dict

import requests


class VacancyAPI(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Подключается к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получает вакансии по поисковому запросу"""
        pass


class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        self._base_url = "https://api.hh.ru/"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self._params = {"text": "", "per_page": 100}
        self._connected = False

    def connect(self) -> None:
        """Проверяет подключение к API hh.ru"""
        try:
            test_params = {"text": "test", "per_page": 1}
            response = requests.get(self._base_url, headers=self._headers, params=test_params)
            response.raise_for_status()  # Проверяет статус ответа
            self._connected = True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения к hh.ru: {e}")
            self._connected = False

    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получает вакансии по поисковому запросу"""
        if not self._connected:
            print("Подключение к API не установлено.")
            return []

        self._params["text"] = search_query
        try:
            response = requests.get(self._base_url, headers=self._headers, params=self._params)
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных: {e}")
            return []
