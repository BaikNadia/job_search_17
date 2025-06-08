from typing import List

from src.api_interactions import HeadHunterAPI
from src.filehandler import JSONSaver
from src.vacancies import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам"""
    return [
        v for v in vacancies
        if any(word.lower() in v.title.lower() or word.lower() in v.description.lower() for word in keywords)
    ]


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрует вакансии по зарплате"""
    if not salary_range:
        return vacancies
    try:
        min_sal, max_sal = map(float, salary_range.split("-"))
        return [v for v in vacancies if min_sal <= v.salary <= max_sal]
    except ValueError:
        return []


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по зарплате"""
    return sorted(vacancies, key=lambda v: v.salary, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Возвращает топ N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]):
    """Выводит вакансии пользователю"""
    if not vacancies:
        print("Нет вакансий по вашему запросу.")
        return

    for idx, vacancy in enumerate(vacancies, 1):
        print(f"{idx}. {vacancy.title}")
        print(f"Ссылка: {vacancy.link}")
        print(f"Зарплата: {vacancy.salary or 'Не указана'} руб.")
        print(f"Описание: {vacancy.description[:100]}...\n")


def user_interaction():
    """Функция взаимодействия с пользователем"""
    hh_api = HeadHunterAPI()
    hh_api.connect()

    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)

    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    json_saver = JSONSaver("vacancies.json")
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации: ").split()
    salary_range = input("Введите диапазон зарплат (пример: 100000-150000): ")

    filtered = filter_vacancies(vacancies_list, filter_words)
    ranged = get_vacancies_by_salary(filtered, salary_range)
    sorted_vacancies = sort_vacancies(ranged)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
