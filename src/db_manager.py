from typing import Any

import psycopg2

from config import config


class DBManager:
    """Класс по работе с базой данных через SQL запросы"""

    def __init__(self, db_name: str = "vacancies") -> None:

        self.db_name = db_name
        self.__params = config()

    def __db_connect(self):
        return psycopg2.connect(dbname=self.db_name, **self.__params)

    def get_companies_and_vacancies_count(self) -> list[str]:
        """Метод получает список всех компаний и кол-во вакансий у каждой компании"""
        conn = self.__db_connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.employer_name, COUNT(*) AS vacancies_count
                FROM vacancies
                JOIN employers e USING(employer_id)
                GROUP BY employer_name
                ORDER BY vacancies_count DESC;
                """
            )
            get_counter = cur.fetchall()
        conn.close()

        return [f"{employer[0]}: {employer[1]} вакансий" for employer in get_counter]

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """Метод получает список всех вакансий"""
        conn = self.__db_connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT e.employer_name, v.vacancy_name, v.salary_from, v.salary_to, v.vacancy_url
                FROM vacancies v
                JOIN employers e USING(employer_id)
                WHERE v.salary_from <> 0
                ORDER BY v.salary_from DESC;
                """
            )
            get_all = cur.fetchall()
        conn.close()
        return get_all

    def get_avg_salary(self) -> str:
        """Метод возвращает среднюю зарплату по вакансиям"""
        conn = self.__db_connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary_from) AS avg_salary
                FROM vacancies
                WHERE salary_from <> 0;
                """
            )
            salary_from = round(cur.fetchone()[0], 2)

            cur.execute(
                """
                SELECT AVG(salary_to) AS avg_salary
                FROM vacancies
                WHERE salary_to <> 0;
                """
            )
            salary_to = round(cur.fetchone()[0], 2)

        conn.close()

        return f"Средняя зарплата: {salary_from} - {salary_to}\n"

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """Метод получает список всех вакансий с зарплатами выше средней"""
        conn = self.__db_connect()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT employer_name, v.vacancy_name, v.salary_from
                FROM employers
                JOIN vacancies v USING(employer_id)
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
                """
            )
            higher_salary = cur.fetchall()
        conn.close()
        return higher_salary

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """ "Метод возвращает выборку по вакансиям, у которых присутствует ключевое слово в названии"""
        conn = self.__db_connect()
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT e.employer_name, vacancy_name, salary_from, salary_to, vacancy_url
                FROM vacancies
                JOIN employers e USING(employer_id)
                WHERE vacancy_name iLIKE '%{keyword}%';
                """
            )
            finder_keyword = cur.fetchall()
        conn.close()
        return finder_keyword
