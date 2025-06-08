# job_search_17
Этот проект позволяет получать данные о вакансиях с hh.ru, сохранять их в JSON-файл и взаимодействовать 
с пользователем через консоль.

## Функционал
- Получение вакансий с hh.ru по поисковому запросу.

- Сохранение данных в JSON-файл.
 
- Фильтрация вакансий по ключевым словам и зарплате.
 
- Сортировка вакансий по зарплате.
 
- Вывод вакансий в удобном формате.

## Структура проекта

project/
├── src/
│ ├── api_interactions.py # VacancyAPI, HeadHunterAPI
│ ├── vacancies.py # Vacancy
│ ├── filehandler.py # FileHandler, JSONSaver
│ └── main.py # user_interaction, вспомогательные функции
└── tests/
├── test_api_interactions.py
├── test_vacancies.py
└── test_filehandler.py

