import math
import os
import sys

import requests
from dotenv import load_dotenv
from terminaltables import DoubleTable

STATISTICS_VACANCIES_SJ = {}
STATISTICS_VACANCIES_HH = {}
AVERAGE_SALARY = []
TABLE_DATA_VACANCIES = []


def predict_rub_salary_for_SuperJob(specialty, superjob_token):
    url = "https://api.superjob.ru/2.0/vacancies/catalogues/"

    headers = {
        "X-Api-App-Id": superjob_token
    }

    payload = {
        "t": "4",
        'keyword': specialty
    }

    data_vacancie = {}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    vacancies_total = response.json()['total']
    data_vacancie['vacancies_found'] = vacancies_total
    vacancies_on_page = 20
    pages = math.ceil(vacancies_total / vacancies_on_page)
    vacancies_suitable = 0
    page = 0
    while page < pages:
        response = requests.get(url, headers=headers,
                                params={'page': page, 'keyword': specialty, "t": "4"})
        response.raise_for_status()
        page += 1
        vacancies = response.json()['objects']
        for vacancy in vacancies:
            professions = vacancy['catalogues']
            for profession in professions:
                if profession['title'] == "IT, Интернет, связь, телеком":
                    if vacancy['currency'] == 'rub':
                        limit_lower = vacancy['payment_from']
                        limit_upper = vacancy['payment_to']
                        if limit_lower + limit_upper == 0:
                            pass
                        else:
                            vacancies_suitable += 1
                            predict_salary(limit_lower, limit_upper, AVERAGE_SALARY)
    data_vacancie['vacancies_processed'] = vacancies_suitable
    data_vacancie['average_salary'] = int(sum(AVERAGE_SALARY) / len(AVERAGE_SALARY))
    STATISTICS_VACANCIES_SJ[specialty] = data_vacancie
    return STATISTICS_VACANCIES_SJ


def predict_rub_salary_for_HeadHunter(specialty):
    url = "https://api.hh.ru/vacancies"
    vacancies_suitable = 0
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.132 Chrome/76.0.3809.132 Safari/537.36"
    }

    payload = {
        "text": f"Программист {specialty}",
        "area": "1",
        "period": "30",
        "only_with_salary": "true",
        "salary.from": "true",
        "salary.to": "true"
    }

    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    vacancies = response.json()['items']
    found = response.json()['found']
    pages = response.json()['pages']
    data_vacancies = dict(vacancies_found=found)
    page = 0
    while page < pages:
        response = requests.get(url, headers=headers, params={'page': page})
        response.raise_for_status()
        page += 1
        for vacancy in vacancies:
            if vacancy['salary']['currency'] != 'RUR':
                pass
            else:
                salary = vacancy['salary']
                limit_lower = salary['from']
                limit_upper = salary['to']
                if limit_lower and limit_upper is None:
                    pass
                else:
                    vacancies_suitable += 1
                    predict_salary(limit_lower, limit_upper, AVERAGE_SALARY)
    data_vacancies['vacancies_processed'] = vacancies_suitable
    data_vacancies['average_salary'] = int(sum(AVERAGE_SALARY) / len(AVERAGE_SALARY))
    STATISTICS_VACANCIES_HH[specialty] = data_vacancies
    return STATISTICS_VACANCIES_HH


def predict_salary(salary_from, salary_to, average_salary):
    if salary_from and salary_to is not None:
        average = int((salary_from + salary_to) / 2)
        average_salary.append(average)
    elif salary_from is None:
        average = int(salary_to * 0.8)
        average_salary.append(average)
    else:
        average = int(salary_from * 1.2)
        average_salary.append(average)
    return average_salary


def generate_tables(statistics_vacancies):
    TABLE_DATA_VACANCIES.append(("Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"))

    data_vacancies = statistics_vacancies.items()
    for statistics in data_vacancies:
        row_table = (statistics[0], statistics[1]['vacancies_found'], statistics[1]['vacancies_processed'],
                     statistics[1]['average_salary'])
        TABLE_DATA_VACANCIES.append(row_table)

    return TABLE_DATA_VACANCIES


def main():
    load_dotenv()
    secret_key_superjob = os.getenv("SUPERJOB_SECRET_KEY")

    if secret_key_superjob is None:
        sys.exit('[*]SuperJob authorization key not found')

    programming_languages = ['Python', 'C', 'C++', 'C#', 'Shell', 'Javascript', 'Java', 'PHP']

    try:
        try:
            for language in programming_languages:
                predict_rub_salary_for_SuperJob(language, secret_key_superjob)
            title_sj = "SuperJob (Moscow)"
            table = generate_tables(STATISTICS_VACANCIES_SJ)
            table_statistics = DoubleTable(table, title_sj)
            print(table_statistics.table)
            print()
        except requests.exceptions.HTTPError as http_err:
            print(f'[*] Check that the SuperJob SECRET KEY is correct\n {http_err}')
        except requests.exceptions.ConnectionError as connect_err:
            exit(f'[*] Check Your network connection\n {connect_err}')
        for language in programming_languages:
            predict_rub_salary_for_HeadHunter(language)
        TABLE_DATA_VACANCIES.clear()
        title_hh = "HeadHunter (Moscow)"
        table = generate_tables(STATISTICS_VACANCIES_HH)
        table_statistics = DoubleTable(table, title_hh)
        print(table_statistics.table)
        print()
    except requests.exceptions.RequestException as err:
        print(f'[*] Something went wrong\n {err}')


if __name__ == "__main__":
    main()
