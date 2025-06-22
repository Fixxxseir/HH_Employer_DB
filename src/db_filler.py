from typing import Any

import psycopg2

from config import config


class DBFiller:
    """Класс заполняют базу данных"""

    def __init__(self, db_name: str = "vacancies") -> None:
        self.db_name = db_name
        self.params = config()

    def into_date_to_database(self, data_employers: dict[str, Any], data_vacancies: list[dict[str, Any]]) -> None:
        """Заполнение данными таблиц базы данных"""
        conn = psycopg2.connect(database=self.db_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employers
                (employer_id, employer_name, employer_url, employer_area)
                VALUES (%s, %s, %s, %s)
                RETURNING employer_id;
                """,
                (
                    data_employers.get("employer_id"),
                    data_employers.get("employer_name"),
                    data_employers.get("employer_url"),
                    data_employers.get("employer_area"),
                ),
            )

            employer_id = cur.fetchone()[0]
            for vacancy in data_vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies
                    (employer_id, vacancy_name, salary_from, salary_to, description, requirement, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        employer_id,
                        vacancy.get("vacancies_name"),
                        vacancy.get("salary_from"),
                        vacancy.get("salary_to"),
                        vacancy.get("description"),
                        vacancy.get("requirement"),
                        vacancy.get("vacancy_url"),
                    ),
                )

        conn.commit()
        conn.close()
