from typing import Any


def get_employer_to_dict(hh_api_data: dict[str, Any]) -> dict[str, Any]:
    """Вытягивание из JSON ответа данных и преобразование в словарь работодателей для БД"""
    if hh_api_data.get("employer")["name"]:
        employer_name = hh_api_data.get("employer")["name"]
    else:
        employer_name = "empty"
    if hh_api_data.get("employer")["id"]:
        employer_id = hh_api_data.get("employer")["id"]
    else:
        employer_id = 0
    if hh_api_data.get("employer")["alternate_url"]:
        employer_url = hh_api_data.get("employer")["alternate_url"]
    else:
        employer_url = "empty"
    if hh_api_data.get("area")["name"]:
        employer_area = hh_api_data.get("area")["name"]
    else:
        employer_area = "empty"

    return {
        "employer_id": employer_id,
        "employer_name": employer_name,
        "employer_url": employer_url,
        "employer_area": employer_area,
    }


def get_vacancies_to_dict(hh_api_data: dict[str, Any]) -> dict[str, Any]:
    """Вытягивание из JSON ответа данных и преобразование в словарь вакансий для БД"""

    if hh_api_data.get("name"):
        vacancies_name = hh_api_data.get("name")
    else:
        vacancies_name = "empty"
    if hh_api_data.get("salary"):
        vacancies_salary_from = (
            hh_api_data.get("salary")["from"] if hh_api_data.get("salary")["from"] is not None else 0
        )
    else:
        vacancies_salary_from = 0
    if hh_api_data.get("salary"):
        vacancies_salary_to = hh_api_data.get("salary")["to"] if hh_api_data.get("salary")["to"] is not None else 0
    else:
        vacancies_salary_to = 0
    if hh_api_data.get("snippet")["responsibility"]:
        vacancies_description = hh_api_data.get("snippet")["responsibility"]
    else:
        vacancies_description = "empty"
    if hh_api_data.get("snippet")["requirement"]:
        vacancies_requirement = hh_api_data.get("snippet")["requirement"]
    else:
        vacancies_requirement = "empty"
    if hh_api_data.get("alternate_url"):
        vacancies_vacancy_url = hh_api_data.get("alternate_url")
    else:
        vacancies_vacancy_url = "empty"

    return {
        "vacancies_name": vacancies_name,
        "salary_from": vacancies_salary_from,
        "salary_to": vacancies_salary_to,
        "description": vacancies_description,
        "requirement": vacancies_requirement,
        "vacancy_url": vacancies_vacancy_url,
    }
