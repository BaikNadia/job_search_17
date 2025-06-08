import pytest

from src.vacancies import Vacancy


def test_vacancy_initialization():
    """Проверяет инициализацию атрибутов вакансии"""
    vacancy = Vacancy("Python Developer", "https://example.com ", "100000-150000 руб.", "Описание")
    assert vacancy.title == "Python Developer"
    assert vacancy.link == "https://example.com "
    assert vacancy.salary == 100000
    assert vacancy.description == "Описание"

def test_salary_parsing():
    """Проверяет корректный парсинг зарплаты из разных форматов"""
    assert Vacancy._parse_salary("от 100000 руб.") == 100000  # Формат "от"
    assert Vacancy._parse_salary("100000-150000 руб.") == 100000  # Диапазон
    assert Vacancy._parse_salary("120000 руб.") == 120000  # Точное значение
    assert Vacancy._parse_salary({"from": 100000, "to": 150000, "currency": "RUR"}) == 100000  # Словарь
    assert Vacancy._parse_salary({"to": 150000, "currency": "RUR"}) == 150000  # Только "to"
    assert Vacancy._parse_salary("не указана") == 0.0  # Не указано
    assert Vacancy._parse_salary(None) == 0.0  # None
    assert Vacancy._parse_salary("до 150000") == 0.0  # "до" — не учитывается


def test_vacancy_validation():
    """Проверяет валидацию названия и ссылки"""
    with pytest.raises(ValueError):
        Vacancy("", "https://example.com ", "100000", "Описание")

    with pytest.raises(ValueError):
        Vacancy("Вакансия", "example.com", "100000", "Описание")


def test_cast_to_object_list():
    """Проверяет преобразование JSON в список объектов Vacancy"""
    raw_data = [{
        "name": "Python Developer",
        "alternate_url": "https://hh.ru/vacancy/123 ",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "snippet": {
            "requirement": "Опыт работы от 3 лет",
            "responsibility": "Разработка на Python"
        }
    }]
    vacancies = Vacancy.cast_to_object_list(raw_data)
    assert len(vacancies) == 1
    assert vacancies[0].title == "Python Developer"
    assert vacancies[0].salary == 100000  # Теперь парсится корректно как int


def test_cast_to_object_list_with_empty_fields():
    """Проверяет, что вакансии с пустыми полями не добавляются"""
    raw_data = [{
        "name": "",
        "alternate_url": "example.com",
        "salary": None,
        "snippet": {}
    }]

    vacancies = Vacancy.cast_to_object_list(raw_data)
    assert len(vacancies) == 0  # ✅ Теперь такие вакансии не создаются

def test_cast_to_object_list_with_salary_to():
    """Проверяет, что вакансия создаётся с 'to' как fallback"""
    raw_data = [{
        "name": "Java Developer",
        "alternate_url": "https://hh.ru/vacancy/456 ",
        "salary": {"to": 150000, "currency": "RUR"},
        "snippet": {"requirement": "Знание Spring Boot"}
    }]
    vacancies = Vacancy.cast_to_object_list(raw_data)
    assert len(vacancies) == 1
    assert vacancies[0].salary == 150000  # Теперь используем 'to' как fallback

def test_vacancy_comparison():
    """Проверяет сравнение вакансий по зарплате"""
    v1 = Vacancy("Вакансия1", "https://ex.com/1 ", "80000", "Описание1")
    v2 = Vacancy("Вакансия2", "https://ex.com/2 ", "120000", "Описание2")
    v3 = Vacancy("Вакансия3", "https://ex.com/3 ", "120000", "Описание3")

    assert v1 < v2
    assert v2 == v3
    assert v1 != v2
    assert v2 > v1


def test_vacancy_str():
    """Проверяет строковое представление вакансии"""
    vacancy = Vacancy("Python Developer", "https://example.com    ", "100000-150000 руб.", "Описание: опыт от 3 лет...")
    expected = (
        "Python Developer\n"
        "Ссылка: https://example.com    \n"
        "Зарплата: 100000 руб.\n"
        "Описание: Описание: опыт от 3 лет..."
    )
    assert str(vacancy) == expected