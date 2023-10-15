# Project run

### Run the project on uvicorn.
```shell
uvicorn main:app --reload
```

### Swagger
```
http://127.0.0.1:8000/docs
```

***
# Alembic

### Autogenerate alembic migration
```shell
alembic revision --autogenerate -m "<commit message>"
```

### Apply head migration
```shell
alembic upgrade head
```

***
# Pre commit stage

### Run pre commit check all files
```shell
pre-commit run --all-files
```

### Modifying pre-commit-config.yaml
Modify .pre-commit-config.yaml if needed to set up some pre commit checks
(Проверку Линтером не добавлял)


***
# Tests

Настройку конфигурации тестов, а также основные фикстуры можно посмотреть в `tests/conftest.py`.
Основной запуска тестов:
```shell
pytest tests/rest_routes
```

Отобразить при запуске тестов output (Debug mode)
```shell
pytest --capture=no
pytest -s
```
