import psycopg2

from config import config


class DBMaker:
    """Создание базы данных и таблиц"""

    def __init__(self, db_name: str = "vacancies") -> None:
        self.db_name = db_name
        self.__params = config(filename="database.ini")

    def create_db(self) -> None:
        """Создание базы данных"""
        conn = psycopg2.connect(database="postgres", **self.__params)
        cur = conn.cursor()
        conn.autocommit = True

        cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        cur.execute(f"CREATE DATABASE {self.db_name}")

        cur.close()
        conn.close()

    def create_table_employers(self) -> None:
        """Создание таблицы работодателей"""
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE TABLE employers (
                employer_id INT PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                employer_url TEXT,
                employer_area TEXT NOT NULL
                )"""
            )

        conn.commit()
        conn.close()

    def create_table_vacancies(self) -> None:
        """Создание таблицы вакансий"""
        conn = psycopg2.connect(dbname=self.db_name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                employer_id INT REFERENCES employers(employer_id),
                vacancy_name VARCHAR(255) NOT NULL,
                salary_from FLOAT,
                salary_to FLOAT,
                description TEXT,
                requirement TEXT,
                vacancy_url TEXT
                )"""
            )

        conn.commit()
        conn.close()


# if __name__ == "__main__":
#     s = DBMaker('test_dddd')
#     s.create_db()
