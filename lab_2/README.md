запустити збірку проєкта 

    docker compose up -d --build
    docker compose exec app bash
    poetry install

тестування завдань

1. генеруємо тестові дані

    poetry run generate

2. запускаємо тестування моделі на даних

    poetry run main

переглянути результат можна в папці src/lab_2/results