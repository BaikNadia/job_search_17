import requests

from src.api_interactions import HeadHunterAPI


def test_hh_api_connect_success():
    """Проверяет успешное подключение к hh.ru"""
    hh_api = HeadHunterAPI()
    hh_api.connect()
    assert hh_api._connected is True


def test_hh_api_connect_failure(monkeypatch):
    """Проверяет подключение при ошибке сети"""

    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr(requests, "get", mock_get)
    hh_api = HeadHunterAPI()
    hh_api.connect()
    assert hh_api._connected is False



def test_hh_api_get_vacancies_on_failure(monkeypatch):
    """Проверяет, что get_vacancies возвращает пустой список при ошибке"""

    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException("Ошибка запроса")

    monkeypatch.setattr(requests, "get", mock_get)
    hh_api = HeadHunterAPI()
    hh_api.connect()
    hh_api._connected = True
    vacancies = hh_api.get_vacancies("Python")
    assert vacancies == []
