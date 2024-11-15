from src.db_filler import DBFiller
from src.db_maker import DBMaker
from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI
from src.utils import get_employer_to_dict, get_vacancies_to_dict


def main(employers: list[str]) -> None:
    db = DBMaker()
    db.create_db()
    print("База данных создана")
    db.create_table_employers()
    print("Создана таблица с работодателями")
    db.create_table_vacancies()
    print("Создана таблица с вакансиями от работодателей")
    print("""...подождите...\nПроисходит заполнение таблиц\n...подождите...\n""")

    for employer in employers:
        hh = HeadHunterAPI().load_vacancies(employer)
        emp_data = get_employer_to_dict(hh[0])
        vac_data = [get_vacancies_to_dict(employer) for employer in hh]
        db_filler = DBFiller()
        db_filler.into_date_to_database(emp_data, vac_data)
    print("Таблицы с вакансиями и работодателями успешно заполнены")

    manager = DBManager()

    while True:
        user_input = input(
            "\nВведите цифру для получения нужной Вам информации.\n"
            "1. получает список всех компаний и количество вакансий у каждой компании.\n"
            "2. получить список всех вакансий.\n"
            "3. получить среднюю зарплату по всем вакансиям.\n"
            "4. получить список всех вакансий с зарплатой выше средней.\n"
            "5. получить выборку по вакансиям, у которых присутствует ключевое слово в названии.\n"
            "Введите номер варианта или stop или 12312312312381239812 что бы завершить сеанс.\n"
            "Ввод:   "
        )
        if user_input == "1":
            companies_and_vacancies_count = manager.get_companies_and_vacancies_count()
            print("Cписок всех компаний и количество вакансий у каждой компании:")
            for i in companies_and_vacancies_count:
                print(i)
        elif user_input == "2":
            all_vacancies = manager.get_all_vacancies()
            print(
                """
            список всех вакансий:
            """
            )
            for i in all_vacancies:
                print(i)
        elif user_input == "3":
            avg_salary = manager.get_avg_salary()
            print(avg_salary)
        elif user_input == "4":
            vacancies_with_higher_salary = manager.get_vacancies_with_higher_salary()
            print("список всех вакансий с зарплатой выше средней:")
            for i in vacancies_with_higher_salary:
                print(i)
        elif user_input == "5":
            user_word = input("Введите ключ слово\n").lower()
            vacancies_with_keyword = manager.get_vacancies_with_keyword(user_word)
            print("выборка по вакансиям, у которых присутствует ключевое слово в названии:")
            for i in vacancies_with_keyword:
                print(i)
        elif user_input == "stop" or "12312312312381239812":
            print("Программа завершила работу")
            break


if __name__ == "__main__":
    employers_list = ["1740", "3529", "6093775", "738", "1062788", "68587", "15478", "633069", "4649269", "80"]
    main(employers_list)

    # employers_list = (["1740", "Yandex"],
    #                   ["3529", "Сбер"],
    #                   ["6093775", "Aston"],
    #                   ["738", "Аурига"],
    #                   ["1062788", "OOO Napoleon IT"],
    #                   ["68587", "Алабуга"],
    #                   ["15478", "Вконтакте"],
    #                   ["633069", "Selectel"],
    #                   ["4649269", "+ I ti"],
    #                   ["80", "Альфа банк"]
    #                   )
