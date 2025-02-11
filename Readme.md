- собрать и запустить контейнеры:
```
docker compose up -d --build
```

- После успешной сборки выполнить следующие действия:

Выполнить миграции:

```
sudo docker exec backend python manage.py makemigrations
```

```
sudo docker exec backend python manage.py migrate
```

Собрать статику:

```
sudo docker exec backend python3 manage.py collectstatic --no-input
```

Загрузить тестовые данные для PostgreSQL:

```
sudo docker exec -it backend python3 manage.py load_data_postgresql
```

Загрузить тестовые данные для sqlite3:

```
sudo docker exec -it backend python3 manage.py load_data_sqlite3
```

Остановить контейнеры и удалить их вместе с волюмами:

```
docker compose down -v
```