import os
import json

import pytest

from src.filehandler import JSONSaver
from src.vacancies import Vacancy

@pytest.fixture
def test_json_file():
    filename = "test_vacancies.json"
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    if os.path.exists(filename):
        os.remove(filename)

def test_json_saver_add_vacancy(test_json_file):
    """Проверяет добавление вакансии в файл"""
    saver = JSONSaver(test_json_file)
    vacancy = Vacancy("Python Developer", "https://example.com ", "100000-150000 руб.", "Описание")
    saver.add_vacancy(vacancy)

    with open(test_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1
    assert data[0]["title"] == "Python Developer"

def test_json_saver_add_duplicate_vacancy(test_json_file):
    """Проверяет, что дубли не добавляются"""
    saver = JSONSaver(test_json_file)
    vacancy = Vacancy("Python Developer", "https://example.com ", "100000-150000 руб.", "Описание")
    saver.add_vacancy(vacancy)
    saver.add_vacancy(vacancy)

    with open(test_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert len(data) == 1


def test_json_saver_delete_vacancy(test_json_file):
    """Проверяет удаление вакансии из файла"""
    saver = JSONSaver(test_json_file)
    vacancy = Vacancy("Тест", "https://example.com ", "100000", "Описание")
    saver.add_vacancy(vacancy)
    saver.delete_vacancy(vacancy)

    with open(test_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    assert data == []
