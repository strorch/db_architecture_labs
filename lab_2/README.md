запустити збірку проєкта 

    docker compose up -d --build
    docker compose exec app bash
    poetry install

тестування завдань

завдання 1

    poetry run mongo_add_values

завдання 2

    poetry run mongo_get_values

завдання 3

    poetry run mongo_get_aggregated_values

завдання 4

    poetry run redis_add_values
    poetry run redis_get_values
    poetry run redis_update_values
    poetry run redis_delete_values