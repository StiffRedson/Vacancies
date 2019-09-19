# Статистика вакансий c сайтов SuperJob и HeadHanter
___

Скрипт выведет статистику по вакансиям программирования по 8-ми наиболее популярным языкам программирования по версии [GitHub](https://habr.com/ru/post/310262/).    
Вакансии отслеживаются с сайтов [HeadHanter](https://hh.ru/) и [SuperJob](https://www.superjob.ru/).    
В консоли вы увидите вывод в виде таблицы по каждой специальности.    
* Кол-во найденых вакансий    
* Кол-во вакансий с указанной зарплатой в рублях   
* Средняя зарплата по данной специальности    

## Как установить?
---
* Установите Python3    
* Сделайте клон проекта к себе на компьютер    
* Настройте окружение в папке проекта    

  ```
  pip install -r requirements.txt
  ```

* Получите ключ авторизфции на [SuperJob](https://api.superjob.ru/).    
Создайте фаил .env и укажите в нем значение ключа следующим образом.    
>SUPERJOB_SECRET_KEY=*Ваш ключ авторизации*    

## Цели проекта
---
Код создан в образовательных целях на сайте для веб-разработчиков [dvmn.org](https://dvmn.org/modules/)

## Автор
---
| Contacts | Ivan Fedorov          |
|----------|-----------------------|
| Email    | StiffRedson@gmail.com |
| Telegram | @StivaRedson          |