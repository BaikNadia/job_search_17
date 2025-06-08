from src.vacancies import Vacancy

def test_vacancy_initialization():
    """Проверяет инициализацию атрибутов вакансии"""
    vacancy = Vacancy("Python Developer", "https://example.com ", "100000-150000 руб.", "Требования: опыт работы от 3 лет...")
    assert vacancy.title == "Python Developer"
    assert vacancy.link == "https://example.com "
    assert vacancy.salary == 150000
    assert vacancy.description == "Требования: опыт работы от 3 лет..."


def test_vacancy_comparison():
    """Проверяет сравнение вакансий по зарплате"""
    v1 = Vacancy("Вакансия1", "https://ex.com/1 ", "100000", "")
    v2 = Vacancy("Вакансия2", "https://ex.com/2 ", "150000", "")
    assert v1 < v2
    assert v2 > v1
    assert v1 != v2
