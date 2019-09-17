from __future__ import print_function

import math
import os
import sys

import requests
from dotenv import load_dotenv
from terminaltables import DoubleTable


def predict_rub_salary_for_SuperJob(language_computer):

    url = "https://api.superjob.ru/2.0/vacancies/catalogues/"

    headers = {
        "X-Api-App-Id": secret_key_superjob
    }

    payload = {
        "t": "4",
        'keyword': f'{language_computer}'
    }

    stata_SJ = {}
    response_SJ = requests.get(url, headers=headers, params=payload)
    response_SJ.raise_for_status()
    vacancies_total = response_SJ.json()['total']
    stata_SJ['vacancies_found'] = vacancies_total
    pages = math.ceil(vacancies_total / 20)
    vacancies_suitable = 0
    page = 0
    while page < pages:
        response = requests.get(url, headers=headers,
                                params={'page': page, 'keyword': f'{language_computer}', "t": "4"})
        response.raise_for_status()
        page += 1
        vacancies = response.json()['objects']
        for vacancy in vacancies:
            professions = vacancy['catalogues']
            for profession in professions:
                if profession['id'] == 33:
                    if vacancy['currency'] == 'rub':
                        limit_lower = vacancy['payment_from']
                        limit_upper = vacancy['payment_to']
                        if limit_lower + limit_upper == 0:
                            pass
                        else:
                            vacancies_suitable += 1
                            predict_salary(limit_lower, limit_upper)
    stata_SJ['vacancies_processed'] = vacancies_suitable
    stata_SJ['average_salary'] = int(sum(average_salary) / len(average_salary))
    statistics_vacansies_SJ[language_computer] = stata_SJ
    return statistics_vacansies_SJ


def predict_rub_salary_for_HeadHunter(computer_language):
    url = "https://api.hh.ru/vacancies"
    vacancies_suitable = 0
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/76.0.3809.132 Chrome/76.0.3809.132 Safari/537.36"
    }

    payload = {
        "text": f"Программист {computer_language}",
        "area": "1",
        "period": "30",
        "only_with_salary": "true",
        "salary.from": "true",
        "salary.to": "true"
    }

    response_HH = requests.get(url, headers=headers, params=payload)
    response_HH.raise_for_status()
    vacancies = response_HH.json()['items']
    found = response_HH.json()['found']
    pages = response_HH.json()['pages']
    data = dict(vacancies_found=found)
    page = 0
    while page < pages:
        response_HH = requests.get(url, headers=headers, params={'page': page})
        response_HH.raise_for_status()
        page += 1
        for vacancy in vacancies:
            if vacancy['salary']['currency'] != 'RUR':
                pass
            else:
                salary = vacancy['salary']
                name_vacancy = vacancy['name']
                limit_lower = salary['from']
                limit_upper = salary['to']
                if limit_lower and limit_upper is None:
                    pass
                else:
                    vacancies_suitable += 1
                    predict_salary(limit_lower, limit_upper)
    data['vacancies_processed'] = vacancies_suitable
    data['average_salary'] = int(sum(average_salary) / len(average_salary))
    statistics_vacansies_HH[computer_language] = data
    return statistics_vacansies_HH


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to is not None:
        average = int((salary_from + salary_to) / 2)
        average_salary.append(average)
    elif salary_from and salary_to is None:
        pass
    elif salary_from is None:
        average = int(salary_to * 0.8)
        average_salary.append(average)
    else:
        average = int(salary_from * 1.2)
        average_salary.append(average)
    return average_salary


def creating_tables(dictionary, title):
    TABLE_DATA = [
        ("Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата")
    ]
    data = dictionary.items()
    for statistics in data:
        vacansies = (statistics[0], statistics[1]['vacancies_found'], statistics[1]['vacancies_processed'],
                     statistics[1]['average_salary'])
        TABLE_DATA.append(vacansies)

    table_instance = DoubleTable(TABLE_DATA, title)
    print(table_instance.table)
    print()
    return tuple(TABLE_DATA)


def main():
    pass


if __name__ == "__main__":
    main()

    load_dotenv()
    secret_key_superjob = os.getenv("KEY")
    if secret_key_superjob is None:
        sys.exit('[*]Sorry, something went wrong')

    languages_computer = ['Python', 'C', 'C++', 'C#', 'Shell', 'Javascript', 'Java', 'PHP']
    statistics_vacansies_SJ = {}
    for language_computer in languages_computer:
        average_salary = []
        predict_rub_salary_for_SuperJob(language_computer)
    title_SJ = "SuperJob (Moscow)"
    creating_tables(statistics_vacansies_SJ, title_SJ)
    statistics_vacansies_HH = {}
    for language_computer in languages_computer:
        average_salary = []
        predict_rub_salary_for_HeadHunter(language_computer)
    title_HH = "HeadHunter (Moscow)"
    creating_tables(statistics_vacansies_HH, title_HH)
