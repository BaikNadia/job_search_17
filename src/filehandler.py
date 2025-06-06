import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from src.vacancies import Vacancy


class FileHandler(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, keywords: Optional[List[str]] = None, salary_range: Optional[str] = None) -> List[Vacancy]:
        """Возвращает список вакансий по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из файла"""
        pass


class JSONSaver(FileHandler):
    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as file:
                file.write("[]")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        data = self._load_data()
        vacancy_dict = {
            "title": vacancy.title,
            "link": vacancy.link,
            "salary": vacancy.salary,
            "description": vacancy.description
        }
        if vacancy_dict not in data:
            data.append(vacancy_dict)
            self._save_data(data)

    def get_vacancies(self, keywords: Optional[List[str]] = None, salary_range: Optional[str] = None) -> List[Vacancy]:
        data = self._load_data()
        filtered = []

        for item in data:
            match = True
            if keywords:
                text = f"{item['title']} {item['description']}".lower()
                match &= any(word.lower() in text for word in keywords)
            if salary_range:
                min_sal, max_sal = map(float, salary_range.split("-"))
                match &= min_sal <= item["salary"] <= max_sal
            if match:
                filtered.append(Vacancy(**item))
        return filtered

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        data = self._load_data()
        data = [item for item in data if item["link"] != vacancy.link]
        self._save_data(data)

    # def _load_data(self) -> List[Dict]:
    #     with open(self._filename, "r", encoding="utf-8") as file:
    #         return json.load(file)

    def _load_data(self) -> List[Dict]:
        """Загружает данные из файла. Если файл пустой или поврежден — возвращает пустой список"""
        try:
            with open(self._filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        return data

    def _save_data(self, data: List[Dict]) -> None:
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
