from typing import Optional, List, Dict



class Vacancy:
    __slots__ = ["_title", "_link", "_salary", "_description"]

    def __init__(self, title: str, link: str, salary: Optional[str], description: str):
        self._title = self._validate_title(title)
        self._link = self._validate_link(link)
        self._description = description
        self._salary = self._parse_salary(salary)

    @staticmethod
    def _validate_title(title: str) -> str:
        """Проверяет, что название вакансии не пустое"""
        if not title:
            raise ValueError("Название вакансии не может быть пустым")
        return title

    @staticmethod
    def _validate_link(link: str) -> str:
        """Проверяет, что ссылка корректная"""
        if not link.startswith("http"):
            raise ValueError("Ссылка должна начинаться с http:// или https://")
        return link

    @staticmethod
    def _parse_salary(salary: Optional[str]) -> float:
        """Обрабатывает зарплату, если она указана"""
        if not salary:
            return 0.0
        try:
            cleaned = salary.replace("\u00a0", "").replace("руб.", "").strip()
            if "-" in cleaned:
                min_salary, max_salary = map(float, cleaned.split("-"))
                return max_salary
            return float(cleaned)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def cast_to_object_list(data: List[Dict]) -> List["Vacancy"]:
        """Преобразует сырые данные в список объектов Vacancy"""
        vacancies = []
        for item in data:
            title = item["name"]
            link = item["alternate_url"]
            salary = item.get("salary")
            salary_str = f"{salary['from']}-{salary['to']} {salary['currency']}" if salary else None
            description = item["snippet"]["requirement"] or item["snippet"]["responsibility"] or "Описание отсутствует"
            vacancies.append(Vacancy(title, link, salary_str, description))
        return vacancies

    @property
    def title(self) -> str:
        return self._title

    @property
    def link(self) -> str:
        return self._link

    @property
    def salary(self) -> float:
        return self._salary

    @property
    def description(self) -> str:
        return self._description

    def __lt__(self, other: "Vacancy") -> bool:
        return self.salary < other.salary

    def __eq__(self, other: "Vacancy") -> bool:
        return self.salary == other.salary

    def __str__(self) -> str:
        return f"{self.title}\nСсылка: {self.link}\nЗарплата: {self.salary or 'Не указана'} руб.\nОписание: {self.description[:100]}..."
