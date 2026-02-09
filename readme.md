# URL Shortener

Простой сервис для сокращения ссылок на Python 3.12 + FastAPI + SQLite.

## Установка и запуск

1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows
```

3. Установите проект и зависимости:
```bash
pip install .
```
*Если планируете запускать тесты:* `pip install ".[test]"`

4. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000`.
Интерактивная документация (Swagger): `http://127.0.0.1:8000/docs`.

## Тестирование
Для запуска тестов выполните:
```bash
pytest
```
```