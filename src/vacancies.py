from typing import Optional, List, Dict, Union


class Vacancy:
    __slots__ = ["_title", "_link", "_salary", "_description"]

    def __init__(self, title: str, link: str, salary: Optional[Union[str, Dict]], description: str):
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
    def _parse_salary(salary: Optional[Union[str, Dict]]) -> float:
        """Обрабатывает зарплату из разных форматов и возвращает минимальное значение или 0"""
        if not salary:
            return 0.0

        # Случай: salary — словарь с 'from' и 'to'
        if isinstance(salary, dict):
            min_salary = salary.get("from")
            max_salary = salary.get("to")
            currency = salary.get("currency", "")

            if min_salary is not None:
                return float(min_salary)
            elif max_salary is not None:
                return float(max_salary)  # Используем 'to' как fallback
            else:
                return 0.0

        # Случай: salary — строка
        if isinstance(salary, str):
            cleaned = salary.replace("\u00a0", "").strip()
            if "от" in cleaned:
                try:
                    return float(cleaned.replace("от", "").strip().split()[0])
                except (ValueError, IndexError):
                    return 0.0
            elif "до" in cleaned:
                return 0.0  # Зарплата "до" — не подходит для фильтрации по минимуму
            elif "-" in cleaned:
                try:
                    return float(cleaned.split("-")[0].strip().split()[0])
                except (ValueError, IndexError):
                    return 0.0
            else:
                try:
                    return float(cleaned.split()[0])
                except (ValueError, IndexError):
                    return 0.0

        return 0.0


    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List["Vacancy"]:
        """Преобразует сырые данные в список объектов Vacancy"""
        vacancies = []

        for item in data:
            title = item.get("name")
            link = item.get("alternate_url")
            salary = item.get("salary")
            description = item.get("snippet", {})
            requirement = description.get("requirement") or description.get("responsibility") or "Описание отсутствует"

            # Пропускаем вакансию, если title или link пустые
            if not title or not link:
                continue  # ✅ Пропускаем некорректные вакансии

            try:
                vacancies.append(cls(title, link, salary, requirement))
            except ValueError as e:
                # Можно логировать или игнорировать
                print(f"Ошибка при инициализации вакансии: {e}")
                continue

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
        salary_str = f"{int(self.salary)}" if self.salary != 0 else "Не указана"
        desc_preview = self.description[:100] + "..." if len(self.description) > 100 else self.description
        return (
            f"{self.title}\n"
            f"Ссылка: {self.link}\n"
            f"Зарплата: {salary_str} руб.\n"
            f"Описание: {desc_preview}"
        )